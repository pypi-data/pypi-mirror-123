import time

import numpy as np
from ase.build import fcc111

from gpatom.gpfp.fingerprint import RadialAngularFP
from gpatom.gpfp.kernel import SquaredExp, Matern, RationalQuad
import pytest

@pytest.mark.parametrize('kernel_class', [SquaredExp, Matern, RationalQuad])
def test_kernelhessian(kernel_class):
    '''
    Test that the Hessian of the squared exponential kernel,
    using the fingerprint, matches with the numerical one.
    '''

    params = dict(limit=4.0, Rlimit=3.0, delta=0.4)

    def new_fp(atoms):
        return RadialAngularFP(atoms=atoms, **params)

    def print_matrix(matrix):
        print()
        for row in matrix:
            for val in row:
                print('{:12.06f}'.format(val), end='')
            print()
        print()

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
    t0 = time.time()
    hessian = np.zeros([3, 3])
    for cc1 in range(3):
        for cc2 in range(3):

            change1, change2 = np.zeros(3), np.zeros(3)
            change1[cc1] = dx
            change2[cc2] = dx

            atoms1 = slab.copy()
            atoms1.rattle(0.01, seed=1)
            fp1 = new_fp(atoms1)

            atoms2 = atoms1.copy()
            atoms2[index1].position += change1
            fp2 = new_fp(atoms2)

            atoms3 = atoms1.copy()
            atoms3.rattle(0.02, seed=2)
            fp3 = new_fp(atoms3)

            atoms4 = atoms3.copy()
            atoms4[index2].position += change2
            fp4 = new_fp(atoms4)

            hessian[cc1, cc2] = (((k.kernel(fp2, fp4) -
                                   k.kernel(fp2, fp3)) -
                                  (k.kernel(fp1, fp4) -
                                   k.kernel(fp1, fp3)))
                                 / dx**2)
    print('Numerical:')
    print_matrix(hessian)
    print('Time consumed:', (time.time() - t0), 'seconds\n')

    # Analytical:
    t0 = time.time()
    atoms1 = slab.copy()
    atoms1.rattle(0.01, seed=1)
    fp1 = new_fp(atoms1)
    atoms3 = atoms1.copy()
    atoms3.rattle(0.02, seed=2)
    fp3 = new_fp(atoms3)
    analytical = k.kernel_hessian(fp1, fp3)[index1, index2]

    print('Analytical:')
    print_matrix(analytical)
    print('Time consumed:', (time.time() - t0), 'seconds\n')


    rtol = 1e-2
    atol = 1e-8
    assert(np.allclose(hessian, analytical,
                       rtol=rtol, atol=atol))
    txt = 'Kernel Hessians match with relative '
    txt += 'tolerance {}. OK!'.format(rtol)
    print(txt)

