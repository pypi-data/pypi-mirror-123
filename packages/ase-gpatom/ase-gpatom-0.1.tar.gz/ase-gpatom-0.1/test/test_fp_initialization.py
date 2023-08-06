import pytest
from gpatom.gpfp.fingerprint import RadialAngularFP
from ase import Atoms
import numpy as np

def test_bad_unitcell():

    positions = [[0., 0., 0.],
                 [1., 1., 1.],
                 [3., 1., 0.]]
    atoms = Atoms(['Cu'] * 3, positions=positions)
    atoms.center(vacuum=6.0, axis=2)

    with pytest.raises(ValueError):  # one unit cell vector is zero
        RadialAngularFP(atoms=atoms)
    

def test_empty_fingerprint():

    bad_positions = [[0., 0., 0.],
                     [10., 10., 10.],
                     [30., 30., 30.]]
    atoms = Atoms(['Cu'] * 3, positions=bad_positions)
    atoms.center(vacuum=6.0)

    fp = RadialAngularFP(atoms=atoms)

    # Assert everything is zero:
    assert np.count_nonzero(fp.vector) == 0
    assert np.count_nonzero(fp.gradients) == 0
    assert np.count_nonzero(fp.anglegradients) == 0
