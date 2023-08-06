""" Tests for pytest

Usage
-----
>>> python3 -m pytest
"""

import pytest

from gpatom.beacon import BEACON
from gpatom.beacon.str_gen import (Rattler, ReadFiles,
                                   RandomCell, RandomBranch)
from ase.build.surface import fcc100
from ase import Atoms
from ase.calculators.emt import EMT
from ase.io import read, write
from ase.constraints import FixAtoms

import numpy as np


def test_go_no_atoms():
    with pytest.raises(TypeError):

        # Raises error since no structure generator is given:
        BEACON(EMT, gp_args={'use_forces': True})


def test_beacon_periodic():
    atoms1 = fcc100('Au', (2, 2, 2))
    atoms1.info = {}
    atoms1.center(vacuum=6.0, axis=2)

    atoms2 = atoms1.copy()
    atoms2.rattle(0.5)

    sgen = RandomCell(atoms1, rng=np.random.RandomState(451))

    go = BEACON(EMT, sgen=sgen,
                atoms=[atoms1, atoms2],
                ndft=1, nsur=1, fmax=0.1)
    go.run()

    atoms2.calc = EMT()
    print(atoms2.get_potential_energy())
    f = open('info.txt', 'r')
    print(f.readlines())
    f.close()
    assert len(go.initatomsgen.lob) == 0  # length of list of best
    assert abs(read('structures_dft.xyz@-1').get_potential_energy() -
               7.2985888331) < 1e-6


def scalefit(beacon_args):
    atoms = Atoms(['Au'] * 4,
                  positions=[[0., 0., 0.]] * 4)
    atoms.center(vacuum=6.0)
    sgen = RandomBranch(atoms, rng=np.random.RandomState(987))

    def_beacon_args = dict(calc=EMT,
                           sgen=sgen,
                           gp_args={'use_forces': True,
                                    'params': {'scale': 10,
                                               'aweight': 50}},
                           ndft=5, nsur=3, nbest=1, nrattle=1,
                           rng=np.random.RandomState(432))
    def_beacon_args.update(beacon_args)
    beacon_args = def_beacon_args

    go = BEACON(**beacon_args)
    go.run()

    f = open('info.txt', 'r')
    lines = f.readlines()
    f.close()

    assert len(lines) == 6
    values = []
    for line in lines:
        row = line.split()
        if line.startswith('#'):
            columns = row[1:]
            continue
        values.append(row)
    values = np.array(values, dtype=float)

    # Values in first step should be different
    # from values in the last step:
    for column in ['pred', 'real', 'unc', 'diff', 'fmax',
                   'mindist', 'maxdist', 'scale', 'weight',
                   'prior', 'noise']:
        col_values = values[:, columns.index(column)]
        assert col_values[0] != col_values[-1]

        # scale is fit (i.e. changed) between steps 2 and 3:
        if column == 'scale':
            assert col_values[1] == col_values[2]
            assert col_values[2] != col_values[3]
            assert col_values[3] == col_values[4]


def test_scalefit():
    beacon_args = dict()
    scalefit(beacon_args)


def test_scalefit_noforces():
    beacon_args = dict(gp_args={'use_forces': False})
    scalefit(beacon_args)


def run_order_of_images(beacon_args):

    atoms = Atoms(['Au'] * 4,
                  positions=[[0., 0., 0.]] * 4)
    atoms.center(vacuum=6.0)

    sgen = RandomBranch(atoms, rng=np.random.RandomState(631))

    atoms1 = sgen.get()
    atoms2 = atoms1.copy()
    atoms2.rattle(0.05, seed=0)

    sgen = Rattler(atoms1.copy(), rng=np.random.RandomState(123))

    def_beacon_args = dict(calc=EMT,
                           sgen=sgen,
                           gp_args={'use_forces': True,
                                    'params': {'scale': 10,
                                               'aweight': 50}},
                           ndft=1, nsur=1, fmax=0.1)
    def_beacon_args.update(beacon_args)
    beacon_args = def_beacon_args

    go1 = BEACON(atoms=[atoms1, atoms2],
                 **beacon_args)
    go1.run()
    e1 = read_last_prediction()

    sgen = Rattler(atoms1.copy(), rng=np.random.RandomState(123))
    beacon_args.update(sgen=sgen)
    go2 = BEACON(atoms=[atoms2, atoms1],
                 **beacon_args)
    go2.run()
    e2 = read_last_prediction()

    assert abs(e1 - e2) < 1e-6


