from gpatom.gpfp.calculator import copy_image, GPCalculator, Model
from gpatom.gpfp.kerneltypes import EuclideanDistance
from gpatom.gpfp.fingerprint import RadialAngularFP
from gpatom.gpfp.prior import RepulsivePotential, CalculatorPrior
from gpatom.gpfp.prior import PriorDistributionSigmoid
from gpatom.gpfp.hpfitter import HyperparameterFitter, GPPrefactorFitter
from gpatom.acquisition import LowerBound

from gpatom.beacon.inout import FileWriter, FileWriter2

from ase.optimize import BFGS
from ase.io import read, write
from ase.calculators.singlepoint import SinglePointCalculator
from ase.parallel import world
from ase.constraints import FixAtoms

from ase.data import covalent_radii
from scipy.spatial import distance_matrix

import numpy as np
import warnings
import os


class BEACON():

    '''
    Bayesian Exploration of Atomic Configurations for Optimization
    --------------------------------------------------------------

    Optimizer to search for the global minimum energy.

    Find optimal structure of a set of atoms given the
    number of atoms, size and periodicity of the unit cell
    and the potential. The calculator uses Gaussian process
    to model the global potential energy landscape, by
    representing the atomic structure by a rotationally,
    translationally and permutationally invariant fingerprint,
    and searches for the absolute minimum of the landscape.

    The original idea behind the method is published
    (along with the code GOFEE) as
        Efficient Global Structure Optimization with a
        Machine-Learned Surrogate Model
        M. K. Bisbo, B. Hammer
        Physical Review Letters, vol. 124, 086102 (2020)
        https://doi.org/10.1103/PhysRevLett.124.086102

    BEACON is published as
        Global optimization of atomic structures with
        gradient-enhanced Gaussian process regression
        S. Kaappa, E. G. del R\'io, K. W. Jacobsen
        Physical Review B, vol. 103, 174114 (2021)
        https://doi.org/10.1103/PhysRevB.103.174114

    Usage:
    1. Create a class instance as
         from gpatom.beacon import BEACON
         go = BEACON(calc=..., sgen=..., ...)
    2. Find optimal structure:
         go.run()

    Parameters:

    calc : Calculator (class name)
        This calculator is invoked every time a real energy
        is calculated. The parameters are given by 'calcparams'

    sgen : RandomStructure instance
        A structure generator that generates initial structures
        for the surrogate minimizations. The given object has
        to have a get() method which gives a structure. A set
        of simple generators is given in file str_gen.py

    calcparams : dict
        Parameters to 'calc'

    atoms : list of ase.Atoms
        Initial training images. If not given, the initial
        set is created with structures given by 'sgen'

    ninit: int
        Number of initial training structures if atoms is not
        given. Default 2

    ndft : int
        Maximum number of search steps during the search.
        After this number of steps, go.run() is terminated.
        Default 100

    nsur : int
        Number of relaxations in surrogate potential at each step
        Default world.size

    nbest : int
        Number of DFT-evaluated structures included in the
        pool of initial structures to be relaxed in the
        surrogate model. Default 0

    nrattle : int
        Number of rattled best structures to be added in the
        pool of initial structures for surrogate relaxations
        Default 0

    gp_args : dict
        Parameters for a GPCalculator object. Default is None,
        in which case the parameters are set automatically.

    largescalefactor : float
        The initial scale is obtained by multiplying the max
        fingerprint norm by this number. This has no effect is
        the length scale is given in gp_args['params'].

    stopfitsize : int
        Number of DFT calculations after which fitting the
        hyperparameters is stopped. Does not affect prefactor
        and prior constant fitting. Default 10000 (=never)

    acq : object
        Acquisition function object. Default LowerBound(kappa=2)

    relax_steps : int
        Maximum number of steps for a surrogate relaxation.
        Default 100

    fmax : float
        Force convergence criterion for surrogate relaxations
        Default 0.05

    checks : bool
        Whether to check valid structure before accepting the
        acquisition function. Default True

    write_surropt_trajs : bool
        Whether to write all the trajectory files of the
        surrogate relaxations. Default False

    neglect_limit : float (units: eV)
        Do not add a data point to the training set if its
        energy exceeds this number. Default is None, letting
        all data points be added to training set.

    dist_limit : float
        Set acquisition function of structure to inf if the
        smallest distance to a training point is below this
        number. Default is 0.0, letting all structures to be
        selected.

    realfmax : float
        Force convergence criterion (in real potential),
        below which a structure is considered converged and
        is then removed from the list-of-best-structures.
        Default 0.1

    rng : np.random.RandomState object
        Random number generator with possible seed to produce
        reproducible results. Default np.random , that is, no
        reproducibility.

    output : string
        Filename of the output for results and parameters.
        Default info.txt

    foutput : string
        Filename of the output for predicted and evaluated forces.
        Default os.devnull (not writing the file)

    logoutput : string
        Filename of the log book. Default log.txt
    '''

    def __init__(self, calc, sgen, calcparams=None, atoms=None,
                 ninit=2, ndft=100, nsur=None, nbest=0, nrattle=0,
                 gp_args=None, largescalefactor=20, stopfitsize=10000,
                 acq=None, relax_steps=100, fmax=0.05,
                 write_surropt_trajs=False, checks=True,
                 neglect_limit=None, dist_limit=0.0,
                 realfmax=0.10,
                 rng=np.random, output='info.txt', foutput=os.devnull,
                 logoutput='log.txt'):

        if calcparams is None:
            calcparams = {}

        if gp_args is None:
            gp_args = {}

        # Initialize self.atoms:
        if (atoms is not None) and (gp_args.get('train_images') is not None):
            warnings.warn('Atoms object specified in both atoms and gp_args. '
                          'Using atoms argument.')

        if atoms is None and gp_args.get('train_images') is None:
            atoms = []
            for i in range(ninit):
                atoms.append(sgen.get())

        elif atoms is None:
            atoms = gp_args.get('train_images')

        self.atoms = atoms

        # Determine training on forces in GP:
        use_forces = gp_args.get('use_forces', True)

        # Constraints:
        self.constr = ConstraintHandler(self.atoms[0])

        # Atoms reader/writer:
        self.atomsio = BEACONAtomsIO(use_forces=use_forces)

        # Make sure each processor has same initial training structures:
        self.atomsio.distribute_atomslist(self.atoms, constr=self.constr)

        # Run parameters:
        self.ndft = ndft
        self.nsur = nsur if nsur is not None else world.size
        assert self.nsur > 0

        # Initialize number of extra structures:
        self.extracount = 0

        # True potential:
        self.calc = calc
        self.calcparams = calcparams

        # Log files:
        self.output = output
        self.foutput = foutput
        self.logoutput = logoutput

        # Acquisition function:
        if acq is None:
            acq = LowerBound(kappa=2)
        self.acq = acq

        # Initial DFT calculations:
        self.set_initial_frames(use_forces=use_forces)

        # Initialize Gaussian process:
        self.gpinterface = BEACONGPInterface(gp_args=gp_args,
                                             largescalefactor=largescalefactor,
                                             stopfitsize=stopfitsize,
                                             initatoms=self.atoms)

        # List of best structures:
        lob = StructureList(self.atoms,
                            n=nbest,
                            flim=realfmax)

        # Initial atoms generator:
        self.initatomsgen = InitatomsGenerator(nrattle=nrattle,
                                               sgen=sgen,
                                               lob=lob,
                                               rng=rng)

        # Surrogate optimizer:
        self.surropt = SurrogateOptimizer(fmax=fmax,
                                          relax_steps=relax_steps,
                                          write_surropt_trajs=write_surropt_trajs)
        # Checker:
        self.checker = Checker(checks=checks, dist_limit=dist_limit,
                               rlimit=0.7, blimit=-np.inf,
                               energylimit=neglect_limit)

        # Run GP once:
        testatoms = self.initatomsgen.get()
        self.gpinterface.calculate(testatoms)

        # Initialize attributes that are invoked in run():
        self.generalfile = None  # FileWriter2
        self.logfile = None  # FileWriter
        self.forcefile = None  # FileWriter

    def set_initial_frames(self, use_forces=True):
        '''
        Calculate energies and forces for initial training images,
        and save to files.
        '''

        for i in range(len(self.atoms)):
            try:
                self.get_properties(self.atoms[i])
            except RuntimeError:  # no calculator attached
                calc = self.new_calc()
                self.atoms[i].calc = calc
                self.get_properties(self.atoms[i])

                tmp = copy_image(self.atoms[i])
                self.atoms[i] = tmp

            self.atomsio.write_xyz(self.atoms[i], strtype='init')

    def new_calc(self):
        ''' Return new Calculator object '''

        return self.calc(**self.calcparams)

    def run(self):
        ''' Run search '''

        # INITIALIZE
        self.initialize_outputfiles()
        self.log_init_structure_info()
        index = 0

        # RUN GLOBAL SEARCH
        while index < self.ndft:

            # INITIALIZE
            self.log_stepinit(index)
            it_result = IterationResult(self.atoms[0])

            self.log_lob_energies()

            for j in range(self.nsur):

                # DISTRIBUTE SURROGATE RELAXATIONS
                if j % world.size != world.rank:
                    continue

                # CREATE NEW STRUCTURES
                testatoms = self.initatomsgen.get(j)

                # SURROGATE RELAXATION
                testatoms = self.relax_surrogate(testatoms, index=index,
                                                 subindex=j)

                # WRITE
                energy, forces, unc = self.get_local_properties(testatoms)
                self.log_relaxedinfo(index=index, energy=energy,
                                     unc=unc, subindex=j)

                # CHOOSE BEST (within a processor)
                my_acq = self.acq.get(energy=energy,
                                      uncertainty=unc)
                better_acq = it_result.is_better(my_acq)

                # CHECK
                if self.checker.checks:
                    distances = self.calculate_distances(testatoms)
                    structure_ok = self.checker.check(atoms=testatoms,
                                                      distances=distances,
                                                      index=index,
                                                      subindex=j,
                                                      logfile=self.logfile)
                else:
                    structure_ok = True
                    self.log_from_master('Structure checks set to False!!!')

                # WRITE
                if better_acq and structure_ok:
                    it_result.update(dict(energy=energy,
                                          forces=forces.flatten().copy(),
                                          unc=unc,
                                          atoms=testatoms,
                                          acq=my_acq,
                                          subindex=j))

            # CHOOSE BEST (between processors)
            (rank_with_best, best_atoms, best_e,
             best_f, best_u, best_acq, best_subindex) = it_result.distribute()

            # CHECK
            if best_acq == np.inf:
                self.log_novalid()

                # Add a new random structure to training set, to
                # try to get rid of resulting invalid structures:
                self.add_random_structures()

                continue

            # LOG
            self.log_bestinfo(index, best_subindex, best_e, best_u, best_acq)

            # DISTRIBUTE
            best_atoms = self.atomsio.distribute_atoms(best_atoms,
                                                       rank=rank_with_best,
                                                       columns=None,
                                                       write_results=False)

            # DFT
            try:
                real_e, real_f = self.get_real(index, best_atoms)
            except Exception as err:
                self.log_from_master('Something went wrong: {} '
                                     'Continuing...'.format(str(err)))
                continue

            # CHECK
            if self.checker.check_bad_result(energy=real_e):
                self.log_badresults(index, real_e)
                continue

            best_atoms = copy_image(best_atoms)  # release memory

            # WRITE RESULT XYZ
            self.atomsio.write_xyz(best_atoms, strtype='result')

            # WRITE RESULT NUMBERS
            # Calculate distances between the fresh structure
            # and the training set:
            distances = self.calculate_distances(best_atoms)
            self.write_results(index, best_e, best_f, best_u,
                               real_e, real_f, distances)

            # ITERATE
            index += 1

            if index == self.ndft:  # if last round:
                break

            # UPDATE GAUSSIAN PROCESS
            self.retrain(best_atoms)

            # UPDATE LIST OF BEST
            self.update_list_of_best(best_atoms, index, best_subindex)


        self.log_from_master('Maximum number of steps '
                             '({}) reached.'.format(self.ndft))

    def get_properties(self, atoms, constr=False):
        '''
        Calculate energy and forces of atoms. Return potential energy.
        '''
        e = atoms.get_potential_energy(force_consistent=None,
                                       apply_constraint=constr)
        atoms.get_forces(apply_constraint=constr)
        return e

    def get_local_properties(self, atoms):
        '''
        Calculate energy and forces in the surrogate potential.
        '''

        local_e, local_f, local_u = self.gpinterface.calculate(atoms)

        return local_e, local_f, local_u

    def get_real(self, index, atoms):
        '''
        Get correct energy of the best found structure.
        '''

        atoms.center()
        atoms.wrap()

        atoms.calc = self.new_calc()
        real_e = self.get_properties(atoms)
        real_f = atoms.calc.results['forces'].flatten()

        txt = 'Index: {:03d} Real energy: {:06f}'
        txt = txt.format(index, real_e)
        self.log_from_master(txt)

        return real_e, real_f

    def add_random_structures(self):
        '''
        Add a structure (by sgen) to the training set.
        '''

        # Get structure:
        atoms = self.initatomsgen.get()
        atoms = self.atomsio.distribute_atoms(atoms, constr=self.constr,
                                              columns=None)

        # Evaluate:
        atoms.calc = self.new_calc()
        self.get_properties(atoms)
        self.update_list_of_best(atoms=atoms, index=-1, subindex=np.inf)

        # Make a list for re-training:
        new_structures = [copy_image(atoms)]

        # Re-train the model:
        self.gpinterface.add_training_points(new_structures)

        # Write extra_NNN.xyz file:
        if world.rank == 0:
            self.atomsio.write_xyz(atoms, strtype='extra',
                                   parallel=False)

        # Save number of extra structures:
        self.extracount += 1

    def relax_surrogate(self, atoms, index, subindex):
        '''
        Local optimization of the coordinates of 'atoms'.
        '''

        atoms.calc = self.gpinterface.get_model_calculator(calculate_uncertainty=False)

        # Relax in surrogate potential:
        if self.surropt.dont_relax:
            self.success = True
        else:
            self.success = self.surropt.relax(atoms, index=index,
                                              subindex=subindex)

        return atoms

    def calculate_distances(self, atoms):
        '''
        Calculate distance of a structure to
        all existing structures in training set of self.gpinterface.gpcalc.
        '''

        distances = self.gpinterface.calculate_distances(atoms)
        return distances

    def retrain(self, atoms):
        '''
        Retrain the Gaussian process with new structures given
        by 'atoms'.
        '''
        self.constr.set_constraints(atoms)
        self.gpinterface.add_training_points([atoms])

    def get_max_force(self, forces):
        '''
        Get maximum absolute force of the given force array. Does
        not take into account the forces on constrained atoms.
        '''
        forces = forces.reshape(-1, 3)[self.constr.ucindex]
        return np.max(np.linalg.norm(forces, axis=1))

    def update_list_of_best(self, atoms, index, subindex):
        '''
        Update the pool of best structures which some of the new
        surrogate relaxations are started from.
        '''

        converged = self.initatomsgen.lob.update(new_atoms=atoms,
                                                 index=subindex)

        if converged:
            self.log_reallocalminimum(e=atoms.get_potential_energy(),
                                      index=index)

    # --------------- LOGGING METHODS ------------------
    # --------------------------------------------------

    def initialize_outputfiles(self):

        if world.rank == 0:
            self.generalfile = FileWriter2(self.output, printout=False)
            self.forcefile = FileWriter(self.foutput, printout=False)

        # All processors
        self.logfile = FileWriter(self.logoutput, printout=False,
                                  write_time=True)

    def log_from_master(self, txt):
        if world.rank == 0:
            self.logfile.write(txt)

    def log_init_structure_info(self):
        world.barrier()
        for i in range(len(self.atoms)):
            txt = ('Init structure {:03d} '
                   'Energy: {:.02f} eV '
                   'Max force: {:.02f} eV/Ang'
                   .format(i,
                           self.atoms[i].get_potential_energy(),
                           self.get_max_force(self.atoms[i].get_forces())))
            self.log_from_master(txt)

    def log_stepinit(self, index):
        txt = ('Index: {:03d} Training data size: {:5d}'
               .format(index, self.gpinterface.ntrain))
        self.log_from_master(txt)

    def log_relaxedinfo(self, index, energy, unc, subindex):
        ''' Log from all processors '''
        notconverged = ''
        if not self.success:
            notconverged = '(Not converged)'
        self.logfile.write('Index: {:03d} Subindex: {:03d} '
                           'Energy: {:.04f} Uncertainty: {:.04f} {}'
                           .format(index, subindex,
                                   energy, unc,
                                   notconverged))

    def log_novalid(self):
        txt = 'No valid structure found. Continuing...'
        self.log_from_master(txt)

    def log_bestinfo(self, index, best_subindex, best_e, best_u, best_acq):
        txt = 'Index: {:03d} '
        txt += 'Best structure: '
        txt += 'Subindex: {:03d} '
        txt += 'Energy: {:04f} '
        txt += 'Uncertainty: {:04f} '
        txt += 'Acquisition: {:04f} '
        txt = txt.format(index, best_subindex, best_e,
                         best_u, best_acq)
        self.log_from_master(txt)

    def log_badresult(self, index, energy):
        txt = ('Index: {:03d} '
               'Neglected energy: {:09.04f} eV'
               .format(index, energy))
        self.log_from_master(txt)

    def log_lob_energies(self):
        '''
        Write energies from list-of-best-structures
        to log file.
        '''

        listofbest_e = self.initatomsgen.lob.energies
        if len(listofbest_e) == 0:
            txt = 'List of best energies is empty.'
            self.log_from_master(txt)
        else:
            txt = 'List of best energies:'
            self.log_from_master(txt)
            for i, e in enumerate(listofbest_e):
                txt = ('Index: {:03d} Energy: {:04f}'
                       .format(i, e))
                self.log_from_master(txt)

    def write_results(self, index, pred_e, pred_f,
                      unc, real_e, real_f, distances):
        '''
        Write all results of a single loop, i.e.
        after a DFT calculation.
        '''

        toforcefile = ""
        pred_list = [pred_e] + list(pred_f)
        real_list = [real_e] + list(real_f)
        for pred, real in zip(pred_list, real_list):
            txt = "i: {:5d} {:12.04f} {:12.04f} \n"
            toforcefile += txt.format(index, pred, real)

        fmax = self.get_max_force(real_f)

        data = dict(index=index,
                    pred=pred_e,
                    real=real_e,
                    unc=unc,
                    diff=real_e - pred_e,
                    fmax=fmax,
                    mindist=distances.min(),
                    maxdist=distances.max(),
                    ntrain=self.gpinterface.ntrain,
                    prior=self.gpinterface.prior,
                    noise=self.gpinterface.noise)

        data.update(self.gpinterface.model.gp.hp)

        if world.rank == 0:
            self.generalfile.write(data)
            self.forcefile.write(toforcefile)
            self.forcefile.write("")

    def log_reallocalminimum(self, index, e):
        txt = 'Index: {:03d} Real local minimum! Energy: {:04f}'
        txt = txt.format(index, e)
        self.log_from_master(txt)


