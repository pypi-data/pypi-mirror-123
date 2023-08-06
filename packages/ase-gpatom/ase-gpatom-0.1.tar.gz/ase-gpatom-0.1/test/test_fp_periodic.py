import time
import numpy as np
import pytest

from ase.build import fcc111

from gpatom.gpfp.fingerprint import (RadialFP,
                                     RadialAngularFP)
from gpatom.gpfp.kerneltypes import EuclideanDistance

@pytest.mark.parametrize('fp', [RadialFP, RadialAngularFP])
def test_periodic_fingerprint(fp):
    """
    Test that fingerprint behaves as wanted with
    periodic boundary conditions, i.e. that re-centering
    atoms does not affect the fingerprint nor its gradients.
    """

    t0 = time.time()

    # Create slab:
    slab = fcc111('Ag', size=(2, 1, 2))
    slab[-4].symbol = 'Au'
    slab[-2].symbol = 'Au'
    slab.center(axis=2, vacuum=4.0)
    slab.pbc = (True, True, False)
    print("Number of atoms: ", len(slab))

    params = dict(r_cutoff=4.0, a_cutoff=3.6, r_delta=0.5, a_delta=0.2)

    fp0 = fp(atoms=slab, **params)
    vec0 = fp0.vector

    slab.positions += np.diag(slab.get_cell()) * 0.1
    fp1 = fp(atoms=slab, **params)
    vec1 = fp1.vector

    d = EuclideanDistance.distance(fp0, fp1)

    assert(d < 1e-8)

    assert(np.allclose(vec0, vec1, atol=1e-8))

    assert(np.allclose(fp0.gradients, fp1.gradients, atol=1e-8))

    if hasattr(fp0, 'anglegradients'):
        assert(np.allclose(fp0.anglegradients, fp1.anglegradients, atol=1e-8))

    t1 = time.time()
    print("time: {:.06f} sec".format(t1 - t0))
