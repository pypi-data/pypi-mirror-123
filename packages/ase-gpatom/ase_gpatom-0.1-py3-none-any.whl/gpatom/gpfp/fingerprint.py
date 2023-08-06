from math import pi
import itertools
from scipy.spatial import distance_matrix
import numpy as np
import ase


class RadialFP:

    def __init__(self, atoms, calc_gradients=True,
                 weight_by_elements=True, **kwargs):
        ''' Parameters:

        r_cutoff: float
            Threshold for radial fingerprint (Angstroms)

        r_delta: float
            Width of Gaussian broadening in radial fingerprint
            (Angstroms)

        r_nbins: int
            Number of bins in radial fingerprint

        calc_gradients: bool
            Whether gradients are calculated

        weight_by_elements: bool
            Whether fingerprint is weighted by the numbers of
            atoms of different elements
        '''

        default_parameters = {'r_cutoff': 8.0,
                              'r_delta': 0.4,
                              'r_nbins': 200}

        self.params = default_parameters.copy()
        self.params.update(kwargs)

        self.calc_gradients = calc_gradients
        self.weight_by_elements = weight_by_elements

        # parameters in this class for constructing the fingerprint:
        self.param_names = ['r_cutoff', 'r_delta', 'r_nbins']

        self.atoms = atoms.copy()
        self.atoms.wrap()

        self.pairs = AtomPairs(self.atoms,
                               self.params['r_cutoff'])

        fpparams = dict(pairs=self.pairs,
                        cutoff=self.params['r_cutoff'],
                        width=self.params['r_delta'],
                        nbins=self.params['r_nbins'],
                        weight_by_elements=self.weight_by_elements)

        self.rho_R = RadialFPCalculator.calculate(**fpparams)
        self.vector = self.rho_R.flatten()

        self.gradients = (RadialFPGradientCalculator.
                          calculate(natoms=self.natoms, **fpparams)
                          if self.calc_gradients else None)

    @property
    def natoms(self):
        return len(self.atoms)

    def recalculate(self, calc_gradients=None):
        '''
        Re-calculate the fingerprint vector and the gradients.
        '''
        calc_gradients = (self.calc_gradients if calc_gradients is None
                          else calc_gradients)

        self.__init__(self.atoms, calc_gradients=calc_gradients,
                      weight_by_elements=self.weight_by_elements,
                      **self.params)

    def reduce_coord_gradients(self):
        '''
        Reshape gradients by flattening the element-to-element
        contributions.
        '''
        return self.gradients.reshape(self.natoms, -1, 3)


class RadialAngularFP(RadialFP):

    def __init__(self, atoms, calc_gradients=True,
                 weight_by_elements=True, **kwargs):
        ''' Parameters:

        a_cutoff: float
                Threshold for angular fingerprint (Angstroms)

        a_delta: float
                Width of Gaussian broadening in angular fingerprint
               (Radians)

        a_nbins: int
            Number of bins in angular fingerprint

        aweight: float
            Scaling factor for the angular fingerprint; the angular
            fingerprint is multiplied by this number

        '''
        RadialFP.__init__(self, atoms, calc_gradients=calc_gradients,
                          weight_by_elements=weight_by_elements, **kwargs)

        default_parameters = {'r_cutoff': 8.0,
                              'r_delta': 0.4,
                              'r_nbins': 200,
                              'a_cutoff': 4.0,
                              'a_delta': 0.4,
                              'a_nbins': 100,
                              'gamma': 0.5,
                              'aweight': 1.0}

        self.params = default_parameters.copy()
        self.params.update(kwargs)

        # parameters in this class for constructing the fingerprint:
        self.param_names = ['r_cutoff', 'r_delta', 'r_nbins',
                            'a_cutoff', 'a_delta', 'a_nbins',
                            'aweight']

        assert self.params['r_cutoff'] >= self.params['a_cutoff']

        self.triples = AtomTriples(self.atoms,
                                   cutoff=self.params['r_cutoff'],
                                   cutoff2=self.params['a_cutoff'])

        fpparams = dict(triples=self.triples,
                        cutoff=self.params['a_cutoff'],
                        width=self.params['a_delta'],
                        nbins=self.params['a_nbins'],
                        aweight=self.params['aweight'],
                        gamma=self.params['gamma'],
                        weight_by_elements=self.weight_by_elements)

        self.rho_a = RadialAngularFPCalculator.calculate(**fpparams)
        self.vector = np.concatenate((self.rho_R.flatten(),
                                      self.rho_a.flatten()), axis=None)

        calc_gradients = (self.calc_gradients if calc_gradients is None
                          else calc_gradients)

        self.anglegradients = (RadialAngularFPGradientCalculator.
                               calculate(natoms=self.natoms,
                                         **fpparams)
                               if calc_gradients else None)

    def reduce_coord_gradients(self):
        '''
        Reshape gradients by flattening the element-to-element
        contributions and all angles, and concatenate those arrays.
        '''
        return np.concatenate((self.gradients.reshape(self.natoms, -1, 3),
                               self.anglegradients.reshape(self.natoms, -1, 3)),
                              axis=1)

    @staticmethod
    def get_fit_aweight(fps):
        '''
        Calculate the ratios between radial and angular parts of the
        fingerprints listed in 'fps', and return the mean of all
        ratios, in order to get a reasonable value for 'aweight'.
        '''
        rad_ang_ratios = []
        for fp in fps:
            if fp.triples.empty:
                continue
            rad_ang_ratios.append(fp.params['aweight'] *
                            fp.rho_R.flatten().sum() /
                            fp.rho_a.flatten().sum())
        return np.mean(rad_ang_ratios)