class LocalOptimizer(BEACON):
    '''
    For testing a model. The model is not re-trained after
    after an optimization step.

    That is, multiple surrogate relaxations are performed and
    their final configuration is evaluated with DFT with a
    fixed training set and hyperparameters.
    '''

    def retrain(self, **kwargs):
        '''
        Dont retrain the model.
        '''
        return

    def add_random_structures(self):
        '''
        Dont add random structures if an optimization produces
        an invalid structure.
        '''
        return


class StructureList:

    def __init__(self, images, n, flim=0.1):
        '''
        This class handles the list of best structures in
        BEACON.

        Parameters:

        atoms: list
            list of ase.Atoms objects
        n: int
            Number of structures to store in the list
        flim: float
            Force threshold. If the maximum force of an atomic
            structure is below this number, it is excluded
            from the list.
        logfile: FileWriter instance
            Writer to handle output writing. Defaults to None,
            that is no output is written by this class.
        '''

        self.n = n  # number of structures
        self.structurelist = []
        self.update_list_by_many(images)
        self.flim = flim

    def update_list_by_many(self, images):
        self.structurelist += images
        self.sort_structurelist()

    def update_list_by_one(self, atoms, overwrite_index=None):
        if overwrite_index is None:
            self.structurelist += [atoms]
        else:
            self.structurelist[overwrite_index] = copy_image(atoms)
        self.sort_structurelist()

    def sort_structurelist(self):
        '''
        Sort images by their potential energies and create a list
        of the sorted structures with maximum length of self.n
        '''

        argsort = np.argsort(self.energies)
        self.structurelist = [copy_image(self.structurelist[i])
                              for i in argsort[:self.n]]

    @property
    def energies(self):
        '''
        Return all potential energies for the structures in the list.
        '''
        return [atoms.get_potential_energy()
                for atoms in self.structurelist]

    def update(self, new_atoms, index):
        '''
        Update the list of best structures.
        Returns True if structure is converged. False if not.
        '''

        e = new_atoms.get_potential_energy()
        f = new_atoms.get_forces()

        # Check if all the forces are below the threshold:
        real_local_min = (np.max(np.linalg.norm(f.reshape(-1, 3),
                                                axis=1)) < self.flim)

        # Check if the structure was obtained
        # by relaxing a structure on the previous list-of-best:
        one_of_listofbest = index < len(self)

        # If it is a real local minimum, return True
        if real_local_min:
            if one_of_listofbest:
                # delete image from list of best
                self.structurelist.pop(index)
            return True

        # Don't add but update if the structure
        # was obtained by relaxing something already on the list:
        overwrite_index = None
        if one_of_listofbest and (e < self.energies[index]):
            overwrite_index = index

        # Add structure to the list:
        self.update_list_by_one(new_atoms, overwrite_index=overwrite_index)

        return False

    def __len__(self):
        return len(self.structurelist)

    def __getitem__(self, i):
        return self.structurelist[i]


