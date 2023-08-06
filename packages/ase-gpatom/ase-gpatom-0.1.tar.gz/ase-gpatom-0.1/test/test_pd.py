from ase.build import fcc100
from ase.calculators.emt import EMT

from gpatom.gpfp.fingerprint import RadialAngularFP
from gpatom.gpfp.calculator import GPCalculator, Model
from gpatom.gpfp.prior import PriorDistributionSigmoid
from gpatom.gpfp.prior import RepulsivePotential
from gpatom.gpfp.prior import CalculatorPrior
from gpatom.gpfp.hpfitter import HyperparameterFitter


def set_structure(atoms, seed=0):
    """
    Create a copy and rattle.
    """
    newatoms = atoms.copy()
    newatoms.rattle(0.1, seed=seed)
    newatoms.calc = EMT()
    return newatoms


def test_pd():
    # Create slab
    slab = fcc100('Ag', size=(2, 2, 2))
    slab[-1].symbol = 'Au'
    slab[-2].symbol = 'Au'
    slab.rattle(0.5)
    slab.center(vacuum=4.0)
    slab.pbc = False
    slab.calc = EMT()

    # Create Training Set
    train_images = []
    for i in range(5):
        # Alter structure and get fingerprint
        slab2 = set_structure(slab, seed=i)
        train_images.append(slab2)

    onemore = set_structure(slab, seed=10)

    print('EMT energy: {}eV'.format(slab.get_potential_energy()))

    # Initialize fingerprint
    fp = RadialAngularFP
    params = {'weight': 1.0, 'scale': 500, 'delta': 0.2}

    prior_calc = RepulsivePotential()
    prior_calc.parameters.rc = 4.0
    prior_calc.parameters.prefactor = 0.7
    prior = CalculatorPrior(prior_calc)
    prior.constant = -360.0

    pd = PriorDistributionSigmoid(loc=100, width=0.001)

    model = Model(train_images=train_images,
                  params=params,
                  fingerprint=fp)
    model = HyperparameterFitter.fit(model, params_to_fit=['scale'], pd=pd)
    
    calc = GPCalculator(model)
    slab.calc = calc

    print('GP energy: {}eV'.format(slab.get_potential_energy()))

    # calc.set_hyperparams({'scale': 13}, noise=1e-3)
    # # calc.train(calc.X, calc.Y)
    # calc.update_train_data([onemore])

    # slab1 = slab.copy()
    # slab1.calc = calc

    # print('GP energy: {}eV'.format(slab1.get_potential_energy()))