class RadialFPCalculator:

    @staticmethod
    def constant(cutoff, nbins):
        return 1 / (cutoff / nbins)

    @staticmethod
    def get_rvec(cutoff, nbins, startpad=-1.0, endpad=2.0):
        ''' Variable array

        Parameters:
        cutoff: float (Angstroms)
        nbins: int
        startpad: float (Angstroms)
            Extension of the fingerprint vector below zero
        endpad: float (Angstroms)
            Extension of the fingerprint vector above cutoff
        '''
        return np.linspace(startpad, cutoff + endpad, nbins)

    @classmethod
    def get_diffvec(self, pairs, cutoff, nbins):
        ''' Distances on variable array '''
        return self.get_rvec(cutoff, nbins) - pairs.dm[:, np.newaxis]

    @classmethod
    def get_peak_heights(self, pairs, cutoff, nbins):
        '''
        Peak heights for each Gaussian in the fingerprint.
        Contains 1/r**2 term and the cutoff function.
        '''
        if pairs.empty:
            return []

        return self.constant(cutoff, nbins) * (1 / pairs.dm**2 +
                                               2 / cutoff**3 * pairs.dm -
                                               3 / cutoff**2)

    @classmethod
    def get_gs(self, pairs, width, cutoff, nbins):
        '''
        Gaussian for at each r_ij (distance between atoms)
        '''
        return np.exp(- self.get_diffvec(pairs, cutoff, nbins)**2 /
                      2 / width**2)

    @classmethod
    def calculate(self, pairs, cutoff, width, nbins,
                  weight_by_elements=False):
        '''
        Calculate the Gaussian-broadened fingerprint.
        '''

        if pairs.empty:
            return np.zeros([pairs.elem.nelem, pairs.elem.nelem, nbins])

        # Gaussians with correct heights:
        gs = self.get_gs(pairs=pairs,
                         width=width,
                         cutoff=cutoff,
                         nbins=nbins)
        gs *= self.get_peak_heights(pairs=pairs,
                                    cutoff=cutoff,
                                    nbins=nbins)[:, np.newaxis]

        # Sum Gaussians to correct element-to-element pairs:
        rho_R = FPTools.sum_in_groups(values=gs,
                                      indexlist=pairs.elem.indices,
                                      nelem=pairs.elem.nelem)

        if weight_by_elements:
            rho_R = FPTools.get_array_weighted_by_elements(rho_R, pairs=pairs)

        return rho_R