class InitatomsGenerator:
    '''
    Generator to give structures for surrogate relaxations in BEACON.
    The relaxations start from some of the already visited low-energy
    structures, the same structures rattled, or random structures.
    '''

    def __init__(self, nrattle, sgen, lob=None,
                 rattlestrength=0.5, rng=np.random):
        self.nrattle = nrattle
        self.lob = lob  # StructureList instance
        self.rattlestrength = rattlestrength
        self.rng = rng
        self.sgen = sgen

    def get(self, i=None):
        '''
        Parameters:

        i: int
            Index that indicates what type of structure is
            returned. (one of best, rattled one of best, or
            random). If None, structure from sgen is given.
        '''

        n_best = self.get_nbest()

        if i is None:
            i = np.inf

        atoms = self.get_atoms(i, n_best)
        return atoms

    def get_nbest(self):
        '''
        Get number of best structures in the current state of
        list-of-best.
        '''

        if self.lob is None:
            return 0

        return len(self.lob)

    def get_atoms(self, i, n_best):
        '''
        Get atoms of different types based on the index 'i'
        and the number of best structures 'n_best'.
        '''

        # One of best:
        if i < n_best:
            atoms = self.get_one_of_best_atoms(i)

        # Rattled one of best:
        elif self.get_rattled_criterion(i, n_best):
            atoms = self.get_rattled_one_of_best(i, n_best)

        # One given by structure generator:
        else:
            atoms = self.sgen.get()

        return atoms

    def get_one_of_best_atoms(self, i):
        '''
        Get i'th structure from the list of best.
        '''
        return self.lob[i].copy()

    def get_rattled_one_of_best(self, i, n_best):
        '''
        Get i'th structure from the list of best and rattle it.
        '''
        atoms = self.lob[i % n_best].copy()
        atoms.rattle(self.rattlestrength,
                     seed=self.rng.randint(100000))
        atoms.wrap()
        return atoms

    def get_rattled_criterion(self, i, n_best):
        return (n_best > 0) and (i < n_best + self.nrattle)


