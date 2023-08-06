import numpy as np
from ase.build import fcc111
from ase.calculators.emt import EMT

from gpatom.gpfp.gp import GaussianProcess
from gpatom.gpfp.calculator import Model
from gpatom.gpfp.fingerprint import RadialAngularFP
from gpatom.gpfp.hpfitter import HyperparameterFitter, GPPrefactorFitter


def test_create():
    fp_class = RadialAngularFP
    params = dict(scale=2.0, limit=4.0, Rlimit=3.0, delta=0.4)

    # Create slab:
    slab = fcc111('Ag', size=(2, 2, 2))
    slab.center(vacuum=4.0, axis=2)
    slab.rattle(0.05)
    slab.calc = EMT()

    fp = fp_class(atoms=slab, **params)

    def new_atoms(rattle_seed=None):
        atoms = slab.copy()
        atoms.rattle(0.05, seed=rattle_seed)
        atoms.calc = EMT()
        return atoms

    frames = [new_atoms(rattle_seed=i) for i in range(1)]

    # from ase.visualize import view
    # view(frames)

    X = [fp_class(atoms=atoms, **params) for atoms in frames]

    energyforces = [[atoms.get_potential_energy()] +
                    list(atoms.get_forces().flatten())
                    for atoms in frames]
    Y = np.array(energyforces).reshape(-1)
    return frames, X, Y, fp_class, params, new_atoms


def test_train_and_predict():
    frames, X, Y, fp_class, params, new_atoms = test_create()
    gp = GaussianProcess(use_forces=True)
    gp.set_hyperparams(params)
    gp.train(X, Y)

    test_atoms = new_atoms(rattle_seed=10)
    test_x = fp_class(atoms=test_atoms, **params)
    results, variance = gp.predict(test_x, get_variance=True)

    test_atoms.calc = EMT()
    print('{:.06f} {:.06f}'.format(results[0],
                                   test_atoms.get_potential_energy()))


def test_fit_hyperparameters():
    frames, X, Y, fp_class, params, new_atoms = test_create()

    model = Model(frames, train_features=X, params=params)

    # Check weight fitting:
    model = GPPrefactorFitter.fit(model)
    logP_afterfit = model.gp.logP()

    model.gp.set_hyperparams({'weight': model.gp.hp['weight']+1})
    model.train_model(model.gp, model.data)
    logP_toobigweight = model.gp.logP()

    model.gp.set_hyperparams({'weight': model.gp.hp['weight']-2})
    model.train_model(model.gp, model.data)
    logP_toosmallweight = model.gp.logP()

    assert logP_afterfit > logP_toobigweight
    assert logP_afterfit > logP_toosmallweight

    # Check length scale fitting:
    model = HyperparameterFitter.fit(model, params_to_fit=['scale'])
    logP_afterfit = model.gp.logP()

    model.gp.set_hyperparams({'scale': model.gp.hp['scale'] * 1.1})
    model.train_model(model.gp, model.data)
    logP_toobigscale = model.gp.logP()

    model.gp.set_hyperparams({'scale': model.gp.hp['scale'] / 1.1 * 0.9})
    model.train_model(model.gp, model.data)
    logP_toosmallscale = model.gp.logP()

    assert logP_afterfit > logP_toobigscale
    assert logP_afterfit > logP_toosmallscale
