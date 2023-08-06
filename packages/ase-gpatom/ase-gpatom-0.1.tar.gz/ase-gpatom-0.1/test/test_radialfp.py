import copy

from ase.build import fcc100
from ase.calculators.emt import EMT

from gpatom.gpfp.fingerprint import RadialFP
from gpatom.gpfp.calculator import GPCalculator, Model


def test_radial():
    def set_structure(atoms, seed=0):
        """
        Create a copy and rattle.
        """
        newatoms = copy.deepcopy(atoms)
        newatoms.rattle(0.1, seed=seed)
        return newatoms


    # Create slab
    slab = fcc100('Ag', size=(2, 2, 2))
    slab[-1].symbol = 'Au'
    slab[-2].symbol = 'Au'
    slab.rattle(0.5)
    slab.center(vacuum=4.0)
    slab.pbc = False
    slab.calc = EMT()

    # Create Training Set
    train_images = []
    for i in range(5):
        # Alter structure and get fingerprint
        slab2 = set_structure(slab, seed=i)
        train_images.append(slab2)

    print('EMT energy: {}eV'.format(slab.get_potential_energy()))

    # Initialize fingerprint
    fp = RadialFP
    params = {'scale': 1000, 'r_delta': 0.4}
    # {'weight': 1.0, 'scale': 1000.0, 'delta': 0.2}

    model = Model(train_images=train_images,
                  params=params,
                  fingerprint=fp)
    calc = GPCalculator(model)

    slab.calc = calc

    print('GP energy: {}eV'.format(slab.get_potential_energy()))
