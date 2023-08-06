""" Tests for pytest

Usage
-----
>>> python3 -m pytest
"""

import pytest

from gpatom.beacon.beacon import (StructureList, InitatomsGenerator,
                                  BEACONGPInterface, SurrogateOptimizer,
                                  ConstraintHandler, Checker, BEACONAtomsIO,
                                  IterationResult)
from gpatom.gpfp.calculator import GPCalculator
from gpatom.beacon.str_gen import RandomBranch
from ase.build.surface import fcc100
from ase.calculators.emt import EMT
from ase.optimize import BFGS
from ase.constraints import FixAtoms
from ase.io import read
from os.path import exists

import numpy as np

def set_atoms():
    atoms1 = fcc100('Au', (2, 2, 1))
    atoms1.pbc = False
    atoms1.info = {}
    atoms1.center(vacuum=6.0)
    atoms1.rattle(0.1)

    sgen = RandomBranch(atoms1, rng=np.random.RandomState(451))
    atoms2 = sgen.get()
    atoms3 = sgen.get()

    atoms1.calc = EMT()
    atoms2.calc = EMT()
    atoms3.calc = EMT()

    return atoms1, atoms2, atoms3, sgen

def test_structurelist():

    atoms1, atoms2, atoms3, sgen = set_atoms()

    # Make sure our test makes sense:
    assert atoms1.get_potential_energy() < atoms2.get_potential_energy()
    assert atoms1.get_potential_energy() < atoms3.get_potential_energy()
    assert atoms3.get_potential_energy() < atoms2.get_potential_energy()

    # Initialize object:
    obj = StructureList(images=[atoms1, atoms2], n=2)
    assert len(obj) == 2

    # Update list:
    obj.update(new_atoms=atoms3, index=2)

    # atoms3 has lower energy than atoms2, and therefore
    # it should have been moved to the second place of
    # structure list:
    assert len(obj) == 2
    assert obj[1] == atoms3
    assert obj.energies[1] == atoms3.get_potential_energy()



    # Relax first structure and move it to the list:
    new = atoms1.copy()
    new.calc = EMT()
    opt = BFGS(new)
    opt.run(fmax=obj.flim)

    # Update list:
    obj.update(new_atoms=new, index=0)

    # Now the first element should have been removed from the
    # list because we relaxed it to small force residuals.
    # The list should only contain atoms3 now:
    assert len(obj) == 1
    assert obj[0] == atoms3
    assert obj.energies[0] == atoms3.get_potential_energy()


def test_empty_structurelist():

    atoms1, atoms2, atoms3, sgen = set_atoms()

    # Initialize object:
    obj = StructureList(images=[], n=2)

    # Update list:
    obj.update(new_atoms=atoms1, index=2)

    assert len(obj) == 1
    assert obj[0] == atoms1
    assert obj.energies[0] == atoms1.get_potential_energy()


def test_testatomsgenerator():

    atoms1, atoms2, atoms3, sgen = set_atoms()

    # Make sure our test makes sense:
    assert atoms1.get_potential_energy() < atoms2.get_potential_energy()
    assert atoms1.get_potential_energy() < atoms3.get_potential_energy()
    assert atoms3.get_potential_energy() < atoms2.get_potential_energy()

    # Initialize object:
    obj = StructureList(images=[atoms1, atoms2], n=2)

    gen = InitatomsGenerator(nrattle=1, sgen=sgen, lob=obj,
                             rng=np.random.RandomState(600))

    # best
    testatoms = gen.get(0)
    testatoms.center()
    atoms1.center()
    assert np.allclose(testatoms.positions, atoms1.positions)

    # second best
    testatoms = gen.get(1)
    testatoms.center()
    atoms2.center()
    assert np.allclose(testatoms.positions, atoms2.positions)

    # rattled one
    testatoms = gen.get(2)
    testatoms.center()
    atoms3 = atoms1.copy()
    atoms3.rattle(0.5, seed=np.random.RandomState(600).randint(100000))
    atoms3.center()
    assert np.allclose(testatoms.positions, atoms3.positions)

    # something else:
    testatoms = gen.get(3)
    testatoms.center()
    sgen = RandomBranch(atoms1, rng=np.random.RandomState(451))

    assert not np.allclose(testatoms.positions, atoms1.positions)
    assert not np.allclose(testatoms.positions, atoms2.positions)
    assert not np.allclose(testatoms.positions, atoms3.positions)

    atoms4 = atoms2.copy()
    rng = np.random.RandomState(601)
    rng.randint(100000)
    atoms4.rattle(0.5, seed=rng.randint(100000))
    atoms4.center()
    assert not np.allclose(testatoms.positions, atoms4.positions)