class RadialFPGradientCalculator(RadialFPCalculator):

    @classmethod
    def get_peak_height_gradients(self, pairs, cutoff, nbins):
        return (self.constant(cutoff, nbins) *
                (-2 / pairs.dm**3 + 2 / cutoff**3))

    @classmethod
    def get_gradient_gaussians(self, pairs, cutoff, nbins, width):
        '''
        Gradients of h * exp() for each atom pair in pairs.indices.
        '''
        return ((- self.get_peak_height_gradients(pairs, cutoff, nbins)[:, np.newaxis]
                 - self.get_diffvec(pairs, cutoff, nbins)
                 * self.get_peak_heights(pairs, cutoff, nbins)[:, np.newaxis]
                 / width**2)
                / pairs.dm[:, np.newaxis]
                * self.get_gs(pairs, width, cutoff, nbins))

    @classmethod
    def calculate(self, natoms, pairs, cutoff,
                  width, nbins, weight_by_elements=False):

        gradients = np.zeros([natoms, pairs.elem.nelem,
                              pairs.elem.nelem, nbins, 3])

        if pairs.empty:
            return gradients

        # results shape: (npairs, nbins, 3)
        results = np.einsum('ij,ik->ijk',
                            self.get_gradient_gaussians(pairs, cutoff,
                                                        nbins, width),
                            -pairs.rm,
                            optimize=True)

        for p in range(len(pairs.indices)):
            i, j = pairs.indices[p]
            A, B = pairs.elem.indices[p]

            gradients[i, A, B] += results[p]
            gradients[j % natoms, A, B] += -results[p]

        if weight_by_elements:
            gradients = np.moveaxis(gradients, 0, 2)  # reorganize
            gradients = FPTools.get_array_weighted_by_elements(gradients,
                                                               pairs=pairs,
                                                               dim=2)
            gradients = np.moveaxis(gradients, 2, 0)  # back-reorganize

        return gradients


class FPTools:

    @staticmethod
    def get_array_weighted_by_elements(array, pairs, dim=2):
        '''
        dim==2:
        array has shape of (N_elements, N_elements, nbins). This method
        divides each (N_elements, N_elements) sub-array with the numbers
        of atoms of different elements, respectively for each sub-array.

        dim==3:
        array has shape of (N_elements, N_elements, N_elements, nbins).
        This method divides each (N_elements, N_elements, N_elements)
        sub-array with the numbers of atoms of different elements,
        respectively for each sub-array.
        '''
        if dim == 2:
            subscripts1 = 'i,j->ij'
            subscripts2 = 'ijk...,ij->ijk...'

        elif dim == 3:
            subscripts1 = 'i,j,k->ijk'
            subscripts2 = 'ijlk...,ijl->ijlk...'

        else:
            raise RuntimeError('Bad number of dimensions.'
                               ' (dim=={})'.format(dim))

        factortable = np.einsum(subscripts1,
                                *(dim * [pairs.elem.counts])
                                ).astype(float)**-1

        return np.einsum(subscripts2, array,
                         factortable, optimize=True)

    @staticmethod
    def sum_in_groups(values, indexlist, nelem):
        '''
        Speeds up this code:

            for i, (A, B) in enumerate(indexlist):
                self.rho_R[A, B] += values[i]

        '''

        dim = len(indexlist[0])

        # get all possible combinations in keys:
        combinations = [range(nelem)] * dim
        keys = list(itertools.product(*combinations))

        # compare each index group to keys:
        indices = (keys == indexlist[:, np.newaxis])

        # choose only rows where all indices match:
        indices = (indices.sum(axis=2) == dim)

        # calculate:
        result = np.einsum('ij,ik->jk', indices, values, optimize=True)

        # reshape:
        result = result.reshape(*(dim * [nelem]), -1)

        return result


