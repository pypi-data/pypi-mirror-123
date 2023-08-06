from gpatom.beacon.str_gen import (RandomBox,
                                   RandomCluster,
                                   RandomBranch)
from ase.build.surface import fcc111
import numpy as np
from ase import Atoms
from ase.constraints import FixAtoms

def test_randombox():
    '''
    Place two silver atoms on Au(111) surface in random
    positions.
    '''

    rng = np.random.RandomState(30062021)

    atoms = fcc111('Au', size=(2, 2, 1))
    atoms.center(vacuum=6.0, axis=2)
    atoms += Atoms(['Ag'] * 2, positions=[[0., 0., 0.]] * 2)
    atoms.set_constraint(FixAtoms(indices=list(range(4))))
    
    max_z = np.max(atoms.positions[:, 2])
    sgen = RandomBox(atoms, box=[(0., 1.),
                                 (0., 1.),
                                 (max_z + 2.0, max_z + 2.2)],
                     rng=rng)
    new_atoms = sgen.get()

    assert np.allclose(new_atoms.positions[:4], atoms.positions[:4])

    assert not np.isclose(new_atoms.positions[4:6], atoms.positions[4:6]).any()

    for i in range(4, 6):
        assert new_atoms.positions[i, 2] > max_z

    assert np.linalg.norm(new_atoms.positions[4] -
                          new_atoms.positions[5]) > 1.0

def test_randomcluster():
    '''
    Insert atoms inside a small box and minimize the
    repulsive potential energy.
    '''

    rng = np.random.RandomState(30062021)
    
    atoms = Atoms(['Cu'] * 6 + ['Ag'] * 6,
                  positions=[[0., 0., 0.]] * 12)
    atoms.center(6.0)

    sgen = RandomCluster(atoms, repstrength=0.45, rng=rng)
    new_atoms = sgen.get()

    for i in range(len(new_atoms)):
        for j in range(len(new_atoms)):
            
            if i == j:
                continue

            distance = np.linalg.norm(new_atoms.positions[i] -
                                      new_atoms.positions[j])
            assert 1.0 < distance
            assert distance < 10.0

def test_randombranch():
    '''
    Generate new clusters by adding atoms one by one next to
    each other.
    '''

    rng = np.random.RandomState(30062021)

    atoms = Atoms(['Cu'] * 6 + ['Ag'] * 6,
                  positions=[[0., 0., 0.]] * 12)
    atoms.center(6.0)

    sgen = RandomBranch(atoms, llim=1.8, ulim=2.2, rng=rng)
    new_atoms = sgen.get()

    for i in range(len(new_atoms)):
        for j in range(len(new_atoms)):
            
            if i == j:
                continue

            distance = np.linalg.norm(new_atoms.positions[i] -
                                      new_atoms.positions[j])
            assert 1.8 < distance
