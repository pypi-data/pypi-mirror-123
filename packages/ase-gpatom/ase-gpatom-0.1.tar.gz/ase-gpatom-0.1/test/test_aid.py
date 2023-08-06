import numpy as np
from ase.build import fcc100, add_adsorbate
from ase.calculators.emt import EMT
from ase.constraints import FixAtoms
from gpatom.aidneb import AIDNEB
from gpatom.aidmin import AIDMin


# 2x2-Al(001) surface with 3 layers and an
# Au atom adsorbed in a hollow site:
def test_aid():
    slab = fcc100('Al', size=(2, 2, 3))
    add_adsorbate(slab, 'Au', 1.7, 'hollow')
    slab.center(axis=2, vacuum=4.0)
    slab.calc = EMT()

    # Fix second and third layers:
    mask = [atom.tag > 0 for atom in slab]
    slab.set_constraint(FixAtoms(mask=mask))

    # 1.2. Optimize initial and final end-points.

    # Initial end-point:
    qn = AIDMin(slab, trajectory='initial.traj',
                use_previous_observations=False,
                trainingset='initial_observations.traj')

    qn.run(fmax=0.01)

    # Final end-point:
    slab[-1].x += slab.get_cell()[0, 0] / 2
    qn = AIDMin(slab, trajectory='final.traj', use_previous_observations=False,
        trainingset = 'final_observations.traj')
    qn.run(fmax=0.01)

    # AIDNEB:
    aidneb = AIDNEB(start='initial_observations.traj',
                    end='final_observations.traj',
                    use_previous_observations=False,
                    calculator=EMT(),
                    interpolation='linear', n_images=5,
                    trajectory='AID.traj'
                    )

    aidneb.run(fmax=0.02, unc_convergence=0.005)

    # AID-NEB Function evaluations:
    n_eval_aidneb = aidneb.function_calls
    print('Number of function evaluations AID-NEB:', n_eval_aidneb)

    # Get saddle-point energy:
    mep_energies = []
    for image in aidneb.images:
        image.calc = EMT()
        mep_energies.append(image.get_potential_energy())

    E_f = np.max(mep_energies) - mep_energies[0]
    print('Climbing image energy:', E_f)

    # Check number of evaluations and energy barrier.
    assert n_eval_aidneb < 12
    assert abs(E_f - 0.400695) < 0.001