class BEACONGPInterface:
    '''
    Interface that handles all communication between BEACON and
    Gaussian processes.
    '''

    def __init__(self, gp_args=None,
                 largescalefactor=20,
                 stopfitsize=1000000,
                 initatoms=None):

        # Default GP:
        prior_calc = RepulsivePotential()
        prior_calc.parameters.rc = 4.0
        prior_calc.parameters.prefactor = 0.7
        default_gp_args = dict(train_images=None,
                               fingerprint=RadialAngularFP,
                               prior=CalculatorPrior(prior_calc),
                               kerneltype='sqexp',
                               params={'scale': 1, 'weight': 1,
                                       'noise': 1e-3, 'noisefactor': 0.5},
                               use_forces=True)

        self.fit_weight = True
        self.scaleprior = PriorDistributionSigmoid(loc=15, width=0.001)
        self.batch_size = 5

        # Initialize gp_args:
        if gp_args is None:
            gp_args = {}

        given_gp_args = gp_args.copy()
        default_gp_args.update(gp_args)
        gp_args = default_gp_args
        self.gp_args = gp_args

        self.stopfitsize = stopfitsize

        self.initialize_parameters(given_gp_args, initatoms, largescalefactor)
        self.model = self.initialize_model(initatoms)

    @property
    def ntrain(self):
        return len(self.model.data)

    @property
    def prior(self):
        return self.model.gp.prior.constant

    @property
    def noise(self):
        return self.model.gp.hp['noise']

    @property
    def hp(self):
        ''' Hyperparameter dictionary '''
        return self.model.gp.hp

    def initialize_parameters(self, args, atomslist, largescalefactor):
        params_given = 'params' in args.keys()

        if callable(getattr(self.gp_args['fingerprint'],
                            'get_fit_aweight', None)):
            if (not params_given) or ('aweight' not in args['params']):
                aweight = self.get_aweight(atomslist)
            else:
                aweight = args['params']['aweight']
        else:
            aweight = 1.0
        self.update_params({'aweight': aweight})

        if (not params_given) or ('scale' not in args['params']):
            scale = self.get_large_scale(atomslist, largescalefactor)
        else:
            scale = args.get('params').get('scale')

        self.update_params({'scale': scale})

    def get_aweight(self, atomslist):
        fp = self.gp_args['fingerprint']
        params = self.gp_args['params']
        fps = [fp(atoms=atoms, calc_gradients=False, **params)
               for atoms in atomslist]

        return fps[0].get_fit_aweight(fps)

    def get_large_scale(self, atomslist, largescalefactor):
        '''
        Set the scale of gp_args to a large value as compared
        to the fingerprint norms.
        '''

        fp = self.gp_args['fingerprint']
        params = self.gp_args['params']
        fps = [fp(atoms=atoms, calc_gradients=False, **params)
               for atoms in atomslist]
        norms = [np.linalg.norm(fp0.vector)
                 for fp0 in fps]

        return largescalefactor * np.max(norms)

    def update_params(self, new_params):
        '''
        Update params dictionary in self.gp_args.
        '''
        self.gp_args['params'].update(new_params)

    def update_args(self, new_args):
        '''
        Update arguments in gp_args.
        '''
        self.gp_args.update(new_args)

    def initialize_model(self, atomslist):
        '''
        Initialize Model.
        '''

        self.update_args({'train_images': atomslist})
        model = Model(**self.gp_args)
        model = GPPrefactorFitter.fit(model)

        return model

    def get_model_calculator(self, calculate_uncertainty=True):
        return GPCalculator(self.model,
                            calculate_uncertainty=calculate_uncertainty)

    def calculate(self, atoms):
        '''
        Predict properties for atoms in the surrogate model.
        '''

        atoms.calc = self.get_model_calculator(calculate_uncertainty=True)

        e = atoms.get_potential_energy()
        f = atoms.get_forces()
        u = atoms.calc.results.get('uncertainty')
        return e, f, u

    def add_training_points(self, atomslist):
        '''
        Add training points to calculator.
        '''

        # stop fitting length scale:
        if len(self.model.data) > self.stopfitsize:
            self.batch_size = 100000

        # make sure that lower limit of fitting the scale is
        # not above the current scale:
        self.update_prior_distribution()
        self.fix_scale()

        self.model.add_training_points(atomslist)
        self.model.train_model(self.model.gp, self.model.data)

        self.model = GPPrefactorFitter.fit(self.model)

        if len(self.model.data) % self.batch_size == 0:
            self.model = HyperparameterFitter.fit(self.model, ['scale'],
                                                  fit_weight=True,
                                                  pd=self.scaleprior)

    def calculate_distances(self, atoms):
        '''
        Calculate the distances between the training set and
        given atoms.
        '''
        fp0 = self.model.new_fingerprint(atoms, calc_gradients=False)

        distances = np.zeros(len(self.model.data), dtype=float)

        for i, x in enumerate(self.model.data.fingerprintlist):
            distances[i] = EuclideanDistance.distance(fp0, x)

        return distances

    def update_prior_distribution(self):
        ''' Update the 'loc' attribute of the prior distribution '''
        distances = self.calculate_distances(self.model.gp.X[0].atoms)
        self.scaleprior.loc = np.mean(distances)

    def fix_scale(self):
        '''
        Set length so that it is at least as high
        as its lower bound for fitting.
        '''
        if (len(self.model.data) + 1) % self.batch_size == 0:
            scale = max(self.model.gp.hp['scale'],
                        self.scaleprior.loc)
            self.model.gp.set_hyperparams({'scale': scale})


