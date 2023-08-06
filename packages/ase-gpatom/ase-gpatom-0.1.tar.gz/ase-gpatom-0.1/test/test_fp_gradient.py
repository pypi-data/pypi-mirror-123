import pytest
from ase.build import bulk
from gpatom.gpfp.fingerprint import (RadialFP, RadialAngularFP,
                                     CartesianCoordFP)
import numpy as np

@pytest.mark.parametrize('fp_class', [RadialFP, RadialAngularFP, CartesianCoordFP])
def test_fp_derivative(fp_class, atoms=None):
    '''
    Test that the fingerprint and the calculated gradient match.
    '''

    atoms = bulk('NaCl', 'rocksalt', a=4.6)
    atoms = atoms.repeat((2, 2, 3))
    atoms.rattle(0.001, seed=12)
    atoms.pbc = False

    index = 3
    dx = 0.0001

    fpparams = dict(aweight=40.0)
    
    atoms1 = atoms.copy()
    fp1 = fp_class(atoms=atoms1, **fpparams)
    v1 = fp1.vector

    atoms2 = atoms.copy()
    atoms2[index].position += [dx, 0., 0.]
    v2 = fp_class(atoms=atoms2, **fpparams).vector

    drho_numerical = (v2 - v1) / dx

    drho_analytical = fp1.reduce_coord_gradients()[index, :, 0] # correct atom, x-component

    # plt.plot(drho_numerical)
    # plt.plot(drho_analytical)
    # plt.show()

    assert np.allclose(drho_numerical, drho_analytical, rtol=1e-3, atol=1e-4)

