import numpy as np
import pytest
from ase.build import bulk
from ase.calculators.emt import EMT

from gpatom.gpmin import GPMin
from gpatom.lgpmin import LGPMin


def test_gpmin():
    atoms = bulk('Au') * (2, 2, 2)
    atoms.rattle(stdev=0.2)
    atoms.calc = EMT()
    opt = GPMin(atoms)
    fmax = 0.001
    for i, _ in enumerate(opt.irun(fmax=fmax)):
        print(_)

    fmax1 = np.linalg.norm(atoms.get_forces(), axis=1).max()
    energy = atoms.get_potential_energy()
    assert fmax1 <= fmax
    assert i == 12  # We expect exactly this number of iterations.
    # It is bad that we test the iteration count so specifically.
    # We'll have to be a little bit zealous like that until we get
    # better unittests.
    assert energy == pytest.approx(0.020860, abs=1e-5)


def test_fit_hyperparams():
    atoms = bulk('Au') * (2, 2, 1)
    atoms.rattle(stdev=0.2)
    atoms.calc = EMT()
    opt = GPMin(atoms, batch_size=5, update_hyperparams=True)

    init_hp = opt.gp.hp.copy()

    fmax = 0.001
    for i, _ in enumerate(opt.irun(fmax=fmax)):
        print(_)

    final_hp = opt.gp.hp.copy()

    assert final_hp['scale'] != init_hp['scale']

    fmax1 = np.linalg.norm(atoms.get_forces(), axis=1).max()
    energy = atoms.get_potential_energy()
    assert fmax1 <= fmax
    assert i == 8  # We expect exactly this number of iterations.
    assert energy == pytest.approx(0.010426, abs=1e-5)


def test_lgpmin():
    atoms = bulk('Au') * (2, 2, 2)
    atoms.rattle(stdev=0.2)
    atoms.calc = EMT()
    opt = LGPMin(atoms, memory=300)
    fmax = 0.001
    for i, _ in enumerate(opt.irun(fmax=fmax)):
        print(_)

    fmax1 = np.linalg.norm(atoms.get_forces(), axis=1).max()
    energy = atoms.get_potential_energy()
    assert fmax1 <= fmax
    assert i == 12  # We expect exactly this number of iterations.
    # It is bad that we test the iteration count so specifically.
    # We'll have to be a little bit zealous like that until we get
    # better unittests.
    assert energy == pytest.approx(0.020860, abs=1e-5)