class SurrogateOptimizer:
    '''
    Small optimizer class to handle local optimizations in BEACON.
    '''

    def __init__(self, fmax=0.05, relax_steps=100,
                 write_surropt_trajs=False):
        self.fmax = fmax
        self.relax_steps = relax_steps
        self.write_surropt_trajs = write_surropt_trajs

    @property
    def dont_relax(self):
        '''
        Return boolean that tells whether the optimizer actually
        relaxes anything, based on self.relax_steps.
        '''
        return self.relax_steps == 0

    def relax(self, atoms, index, subindex):
        '''
        Relax atoms in the surrogate potential.
        '''

        kwargs = dict(atoms=atoms,
                      maxstep=0.2,
                      logfile=os.devnull,
                      master=True)

        if self.write_surropt_trajs:
            fname = 'opt_{:03d}_{:03d}.traj'.format(index, subindex)
            kwargs.update({'trajectory': fname})

        opt = BFGS(**kwargs)

        success = opt.run(fmax=self.fmax, steps=self.relax_steps)
        return success


class ConstraintHandler:
    '''
    Store constraints that are used in Atoms objects in BEACON.
    '''

    def __init__(self, initatoms):
        self.natoms = len(initatoms)
        self.constraints = initatoms.constraints
        self.cindex = self.get_constrained_index()  # FixAtoms index
        self.ucindex = self.get_unconstrained_index()  # negative FixAtoms index

    def get_constrained_index(self):
        '''
        Get the list of indices that are constrained with FixAtoms.
        '''
        constr_index = []
        for C in self.constraints:
            if isinstance(C, FixAtoms):
                constr_index = C.index

        return np.array(constr_index, dtype=int)

    def get_unconstrained_index(self):
        '''
        Get the list of indices that are NOT constrained with FixAtoms.
        '''
        unconstr_index = []
        for i in range(self.natoms):
            if i not in self.cindex:
                unconstr_index.append(i)

        return np.array(unconstr_index, dtype=int)

    def set_constraints(self, atoms):
        '''
        Set the constraints to 'atoms'.
        '''
        for c in self.constraints:
            atoms.set_constraint(c)


