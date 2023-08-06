import pytest
from ase.build import fcc100, add_adsorbate
from ase.constraints import FixAtoms
from ase.calculators.emt import EMT
from ase.io import read

from gpatom.aidts import AIDTS


@pytest.mark.skip('Apparently not meant to be an automatic test')
def test_aids_example():
    atoms = fcc100('Pt', size = (2, 2, 1), vacuum = 10.0)
    add_adsorbate(atoms, 'Pt', 1.611, 'hollow')

    # Freeze the "slab"
    mask = [atom.tag > 0 for atom in atoms]
    atoms.set_constraint(FixAtoms(mask = mask))

    # Calculate using EMT
    atoms.calc = EMT()
    atoms.get_potential_energy()

    """
    Create dummy Atoms object with the positions of the structure to send the
    dimer. For instance if we want to send a dimer that move the Pt to the [001]
    direction we can do:
    """

    atoms_vector = atoms.copy()
    atoms_vector.positions[-1] = atoms_vector.positions[-1] + [0.5, 0.0, 0.0]

    # Take a look to the atoms (initial) and the dummy Atoms (atoms_vector,final).
    # view(atoms)  # initial structure.
    # view(atoms_vector)  # dummy structure (needed to send a vector towards there).

    # Then we can run the machine learning dimer method:
    mldimer = AIDTS(atoms=atoms,  # atoms, initial structure
                    atoms_vector=atoms_vector,  # dummy structure
                    vector_length=0.7,  # length of the atoms displacement.
                    max_train_data=50  # max training data (memory).
                    )

    mldimer.run(fmax=0.02)

    """
    You can take a look to the optimization process by read the trajectory
    file containing all the single-point calculations that the ML algorithm did
    to find the saddle-point:
    """

    atoms_opt = read('AID_observations.traj', ':')
    # view(atoms_opt)
