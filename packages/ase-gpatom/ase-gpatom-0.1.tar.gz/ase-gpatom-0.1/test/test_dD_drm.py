import time
import numpy as np
from ase.build import fcc100
from gpatom.gpfp.fingerprint import RadialAngularFP
from gpatom.gpfp.kerneltypes import EuclideanDistance

import pytest


@pytest.mark.parametrize('distance_class', [EuclideanDistance])
def test_dD_drm(distance_class):
    '''
    Test that the implemented derivative of the distance w.r.t.
    an atom coordinate matches with the numerical one.
    '''

    def new_fp(atoms):
        return RadialAngularFP(atoms=atoms,
                               r_cutoff=4.0,
                               a_cutoff=3.0,
                               scale=6,
                               aweight=0.1,
                               calc_gradients=True)


    # Create slab:
    slab = fcc100('Ag', size=(2, 2, 2))
    slab[-4].symbol = 'Au'
    slab[-2].symbol = 'Au'
    slab.center(axis=2, vacuum=4.0)
    slab.rattle(0.05)

    fp = new_fp(slab)

    index1 = 5
    index2 = 6

    dx = 0.00001

    # Numerical:
    t0 = time.time()
    dD_drm = np.zeros([3])
    for cc1 in range(3):

            change1 = np.zeros(3)
            change1[cc1] = dx

            atoms1 = slab.copy()
            atoms1.rattle(0.01, seed=1)
            fp1 = new_fp(atoms1)

            atoms2 = atoms1.copy()
            atoms2[index1].position += change1
            fp2 = new_fp(atoms2)

            atoms3 = atoms1.copy()
            atoms3.rattle(0.02, seed=2)
            fp3 = new_fp(atoms3)

            dD_drm[cc1] = (distance_class.distance(fp2, fp3) -
                           distance_class.distance(fp1, fp3)) / dx

    print('\nNumerical:\n', dD_drm, '\nTime consumed:',
          (time.time() - t0), 'seconds\n')

    # Analytical:
    t0 = time.time()

    atoms1 = slab.copy()
    atoms1.rattle(0.01, seed=1)
    fp1 = new_fp(atoms1)

    atoms3 = atoms1.copy()
    atoms3.rattle(0.02, seed=2)
    fp3 = new_fp(atoms3)

    analytical = distance_class.dD_drm(fp1, fp3)[index1]
    print('\nAnalytical:\n', analytical, '\nTime consumed:',
          (time.time() - t0), 'seconds\n')

    assert np.allclose(analytical, dD_drm, rtol=5e-3)