class Checker:
    '''
    Check methods for surrogate-relaxed structures. The methods checks
    that the atom-to-atom distances are not too short, that the distance of
    the structure to previous structures is not too small, and that
    the true energy of the structure is low enough.
    '''

    def __init__(self, checks=True, dist_limit=0.0, rlimit=0.7, blimit=-np.inf,
                 energylimit=np.inf):
        self.checks = checks
        self.dist_limit = dist_limit
        self.rlimit = rlimit
        self.blimit = blimit
        self.energylimit = energylimit

    def check_atomic_distances(self, atoms):
        '''
        Check if atoms are too close to each other or
        too close to unit cell boundary.

        Parameters:
        -----------
        atoms : ase.Atoms
        object to check

        rlimit : float
        Limit for check if atoms are too close
        to each other (default 0.7)

        blimit : float
        Limit for check if atoms are too close
        to unit cell boundary (default -np.inf i.e. always valid)
        '''
        atoms = atoms.copy()
        atoms.wrap()
        atoms = atoms.repeat([1 + int(c) for c in atoms.pbc])

        coord = atoms.positions

        # Atoms too close to each other:
        dm = distance_matrix(coord, coord)
        dm += 10.0 * np.eye(len(dm))

        cov_radii = self.rlimit * self.cov_radii_table(atoms)
        if (dm < cov_radii).any():
            return False

        for i in range(3):
            icoord = coord[:, i]
            if (icoord - 0.0 < self.blimit).any():
                return False

        return True

    def check_fingerprint_distances(self, distances):
        '''
        Return True if distances are ok,
        False if not.
        '''
        return np.min(distances) > self.dist_limit

    def check(self, atoms, distances, index, subindex, logfile=None):
        '''
        Check the atomic distances and the fingerprint distances of
        'atoms'.
        '''

        if logfile is None:
            logfile = FileWriter(filename=os.devnull, printout=False)

        fp_distances_ok = self.check_fingerprint_distances(distances)
        if not fp_distances_ok:
            logfile.write('Index: {:03d} Subindex: {:03d} '
                          'Too close to existing structure. '
                          'No accept.'
                          .format(index, subindex))
            return False

        atomic_distances_ok = self.check_atomic_distances(atoms)
        if not atomic_distances_ok:
            logfile.write('Index: {:03d} Subindex: {:03d} '
                          'Structure not valid. No accept.'
                          .format(index, subindex))
            return False

        return True

    def cov_radii_table(self, atoms):
        '''
        Return all-to-all table of the sums of covalent radii for
        atom pairs in 'atoms'.
        '''
        table = [[(covalent_radii[i] + covalent_radii[j])
                  for i in atoms.symbols.numbers]
                 for j in atoms.symbols.numbers]
        table = np.array(table)
        return table

    def check_bad_result(self, energy):
        '''
        Check if the result has so bad energy that
        we don't want to include it into the training set
        '''

        if self.energylimit is None:
            return False

        return energy > self.energylimit