class RadialAngularFPCalculator:

    @staticmethod
    def angleconstant(aweight, nbins):
        return aweight / (pi / nbins)

    @staticmethod
    def get_thetavec(nbins, startpad=-0.5 * pi, endpad=0.5 * pi):
        '''
        Parameters:
        nbins: int
        startpad: float (rads)
            Extension of the fingerprint vector below zero
        endpad: float (rads)
            Extension of the fingerprint vector above cutoff
        '''
        return np.linspace(startpad, pi + endpad, nbins)

    @staticmethod
    def cutoff_function(dist_array, cutoff, gamma):
        '''
        Calculate cutoff function for each distance in the input
        array `dist_array`
        '''

        return np.where(dist_array <= cutoff,
                        (1 + gamma *
                         (dist_array / cutoff)**(gamma + 1) -
                         (gamma + 1) *
                         (dist_array / cutoff)**gamma), 0.0)

    @classmethod
    def fcij(self, triples, cutoff, gamma):
        return self.cutoff_function(triples.adm, cutoff, gamma=gamma)

    @classmethod
    def fcjk(self, triples, cutoff, gamma):
        return self.cutoff_function(triples.edm, cutoff, gamma=gamma)

    @classmethod
    def get_ags(self, triples, width, nbins, aweight):
        ''' Angle gaussians '''
        return (self.angleconstant(aweight, nbins) *
                np.exp(- (self.get_thetavec(nbins) -
                          triples.thetas[:, np.newaxis])**2 /
                       2 / width**2))

    @classmethod
    def get_cutoff_ags(self, triples, cutoff, width, nbins, aweight, gamma):
        '''
        Angle gaussians multiplied by the cutoff functions
        '''
        return (self.fcij(triples, cutoff, gamma)[:, np.newaxis] *
                self.fcjk(triples, cutoff, gamma)[:, np.newaxis] *
                self.get_ags(triples, width, nbins, aweight))

    @classmethod
    def calculate(self, triples, cutoff, width, nbins, aweight,
                  gamma, weight_by_elements=False):
        ''' Calculate the angular fingerprint with Gaussian broadening  '''

        if triples.empty:
            rho_a = np.zeros([triples.elem.nelem, triples.elem.nelem,
                              triples.elem.nelem, nbins])
            return rho_a

        # Gaussians with correct height:
        gs = self.get_cutoff_ags(triples, cutoff, width, nbins, aweight, gamma)

        # Sum Gaussians to correct element-to-element-to-element angles:
        rho_a = FPTools.sum_in_groups(values=gs,
                                      nelem=triples.elem.nelem,
                                      indexlist=triples.elem.indices)

        if weight_by_elements:
            rho_a = FPTools.get_array_weighted_by_elements(rho_a, pairs=triples, dim=3)

        return rho_a


