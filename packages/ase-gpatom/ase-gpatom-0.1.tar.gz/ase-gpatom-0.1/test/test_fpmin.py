from ase.calculators.emt import EMT
from ase.build import bulk

from gpatom.aidmin import AIDMin, AIDModel
from gpatom.gpfp.fingerprint import (RadialFP,
                                     CartesianCoordFP)


def fingerprint_relaxation(fp, **params):
    atoms = bulk('Ag', 'fcc')
    atoms *= (3, 2, 1)

    atoms.rattle(0.2, seed=4)
    N = len(atoms)
    indices = [0]

    for i in indices:
        atoms[i].symbol = 'Au'

    model = AIDModel(update_prior_strategy='maximum',
                     fingerprint=fp,
                     params=params,
                     mask_constraints=False)

    atoms.calc = EMT()

    opt = AIDMin(atoms,
                 model_calculator=model,
                 use_previous_observations=False,
                 trainingset=[])

    opt.run(fmax=0.05)


def test_radial_relaxation():
    params = dict(scale=1000, limit=4.0)
    fingerprint_relaxation(fp=RadialFP, **params)


def test_cartesiancoord_relaxation():
    params = dict(scale=0.1)
    fingerprint_relaxation(fp=CartesianCoordFP, **params)