class BEACONAtomsIO:
    '''
    Handle write and read of Atoms objects within BEACON.
    '''

    def __init__(self, use_forces=True):

        self.use_forces = use_forces

        # filenames for writing xyz
        self.initstrfile = 'init_structures.xyz'
        self.structurefile = 'structures_dft.xyz'
        self.tmpfile = 'tmp.xyz'
        self.extrafile = 'extras.xyz'
        self.names_by_type = {'init': self.initstrfile,
                              'result': self.structurefile,
                              'tmp': self.tmpfile,
                              'extra': self.extrafile}

        self.initialize_xyzfiles()

        return

    def initialize_xyzfiles(self):
        '''
        Create empty files.
        '''
        if world.rank == 0:
            for key in self.names_by_type:
                f = open(self.names_by_type[key], 'w')
                f.close()

    def write_xyz(self, atoms, strtype,
                  columns=['symbols', 'positions', 'forces'],
                  append=True, **kwargs):
        '''
        Write atoms to the file specified by strtype.
        '''

        if columns is not None:
            atoms.arrays['forces'] = atoms.get_forces()

        filename = self.names_by_type.get(strtype)

        with warnings.catch_warnings():

            # with EMT, a warning is triggered while writing the
            # results in ase/io/extxyz.py. Lets filter that out:
            warnings.filterwarnings('ignore', category=UserWarning)

            write(filename, atoms, columns=columns,
                  append=append, **kwargs)

    def write_tmpfile(self, atoms, parallel=True, **kwargs):
        '''
        Write a temporary file.
        '''
        write(self.tmpfile, atoms, parallel=parallel, append=False, **kwargs)

    def read_tmpfile(self, parallel=True):
        '''
        Read Atoms from the temporary file.
        '''
        return read(self.tmpfile, parallel=parallel)

    def distribute_atomslist(self, atomslist, constr=None):
        '''
        Distribute the list of Atoms objects over processors
        from master rank.
        '''

        assert type(atomslist) is list

        for i in range(len(atomslist)):
            atomslist[i] = self.distribute_atoms(atomslist[i], constr=constr)

    def distribute_atoms(self, atoms, constr=None, rank=0, **kwargs):
        '''
        Distribute Atoms object from rank 'rank' to all processors.
        '''

        if world.rank == rank:
            self.write_tmpfile(atoms, parallel=False, **kwargs)
        world.barrier()

        atoms = self.read_tmpfile()

        if constr is not None:
            constr.set_constraints(atoms)

        return atoms