class RadialAngularFPGradientCalculator(RadialAngularFPCalculator):

    @classmethod
    def nabla_fcij(self, triples, cutoff, gamma):
        return self.nabla_fc(dist_array=triples.adm,
                             rvec_array=triples.arm,
                             cutoff=cutoff,
                             gamma=gamma)

    @classmethod
    def nabla_fcjk(self, triples, cutoff, gamma):
        return self.nabla_fc(dist_array=triples.edm,
                             rvec_array=-triples.erm,
                             cutoff=cutoff,
                             gamma=gamma)

    @staticmethod
    def nabla_fc(dist_array, rvec_array, cutoff, gamma):
        dfc_dd = (gamma * (gamma + 1) / cutoff *
                  ((dist_array / cutoff) ** gamma -
                   (dist_array / cutoff) ** (gamma - 1)))
        dd_drm = np.einsum('ij,i->ij', rvec_array, dist_array**-1)
        return np.einsum('i,ij->ij', dfc_dd, dd_drm)

    @classmethod
    def dthetaijk_dri(self, triples):
        return (self.dtheta_prefactors(triples)[:, np.newaxis] *
                (self.dtheta_factor1(triples) - triples.erm))

    @classmethod
    def dthetaijk_drj(self, triples):
        first = self.dtheta_factor1(triples) - triples.arm
        second = self.dtheta_factor2(triples) - triples.erm
        return (-self.dtheta_prefactors(triples)[:, np.newaxis] *
                (first + second))

    @classmethod
    def dthetaijk_drk(self, triples):
        return (-self.dtheta_prefactors(triples)[:, np.newaxis] *
                (triples.arm - self.dtheta_factor2(triples)))

    @classmethod
    def dtheta_factor1(self, triples):
        return (self.rm_dotp(triples)[:, np.newaxis] /
                np.square(triples.adm)[:, np.newaxis] * triples.arm)

    @classmethod
    def dtheta_factor2(self, triples):
        return (self.rm_dotp(triples)[:, np.newaxis] /
                np.square(triples.edm)[:, np.newaxis] * triples.erm)

    @staticmethod
    def rm_dotp(triples):
        return np.einsum('ij,ij->i', triples.arm, triples.erm)

    @staticmethod
    def dtheta_prefactors(triples):
        return (np.abs(np.sin(triples.thetas)) *
                triples.adm * triples.edm)**-1

    @classmethod
    def calculate(self, natoms, triples, cutoff, width, nbins, aweight,
                  gamma, weight_by_elements=False):

        gradients = np.zeros([natoms, triples.elem.nelem, triples.elem.nelem,
                              triples.elem.nelem, nbins, 3])

        if triples.empty:
            return gradients

        firsts, seconds, thirds = self.do_anglegradient_math(triples, cutoff,
                                                             width, nbins,
                                                             aweight, gamma)

        # Add the precalculated arrays to correct element contributions:
        for p in range(len(triples.indices)):
            i, j, k = triples.indices[p]
            A, B, C = triples.elem.indices[p]

            gradients[i, A, B, C] += firsts[p]
            gradients[j % natoms, A, B, C] += seconds[p]
            gradients[k % natoms, A, B, C] += thirds[p]

        if weight_by_elements:
            gradients = np.moveaxis(gradients, 0, 3)  # reorganize
            gradients = FPTools.get_array_weighted_by_elements(gradients,
                                                               pairs=triples,
                                                               dim=3)
            gradients = np.moveaxis(gradients, 3, 0)  # back-reorganize

        return np.array(gradients)

    @classmethod
    def do_anglegradient_math(self, triples, cutoff, width,
                              nbins, aweight, gamma):
        '''
        Calculate arrays to be used in the angular fingerprint gradient
        calculation.
        '''
        diffvecs = np.subtract.outer(self.get_thetavec(nbins), triples.thetas).T
        ags = self.get_ags(triples, width, nbins, aweight)
        fcij = self.fcij(triples, cutoff, gamma)
        fcjk = self.fcjk(triples, cutoff, gamma)

        firstvalues = (fcjk[:, np.newaxis, np.newaxis] *
                       np.einsum('ij,ik->ijk', ags,
                                 self.nabla_fcij(triples, cutoff, gamma)))

        secondvalues = (fcij[:, np.newaxis, np.newaxis] *
                        np.einsum('ij,ik->ijk', ags,
                                  self.nabla_fcjk(triples, cutoff, gamma)))

        thirdinits = (fcij[:, np.newaxis] *
                      fcjk[:, np.newaxis] *
                      diffvecs / width**2 * ags)

        third_i = np.einsum('ij,ik->ijk', thirdinits, self.dthetaijk_dri(triples))
        third_j = np.einsum('ij,ik->ijk', thirdinits, self.dthetaijk_drj(triples))
        third_k = np.einsum('ij,ik->ijk', thirdinits, self.dthetaijk_drk(triples))

        firsts = firstvalues + third_i
        seconds = -firstvalues + secondvalues + third_j
        thirds = -secondvalues + third_k

        return firsts, seconds, thirds


