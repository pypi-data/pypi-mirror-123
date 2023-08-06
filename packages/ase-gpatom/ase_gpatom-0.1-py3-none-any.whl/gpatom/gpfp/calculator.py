import warnings
from copy import copy

import numpy as np
from ase.calculators.calculator import Calculator, all_changes
from ase.calculators.singlepoint import SinglePointCalculator

from gpatom.gpfp.fingerprint import CartesianCoordFP
from gpatom.gpfp.gp import GaussianProcess
from gpatom.gpfp.kerneltypes import EuclideanDistance


def copy_image(atoms):
    '''
    Copy an image, so that it is suitable as a training set point.
    It returns a copy of the atoms object with the single point
    calculator attached
    '''
    # Check if the input already has the desired format
    if atoms.calc.__class__.__name__ == 'SinglePointCalculator':
        # Return a copy of the atoms object
        calc = copy(atoms.calc)
        atoms0 = atoms.copy()

    else:
        # Check if the atoms object has energy and forces calculated for
        # this position
        # If not, compute them
        atoms.get_forces()

        # Initialize a SinglePointCalculator to store this results
        calc = SinglePointCalculator(atoms, **atoms.calc.results)

    atoms0 = atoms.copy()
    atoms0.calc = calc
    return atoms0


class Model:
    '''
    GP model parameters
    -------------------
    train_images: list
        List of Atoms objects containing the observations which will be use
        to train the model.

    train_features: list
        List of pre-calculated fingerprints for each structure in
        train_images

    prior: Prior object or None
        Prior for the GP regression of the PES surface. See
        ase.optimize.activelearning.prior. If *Prior* is None, then it is set
        as the ConstantPrior with the constant being updated using the
        update_prior_strategy specified as a parameter.

    kerneltype: str
        One of the possible kernel types: 'sqexp', 'matern', 'rq'

    fingerprint: Fingerprint (class name)
        Fingerprint class to be used in the model

    params: dict
        Dictionary to include all the hyperparameters for the kernel and
        for the fingerprint

    use_forces: bool
        Whether to train the GP on forces

    '''

    def __init__(self, train_images=[], train_features=None,
                 prior=None, kerneltype='sqexp', fingerprint=None,
                 params={'weight': 1., 'scale': 0.4,
                         'noise': 0.005, 'noisefactor': 0.5},
                 use_forces=True):

        if fingerprint is None:
            fingerprint = CartesianCoordFP
        self.fp = fingerprint

        # Initialize training set
        train_images = [copy_image(i) for i in train_images]

        # train_features can be input if they are already calculated.
        # Otherwise, calculate them now:
        if train_features is None:
            train_features = [self.new_fingerprint(atoms, params, use_forces)
                              for atoms in train_images]
        fingerprints = train_features

        # Training data:
        energies = [atoms.get_potential_energy(apply_constraint=False)
                    for atoms in train_images]
        forces = [atoms.get_forces(apply_constraint=False)
                  for atoms in train_images]

        self.data = Database(fingerprints, energies, forces)

        self.gp = GaussianProcess(hp=params, prior=prior,
                                  kerneltype=kerneltype,
                                  use_forces=use_forces)

        self.gp = self.train_model(self.gp, self.data)

    def new_fingerprint(self, atoms, params=None, calc_gradients=True):
        '''
        Compute a fingerprint of 'atoms' with given parameters.
        '''
        if params is None:
            params = self.gp.hp

        return self.fp(atoms=atoms, calc_gradients=calc_gradients,
                       **params)

    def add_training_points(self, train_images, data=None):
        '''
        Calculate fingerprints and add features and corresponding targets
        to the database of 'data'.
        '''
        if data is None:
            data = self.data

        for im in train_images:
            image = copy_image(im)
            fp = self.new_fingerprint(image)
            data.add(fp, image.get_potential_energy(apply_constraint=False),
                     image.get_forces(apply_constraint=False))

    def train_model(self, gp, data):
        '''
        Train a Gaussian process with given data.

        Parameters
        ----------
        gp : GaussianProcess instance
        data : Database instance

        Return a trained GaussianProcess instance
        '''

        if self.gp.use_forces:
            targets = data.get_all_energyforces()
        else:
            targets = data.energylist
        features = data.get_all_fingerprints()

        gp.train(features, targets)

        return gp

    def calculate(self, fp, get_variance=True):
        '''
        Calculate energy, forces and uncertainty for the given
        fingerprint. If get_variance==False, variance is returned
        as None.
        '''
        return self.gp.predict(fp, get_variance=get_variance)