class IterationResult:
    '''
    Class to store, update, and distribute results from the
    surrogate relaxations.
    '''

    def __init__(self, atoms):
        '''
        atoms: Atoms object
            A sample of atoms object that is only used to read the
            size of the force array for initialization here.
        '''

        self.best_acq = np.inf
        self.my_best = dict(acq=np.inf,
                            energy=0.0,
                            forces=np.empty(len(atoms) * 3),
                            unc=0.0,
                            subindex=0,
                            atoms=atoms)

    @property
    def my_best_acq(self):
        '''
        Best acquisition function at this rank.
        '''
        return self.my_best['acq']

    def update(self, dct):
        '''
        Update the results for this rank.
        '''
        self.my_best.update(dct)

    def is_better(self, value):
        '''
        Test if value is smaller than my_best_acq.
        '''
        if value < self.my_best_acq:
            return True

        return False

    def distribute(self):
        '''
        Share data between processors, and return the data for the
        structure that has the best acquisition function over all
        ranks.
        '''

        minrank = self.get_min_rank()

        # Share data among processors:
        best_e = np.atleast_1d(self.my_best['energy'])
        best_f = self.my_best['forces']
        best_u = np.atleast_1d(self.my_best['unc'])
        best_acq = np.atleast_1d(self.my_best['acq'])
        my_best_subindex = np.atleast_1d(self.my_best['subindex'])

        best_atoms = self.my_best['atoms']
        world.broadcast(best_e, minrank)
        world.broadcast(best_f, minrank)
        world.broadcast(best_u, minrank)
        world.broadcast(best_acq, minrank)
        world.broadcast(my_best_subindex, minrank)

        # Set results to attributes:
        best_e = best_e[0]
        best_u = best_u[0]
        best_acq = best_acq[0]

        best_subindex = my_best_subindex[0]
        return (minrank, best_atoms, best_e, best_f,
                best_u, best_acq, best_subindex)

    def get_min_rank(self):
        '''
        Get rank with the minimal acquisition function.
        '''
        my_best_acq = np.atleast_1d(self.my_best_acq)

        # List all acquisition functions to an array with the
        # indices corresponding to rank indices:
        all_acqs = np.empty([world.size, 1])
        for rank in range(world.size):
            tmp = my_best_acq.copy()
            world.broadcast(tmp, rank)
            all_acqs[rank] = tmp.copy()

        # Get rank with the best acquisition:
        return np.argmin(all_acqs)
