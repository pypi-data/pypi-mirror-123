from ase.build import fcc100
from ase.calculators.emt import EMT
import warnings

from gpatom.gpfp.fingerprint import RadialAngularFP

from gpatom.gpfp.calculator import GPCalculator, Model, Database, copy_image
from gpatom.gpfp.prior import ConstantPrior
from gpatom.gpfp.gp import GaussianProcess


class ModifiedModel(Model):
    def __init__(self, kerneltype='sqexp', train_images=[], train_features=None,
                 prior=None, fingerprint=None,
                 params={'weight': 1., 'scale': 0.4,
                         'noise': 0.005, 'noisefactor': 0.5},
                 use_forces=True, par=True):

        prior = ConstantPrior(constant=0.0)
        self.fp = fingerprint
        train_images = [copy_image(i) for i in train_images]
        fingerprints = [self.new_fingerprint(atoms, params, use_forces)
                          for atoms in train_images]
        energies = [atoms.get_potential_energy(apply_constraint=False)
                    for atoms in train_images]
        forces = [atoms.get_forces(apply_constraint=False)
                  for atoms in train_images]
        self.data = Database(fingerprints, energies, forces)
        self.gp = GaussianProcess(hp=params, prior=prior, kerneltype=kerneltype,
                                  use_forces=use_forces, parallelkernel=par)
        self.gp = self.train_model(self.gp, self.data)


def make_prediction(parallel):
    def set_structure(atoms, seed=0):
        """
        Create a copy and rattle.
        """
        newatoms = atoms.copy()
        newatoms.rattle(0.05, seed=seed)

        newatoms.calc = EMT()
        return newatoms


    # Create atoms
    atoms = fcc100('Ag', size=(2, 2, 1))
    atoms[-1].symbol = 'Au'
    atoms[-2].symbol = 'Au'
    atoms.rattle(0.5)
    atoms.center(vacuum=4.0)
    atoms.pbc = False


    # Create Training Set
    train_images = []
    for i in range(2):
        # Alter structure and get fingerprint
        atoms2 = set_structure(atoms, seed=i)
        train_images.append(atoms2)

    atoms.calc = EMT()

    model = ModifiedModel(train_images=train_images,
                          par=parallel,
                          params={'scale': 1000},
                          fingerprint=RadialAngularFP)

    atoms.calc = GPCalculator(model)

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=UserWarning)
        e_pred = atoms.get_potential_energy()

    return e_pred


def test_kernels_sameresult():
    e1 = make_prediction(False)
    e2 = make_prediction(True)

    assert abs(e1 - e2) < 1e-6
