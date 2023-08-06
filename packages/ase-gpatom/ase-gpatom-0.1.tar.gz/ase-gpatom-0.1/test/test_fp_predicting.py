from ase.build import fcc100
from ase.calculators.emt import EMT
import warnings

from gpatom.gpfp.fingerprint import (RadialFP, RadialAngularFP)

from gpatom.gpfp.calculator import Model, GPCalculator
import pytest

@pytest.mark.parametrize('fp', [RadialFP, RadialAngularFP])
@pytest.mark.parametrize('kernel', ['sqexp', 'matern', 'rq'])
def test_prediction(fp, kernel):
    def set_structure(atoms, seed=0):
        """
        Create a copy and rattle.
        """
        newatoms = atoms.copy()
        newatoms.rattle(0.05, seed=seed)

        newatoms.calc = EMT()
        return newatoms


    # Create slab
    slab = fcc100('Ag', size=(2, 2, 2))
    slab[-1].symbol = 'Au'
    slab[-2].symbol = 'Au'
    slab.rattle(0.5)
    slab.center(vacuum=4.0)
    slab.pbc = False


    # Create Training Set
    train_images = []
    for i in range(5):
        # Alter structure and get fingerprint
        slab2 = set_structure(slab, seed=i)
        train_images.append(slab2)

    slab.calc = EMT()

    # Initialize fingerprint
    params = {'scale': 1000, 'r_delta': 0.4}

    model = Model(train_images=train_images,
                  kerneltype=kernel, params=params,
                  fingerprint=fp)

    slab.calc = GPCalculator(model)

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=UserWarning)
        e_pred = slab.get_potential_energy()

    slab.calc = EMT()
    e_real = slab.get_potential_energy()
    print()
    print('EMT energy: {:10.04f} eV'.format(e_real))
    print('GP energy: {:11.04f} eV'.format(e_pred))

    assert abs(e_pred - 10.665) < 5e-3