class Database:

    def __init__(self, fingerprints=tuple(), energies=tuple(),
                 forces=tuple()):

        if not (len(fingerprints) == len(energies) == len(forces)):
            raise ValueError('Length of all input data do not match.')

        self.fingerprintlist = list(fingerprints)
        self.energylist = list(energies)
        self.forceslist = list(forces)

    def __eq__(self, db):
        if len(self) != len(db):
            return False

        # Compare distances of fingerprints:
        for i in range(len(self)):
            for j in range(len(self)):
                fp1 = self.fingerprintlist[i]
                fp2 = db.fingerprintlist[i]
                if EuclideanDistance(fp1, fp2) < 1e-4:
                    return False

        return True

    def __len__(self):
        '''
        Return number of data points in the database.
        '''
        return len(self.fingerprintlist)

    def copy(self):
        return Database(self.fingerprintlist, self.energylist,
                        self.forceslist)

    def add(self, fingerprint, energy, forces):
        '''
        Add data to database.
        '''
        self.fingerprintlist.append(fingerprint)
        self.energylist.append(energy)
        self.forceslist.append(forces)

    def get_energyforce_array(self, index, negative_forces=True):
        '''
        Return a list where the first element is energy, and
        the last element is forces for the given index.
        '''
        factor = -1 if negative_forces else 1
        return ([self.energylist[index]] +
                list(factor * self.forceslist[index].flatten()))

    def get_all_fingerprints(self):
        return self.fingerprintlist

    def get_all_energyforces(self, negative_forces=True):
        '''
        Return all energies and forces, ordered as
        [e1, f11x, f11y, f11z, f12x, f12y, ...f1Nz, e2, f21x, f21y,
        f21z, f22x, f22y, ...]
        '''
        listofall = []
        for i in range(len(self.energylist)):
            listofall += self.get_energyforce_array(
                i,
                negative_forces=negative_forces
            )
        return listofall


class GPCalculator(Calculator):

    implemented_properties = ['energy', 'forces', 'uncertainty']
    nolabel = True

    def __init__(self, model, calculate_uncertainty=True):

        Calculator.__init__(self)

        self.model = model
        self.calculate_uncertainty = calculate_uncertainty

    def calculate(self, atoms=None,
                  properties=['energy', 'forces', 'uncertainty'],
                  system_changes=all_changes):
        '''
        Calculate the energy, forces and uncertainty on the energies for a
        given Atoms structure. Predicted energies can be obtained by
        *atoms.get_potential_energy()*, predicted forces using
        *atoms.get_forces()* and uncertainties using
        *atoms.get_calculator().results['uncertainty'].
        '''
        # Atoms object.
        Calculator.calculate(self, atoms, properties, system_changes)

        model = self.model  # alias

        # Calculate fingerprint:
        x = model.new_fingerprint(self.atoms)

        # Get predictions:
        f, V = model.calculate(x, get_variance=self.calculate_uncertainty)

        # Obtain energy and forces for the given geometry.
        energy = f[0]
        forces = -f[1:].reshape(-1, 3)

        # Get uncertainty for the given geometry.
        if self.calculate_uncertainty:
            if model.gp.use_forces:
                uncertainty = V[0][0]
            else:
                uncertainty = V[0]
            if uncertainty < 0.0:
                uncertainty = 0.0
                warning = ('Imaginary uncertainty has been set to zero')
                warnings.warn(warning)
            uncertainty = np.sqrt(uncertainty)
        else:
            uncertainty = None

        # Results:
        self.results['energy'] = energy
        self.results['forces'] = forces
        self.results['uncertainty'] = uncertainty