def test_GPInterface():

    atoms1, atoms2, atoms3, sgen = set_atoms()

    sgen = RandomBranch(atoms1, rng=np.random.RandomState(451))

    initatoms = [sgen.get(), sgen.get()]

    # Test error if no calculator is attached to init atoms:
    with pytest.raises(RuntimeError):
        gp = BEACONGPInterface(initatoms=initatoms)

    for atoms in initatoms:
        atoms.calc = EMT()

    gp = BEACONGPInterface(initatoms=initatoms)

    # Assert correct length scale:
    assert abs(gp.gp_args['params']['scale'] - 407.301) < 0.001

    # Assert predicted energy and uncertainty:
    testatoms = sgen.get()
    e, f, u = gp.calculate(testatoms)
    assert abs(e - 71.901) < 0.001
    assert abs(u - 0.9736) < 0.0001

    # Test fitting the length scale:
    testatoms.calc = EMT()
    testatoms.get_potential_energy()
    gp.add_training_points([testatoms])

    gp.batch_size = 4
    gp.update_prior_distribution()
    gp.model.gp.set_hyperparams({'scale': 0.00001})
    gp.fix_scale()
    assert abs(gp.model.gp.hp['scale'] - 7.167) < 0.001


def test_surrogateoptimizer():

    atoms1, atoms2, atoms3, sgen = set_atoms()
    sgen = RandomBranch(atoms1, rng=np.random.RandomState(451))

    initatoms = [sgen.get(), sgen.get()]

    for atoms in initatoms:
        atoms.calc = EMT()

    gp = BEACONGPInterface(initatoms=initatoms)

    opt = SurrogateOptimizer(fmax=0.05, relax_steps=0,
                             write_surropt_trajs=True)

    # assert correct value because relax_steps=0:
    assert opt.dont_relax

    opt = SurrogateOptimizer(fmax=0.05, relax_steps=10,
                             write_surropt_trajs=True)

    # assert correct value because relax_steps > 0:
    assert not opt.dont_relax

    atoms1.calc = GPCalculator(gp.model)
    success = opt.relax(atoms1, index=2, subindex=12)

    # assert no success because so few evaluations:
    assert not success

    # assert file exists:
    assert exists('opt_002_012.traj')

    # assert correct result:
    assert abs(atoms1.get_potential_energy() - -5.207) < 0.001


def test_constrainthandler():
    atoms1 = fcc100('Au', (2, 2, 1))
    atoms1.pbc = False
    atoms1[1].symbol = 'Cu'

    # No constraints:
    c = ConstraintHandler(atoms1)
    assert len(c.constraints) == 0
    assert len(c.cindex) == 0
    assert (c.ucindex == list(range(len(atoms1)))).all()


    # With constraints:
    atoms1.set_constraint(FixAtoms(indices=(0, 2)))

    c = ConstraintHandler(atoms1)
    assert len(c.constraints) == 1
    assert (c.cindex == [0, 2]).all()
    assert (c.ucindex == [1, 3]).all()


def test_checker():
    atoms1, atoms2, atoms3, sgen = set_atoms()
    atoms1[1].symbol = 'Cu'

    atoms1.positions = [[0., 0., 0.],
                        [1., 0., 0.],
                        [0., 3., 0.],
                        [0., 3., 10.]]

    checker = Checker(checks=True, dist_limit=0.5,
                      energylimit=1.0, blimit=-np.inf)

    # bad bond lengths:
    assert not checker.check(atoms1, distances=[100.], index=0, subindex=0)

    atoms1.positions = [[0., 0., 0.],
                        [2., 0., 0.],
                        [0., 4., 0.],
                        [0., 3., 10.]]

    # good:
    assert checker.check(atoms1, distances=[100.], index=0, subindex=0)

    # bad distances:
    assert not checker.check(atoms1, distances=[0.4, 100.], index=0, subindex=0)

    # energy checks:
    assert checker.check_bad_result(energy=2.5)
    assert not checker.check_bad_result(energy=0.5)


def test_beaconatomsio():

    # default params:
    atomsio = BEACONAtomsIO()
    assert exists('structures_dft.xyz')

    # test write_xyz:
    atoms1 = fcc100('Au', (2, 2, 1))
    atoms1.info.clear()
    atoms1.pbc = False
    atoms1.calc = EMT()
    atoms1.get_potential_energy()

    atomsio.write_xyz(atoms1, strtype='init')
    testatoms = read('init_structures.xyz@:')
    assert len(testatoms) == 1

    # tmp.xyz read and write:
    atomsio.write_tmpfile(atoms1,
                          write_results=False)
    testatoms = atomsio.read_tmpfile()
    assert len(testatoms) == 4


def test_iterationresult():
    atoms1, atoms2, atoms3, sgen = set_atoms()
    it_result = IterationResult(atoms1)

    assert it_result.is_better(1.0)

    it_result.update({'acq': 0.5})
    assert not it_result.is_better(1.0)

    assert it_result.get_min_rank() == 0
