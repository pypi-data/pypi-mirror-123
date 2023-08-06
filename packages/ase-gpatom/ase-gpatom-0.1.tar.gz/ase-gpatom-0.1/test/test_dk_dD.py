import numpy as np
from ase.build import fcc111

from gpatom.gpfp.fingerprint import RadialAngularFP
from gpatom.gpfp.kernel import SquaredExp, Matern, RationalQuad
from gpatom.gpfp.kerneltypes import EuclideanDistance
import pytest

@pytest.mark.parametrize('kernel_class', [SquaredExp, Matern, RationalQuad])
def test_dk_dD(kernel_class):
    '''
    Test that the derivative of the kernel function w.r.t. the distance
    is correct for each kernel type.
    '''

    params = dict(r_cutoff=4.0, a_cutoff=3.0)

    def new_fp(atoms):
        return RadialAngularFP(atoms=atoms, **params)

    # Create slab:
    slab = fcc111('Ag', size=(2, 2, 2))
    slab[-4].symbol = 'Au'
    slab[-2].symbol = 'Au'
    slab.center(axis=2, vacuum=4.0)
    slab.rattle(0.05)

    fp = new_fp(slab)

    index1 = 1
    index2 = 6

    dx = 0.0001

    k = kernel_class()

    # Numerical:
    atoms1 = slab.copy()
    atoms1.rattle(0.01, seed=1)
    fp1 = new_fp(atoms1)

    atoms2 = atoms1.copy()
    atoms2[index1].position += [dx, 0., 0.]
    fp2 = new_fp(atoms2)

    dk = k.kernel(fp2, fp) - k.kernel(fp1, fp)
    dD = (EuclideanDistance.distance(fp2, fp) -
          EuclideanDistance.distance(fp1, fp))
    numerical = dk / dD
    print('Numerical:', numerical)

    # Analytical:
    analytical = k.dk_dD(fp, fp1)
    print('Analytical:', analytical)

    rtol = 1e-2
    atol = 1e-8
    assert(np.allclose(numerical, analytical,
                       rtol=rtol, atol=atol))