class AtomsExtender:

    def __init__(self, atoms, cutoff, cutoff2=None):
        '''
        Extend the unit cell so that all the atoms within the cutoff
        are in the same cell, indexed properly. The extended atoms are
        stored in Atoms object extendedatoms. The original atoms
        in a unit cell that matches the extended atoms is stored in
        primaryatoms.

        Parameters:
        atoms: Atoms object to extend
        cutoff: cutoff value in Angstroms
        cutoff2: secondary cutoff value in Angstroms to be used with
                 triples
        '''

        natoms = len(atoms)

        # Number of cells needed to consider given the limit and pbc:
        nx, ny, nz = AtomsExtender.get_ext_factors(atoms, cutoff, cutoff2)

        self.extendedatoms = atoms.repeat([nx, ny, nz])

        newstart = natoms * int(np.prod([nx, ny, nz]) / 2)
        newend = newstart + natoms
        self.primaryatoms = self.extendedatoms[newstart:newend]

    @staticmethod
    def get_ext_factors(atoms, cutoff, cutoff2):
        '''
        Return nx, ny, nz as the numbers of extended cells in each
        direction, needed to consider the given limit and pbc.
        '''
        ncells = AtomsExtender.get_ncells(atoms, cutoff, cutoff2)
        nx, ny, nz = [1 + 2 * int(n) * atoms.pbc[i]
                      for i, n in enumerate(ncells)]
        return nx, ny, nz

    @staticmethod
    def get_ncells(atoms, cutoff, cutoff2):
        ''' Return number of cells to consider due to periodic
        boundary conditions '''

        AtomsExtender.check_cell(atoms)

        # Determine unit cell parameters:
        lengths = atoms.cell.lengths()
        ncells = [cutoff // lengths[i] + 1 for i in range(3)]

        if cutoff2 is None:
            return ncells

        ncells2 = [(2 * cutoff2) // lengths[i] + 1
                   for i in range(3)]

        return [max(ncells[i], ncells2[i]) for i in range(3)]

    @staticmethod
    def check_cell(atoms):
        if atoms.cell.rank != 3:
            raise ValueError('Atoms object has to have a 3D unit cell.')


class AtomPairs:

    def __init__(self, atoms, cutoff):
        '''
        Resolve indices between which the distances are considered
        in the fingerprint.

        Store information for pair indices, elements, distances and
        dislocation vectors.
        '''
        extender = AtomsExtender(atoms, cutoff)

        ap = extender.primaryatoms.positions
        ep = extender.extendedatoms.positions
        self.indices = AtomPairs.get_pair_index_list(ap, ep, cutoff)
        self.rm = []
        self.dm = []

        if len(self.indices) > 0:

            # vectors between positions:
            self.rm = (ap[self.indices[:, 0]] -
                       ep[self.indices[:, 1]])

            # distances between positions:
            self.dm = np.linalg.norm(self.rm, axis=1)

        self.elem = FPElements(atoms1=extender.primaryatoms,
                               atoms2=extender.extendedatoms,
                               indices=self.indices)

    @staticmethod
    def get_pair_index_list(pos1, pos2, cutoff):
        '''
        Returns a list of pairs of atom indices for atoms that are
        within the cutoff radius.

        Parameters:
        pos1: position matrix (N, 3)
        pos2: position matrix (N, 3)
        cutoff: distance beyond which an atom pair is neglected
        '''
        dm = distance_matrix(x=pos1, y=pos2)

        # Set too long distances to 0:
        dm[dm > cutoff] = 0.0

        # Indices of valid distances:
        Ai, Aj = np.nonzero(dm)

        # Return index pairs as a list:
        return np.stack((Ai, Aj)).T

    @property
    def empty(self):
        return len(self.indices) == 0


class FPElements:

    def __init__(self, atoms1, atoms2, indices):
        '''
        Store chemical element information for all the atom pairs between
        'atoms1' and 'atoms2' as given by 'indices'.
        '''
        self.atoms1 = atoms1
        self.atoms2 = atoms2

        # Store numbers of elements in atoms1:
        self.counts = self.get_elemcounts(self.atoms1)

        # Element indices for each atom pair in indices:
        self.indices = self.get_element_index_list(indices)

    @classmethod
    def get_elemcounts(self, atoms):
        '''
        Return the numbers of atoms of different elements as a list
        that is ordered in the same way as the sorted element set.
        '''
        elset = self.get_elementset(atoms)
        return [atoms.symbols.formula[elem] for elem in elset]

    @staticmethod
    def get_elementset(atoms):
        '''
        Return the different elements in 'atoms' as a sorted set.
        '''
        return sorted(atoms.symbols.species())

    @classmethod
    def get_symbols_indices(self, atoms):
        '''
        Go through atoms.symbols and store the indices of the symbols
        as they appear in element set.
        '''
        elset = self.get_elementset(atoms)
        return [elset.index(s) for s in atoms.symbols]

    def get_element_index_list(self, indices):
        '''
        For each atom pair, given by 'indices', return the indices of
        their elements as they appear in the sorted element set.
        '''
        symbols1 = FPElements.get_symbols_indices(self.atoms1)
        symbols2 = FPElements.get_symbols_indices(self.atoms2)

        # Element indices for each atom pair:
        return np.array([(symbols1[i], symbols2[j])
                         for i, j in indices], dtype=int)

    @ase.utils.lazyproperty
    def nelem(self):
        return len(self.atoms1.symbols.species())


class AtomTriples:

    def __init__(self, atoms, cutoff, cutoff2):
        '''
        Finds atom triples within cutoff, and stores the indices, elements,
        distances, dislocation vectors, and angles for each triple.

        Parameters:
        atoms: Atoms object to consider
        cutoff: cutoff value (Angstroms) for the radial part
        cutoff2: secondary cutoff value for the angular part

        About cutoff values: The radial cutoff value is only used in
        determining the proper extended unit cell size for systems with
        periodic boundary conditions. The extended unit cell has to be
        large enough to reach the 'cutoff' value and 2 times 'cutoff2'
        value from the primary unit cell. The reach of 2x'cutoff2'
        comes from the fact that an angle can reach from an atom in the
        primary cell to another one in extended cell with a total distance
        of 2x'cutoff2'.
        '''

        extender = AtomsExtender(atoms, cutoff=cutoff, cutoff2=cutoff2)

        self.primaryatoms = extender.primaryatoms
        self.extendedatoms = extender.extendedatoms

        ap = self.primaryatoms.positions
        ep = self.extendedatoms.positions

        self.indices = self.get_angle_index_list(ap, ep, cutoff2)

        if len(self.indices) > 0:

            # vectors from primary atoms to extended atoms:
            self.arm = ap[self.indices[:, 0]] - ep[self.indices[:, 1]]

            # vectors from extended atoms to extended atoms
            self.erm = ep[self.indices[:, 2]] - ep[self.indices[:, 1]]

            # distances between primary atoms and extended atoms:
            self.adm = np.linalg.norm(self.arm, axis=1)

            # distances between extended atoms and extended atoms:
            self.edm = np.linalg.norm(self.erm, axis=1)

            # arccos arguments for each angle:
            args = (np.einsum('ij,ij->i', self.arm, self.erm)
                    / self.adm / self.edm)

            # Take care of numerical errors:
            args = np.where(args >= 1.0, 1.0 - 1e-12, args)
            args = np.where(args <= -1.0, -1.0 + 1e-12, args)

            # Angles:
            self.thetas = np.arccos(args)

        self.elem = FPElementsForTriples(atoms1=self.primaryatoms,
                                         atoms2=self.extendedatoms,
                                         indices=self.indices)

    @staticmethod
    def get_angle_index_list(pos1, pos2, cutoff):
        '''
        Get list of atom indices between which an angle is
        considered in the fingerprint.
        '''

        # Extended distance and displacement vector matrices:
        dm = distance_matrix(pos1, pos2)
        edm = distance_matrix(pos2, pos2)

        # Set too long distances to 0.0:
        dm[dm > cutoff] = 0.0
        edm[edm > cutoff] = 0.0

        # Indices of valid distances:
        Ai, Aj = np.nonzero(dm)
        Bj, Bk = np.nonzero(edm)

        # Indices where the j-indices match:
        matches = np.nonzero(np.equal.outer(Aj, Bj))

        # Combine i,j,k-indices:
        indices = np.stack((Ai[matches[0]],
                            Aj[matches[0]],
                            Bk[matches[1]])).T

        # Remove triples where i and k index refer to the same atom:
        start = int(len(pos2) / len(pos1) / 2) * len(pos1)
        indices = indices[(indices[:, 2] - start) != indices[:, 0]]
        return indices

    @property
    def empty(self):
        return len(self.indices) == 0


class FPElementsForTriples(FPElements):
    '''
    Element information storage class for atom triples.
    '''
    def get_element_index_list(self, indices):
        '''
        For each atom triple, given by 'indices', return the indices of
        their elements as they appear in the sorted element set.
        '''
        symbols1 = self.get_symbols_indices(self.atoms1)
        symbols2 = self.get_symbols_indices(self.atoms2)

        return np.array([(symbols1[i],
                          symbols2[j],
                          symbols2[k])
                         for i, j, k in indices], dtype=int)


class CartesianCoordFP:

    def __init__(self, atoms, **kwargs):
        ''' Null fingerprint where the fingerprint vector is
        merely the flattened atomic coordinates. '''

        self.params = {}
        self.param_names = []

        self.atoms = atoms
        self.vector = self.atoms.get_positions(wrap=False).reshape(-1)
        self.gradients = self.calculate_gradients()

    def recalculate(self):
        self.__init__(atoms=self.atoms)

    @property
    def natoms(self):
        return len(self.atoms)

    def calculate_gradients(self):
        gradients = np.eye(self.natoms * 3)
        gradients = gradients.reshape(self.natoms, -1, 3, order='F')
        return gradients

    def reduce_coord_gradients(self):
        return self.gradients.reshape(self.natoms, -1, 3)