def test_order_of_images():
    beacon_args = {}
    run_order_of_images(beacon_args)


def test_order_of_images_noforces():
    beacon_args = dict(gp_args={'use_forces': False,
                                'params': {'scale': 10, 'aweight': 50}})
    run_order_of_images(beacon_args)


def test_same_point():
    atoms1 = fcc100('Au', (2, 2, 2))
    atoms1.info = {}
    atoms1.center(vacuum=6.0, axis=2)
    sg = Rattler(atoms1, rng=np.random.RandomState(321))
    atoms2 = sg.get()

    atoms2.calc = EMT()
    atoms2.pbc = True, True, False
    atoms2.center()
    e1 = atoms2.get_potential_energy()
    f1 = atoms2.get_forces()

    write('mytmp.xyz', atoms2)

    sg = ReadFiles(['mytmp.xyz'] * 2)

    noise = 1e-3
    go = BEACON(EMT,
                gp_args={'use_forces': True,
                         'params': {'scale': 0.01, 'noise': noise}},
                atoms=[atoms1, atoms2],
                ndft=1,
                nsur=1,
                nrattle=0,
                nbest=0,
                relax_steps=0,
                fmax=1e12,
                sgen=sg,
                checks=False,
                foutput='forces.txt')

    go.run()

    e2 = read_last_prediction()
    f2 = read_last_predicted_forces()

    # Energies
    assert abs(e1 - e2) < noise

    # Forces
    assert (np.square(f1.flatten() - f2.flatten()) < noise**2).all()

    # clean-up
    from os import remove
    remove('mytmp.xyz')
    remove('tmp.xyz')


def read_last_prediction():
    with open('info.txt', 'r') as f:
        e = float(f.readlines()[-1].split()[1])
    return e


def read_last_predicted_forces():
    with open('forces.txt', 'r') as f:
        forces = []
        for i, line in enumerate(f):
            if i == 0:  # energy line
                continue
            line = line.split()
            if len(line) < 2:
                continue
            forces.append(line[2])

    forces = np.array(forces).astype(float)
    return forces


class ListGenerator:
    def __init__(self, atomslist):
        self.atomslist = [a.copy() for a in atomslist]
        self.index = 0

    def get(self):
        atoms = self.atomslist[self.index]
        self.index += 1
        return atoms


def test_invalid_structures():
    atoms1 = fcc100('Au', (2, 2, 1))
    atoms1.info = {}
    atoms1.pbc = False
    atoms1.center(vacuum=6.0)
    atoms1.rattle(0.1)

    atoms2 = atoms1.copy()
    atoms2.rattle(0.5)

    badatoms = atoms2.copy()
    badatoms.positions[1] = badatoms.positions[0] + [0., 0.5, 0.5]

    sgen = ListGenerator([badatoms, badatoms, atoms1, atoms1])

    go = BEACON(EMT, sgen=sgen,
                atoms=[atoms1, atoms2],
                ndft=1, nsur=1,
                relax_steps=0)
    go.run()

    extras = read('extras.xyz@:')
    assert len(extras) == 1
    assert go.gpinterface.ntrain == 3


def test_constrainedatoms():
    '''
    Test that the FixAtoms constraints of initial training set
    is transferred into Beacon and its resulting structures.
    '''

    atoms = fcc100('Au', (2, 2, 1))
    atoms.info = {}
    atoms.pbc = False
    atoms.center(vacuum=1.0)
    atoms.rattle(0.05)
    atoms.set_constraint(FixAtoms(indices=[1, 2]))

    origpos = atoms.positions.copy()

    sgen = RandomCell(atoms, rng=np.random.RandomState(451))

    go = BEACON(EMT, sgen=sgen,
                ndft=1, nsur=1, fmax=0.1)
    go.run()

    newpos = read('structures_dft.xyz@-1').positions.copy()

    # test only relative positions (because beacon might wrap
    # and re-center atoms):

    # constrained atoms:
    assert np.allclose(newpos[2] - newpos[1],
                       origpos[2] - origpos[1])

    # unconstrained atoms:
    assert not np.allclose(newpos[1] - newpos[0],
                           origpos[1] - origpos[0])
