from gpatom.gpfp.prior import RepulsivePotential
from gpatom.beacon.beacon import ConstraintHandler
from ase.optimize import BFGS
from ase.io import read

from scipy.spatial import distance_matrix
import numpy as np
import os


class RandomStructure:

    def __init__(self, atoms, rng=np.random):
        self.atoms = atoms
        self.rng = rng

    def sph2cart(self, r, theta, phi):
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return x, y, z

    def minimize_repulsive(self, atoms, repstrength=0.4):
        """ Relax a structure in a simple repulsive potential """

        reppot = RepulsivePotential()
        reppot.parameters.rc = 4.0
        reppot.parameters.prefactor = repstrength
        atoms.calc = reppot

        fmax = 0.01

        for i in range(100):
            opt = BFGS(atoms, maxstep=0.1, logfile=os.devnull)
            opt.run(fmax=fmax, steps=4)
            if np.max(np.linalg.norm(atoms.get_forces(), axis=1)) < fmax:
                break
        return atoms


class RandomBranch(RandomStructure):

    def __init__(self, atoms, llim=1.6, ulim=2.0,
                 shuffle=True, **kwargs):

        RandomStructure.__init__(self, atoms, **kwargs)

        assert (llim <= ulim), ('Upper limit (ulim) '
                                'should be larger than '
                                'lower limit (llim).')

        self.llim = llim
        self.ulim = ulim
        self.shuffle = shuffle

    def get(self):
        newatoms = self.atoms.copy()
        cell = newatoms.cell.lengths()
        newpos = []

        for i, symbol in enumerate(self.atoms.get_chemical_symbols()):
            if i == 0:
                newpos.append(newatoms.cell.lengths() / 2)
                continue

            while True:
                # Sample position for new atom:
                r, theta, phi = self.rng.random([3])
                r = self.llim + r * (self.ulim - self.llim)
                theta *= np.pi
                phi *= 2 * np.pi
                pos = self.sph2cart(r, theta, phi)

                # Add atom next to another one
                neighborindex = self.rng.randint(i)

                position = newpos[neighborindex] + pos
                newpos.append(position)

                # Check for valid structure:
                dm = distance_matrix(newpos, newpos)
                dm = np.where(dm > 0.0, dm, 100.)

                distances_ok = dm.min() > self.llim
                cell_ok = (0.0 < position).all() and (position < cell).all()

                if distances_ok and cell_ok:
                    break
                else:
                    newpos.pop(-1)

        newpos = np.array(newpos)

        newatoms.positions = newpos
        newatoms.center()

        if self.shuffle:
            self.rng.shuffle(newatoms.symbols.numbers)

        return newatoms


class RandomCell(RandomStructure):

    def __init__(self, atoms, do_minimize_repulsive=True,
                 repstrength=0.4, **kwargs):

        RandomStructure.__init__(self, atoms, **kwargs)

        self.do_minimize_repulsive = do_minimize_repulsive
        self.repstrength = repstrength
        self.constr = ConstraintHandler(atoms)

    def get(self):
        cell = self.atoms.cell.lengths()
        newatoms = self.atoms.copy()

        newpos = []

        for atom in self.atoms:

            if atom.index in self.constr.cindex:
                newpos.append(self.atoms.positions[atom.index])
                continue

            x = cell[0] * self.rng.random()
            y = cell[1] * self.rng.random()
            z = cell[2] * self.rng.random()

            pos = np.array([x, y, z])

            newpos.append(pos)

        newpos = np.array(newpos)

        # world.broadcast(newpos, 0)

        newatoms.positions = newpos

        if self.do_minimize_repulsive:
            newatoms = self.minimize_repulsive(newatoms,
                                               repstrength=self.repstrength)
        newatoms.wrap()
        newatoms.calc = None
        return newatoms


class RandomBox(RandomStructure):

    def __init__(self, atoms, box=[(0., 1.), (0., 1.), (0., 1.)],
                 do_minimize_repulsive=True, repstrength=0.4, **kwargs):

        RandomStructure.__init__(self, atoms, **kwargs)

        self.box = box
        self.do_minimize_repulsive = do_minimize_repulsive
        self.repstrength = repstrength
        self.constr = ConstraintHandler(atoms)

    def get_xyz(self):
        box = self.box
        x = (box[0][1] - box[0][0]) * self.rng.random() + box[0][0]
        y = (box[1][1] - box[1][0]) * self.rng.random() + box[1][0]
        z = (box[2][1] - box[2][0]) * self.rng.random() + box[2][0]
        return np.array([x, y, z])

    def get(self):
        newatoms = self.atoms.copy()

        newpos = []

        for atom in self.atoms:

            if atom.index in self.constr.cindex:
                pos = atom.position
            else:
                pos = self.get_xyz()

            newpos.append(pos)

        newpos = np.array(newpos)

        # world.broadcast(newpos, 0)

        newatoms.positions = newpos

        if self.do_minimize_repulsive:
            newatoms = self.minimize_repulsive(newatoms,
                                               repstrength=self.repstrength)
        newatoms.wrap()
        newatoms.calc = None

        newatoms.set_constraint(self.constr.constraints)

        return newatoms


class RandomCluster(RandomStructure):

    def __init__(self, atoms, repstrength=0.4, **kwargs):

        RandomStructure.__init__(self, atoms, **kwargs)

        self.repstrength = repstrength

    def get(self):
        newatoms = self.atoms.copy()

        newpos = []

        for atom in self.atoms:

            x = 0.5 * self.rng.random()
            y = 0.5 * self.rng.random()
            z = 0.5 * self.rng.random()

            pos = np.array([x, y, z])

            newpos.append(pos)

        newatoms.positions = newpos
        newatoms = self.minimize_repulsive(newatoms,
                                           repstrength=self.repstrength)

        newatoms.center()
        newatoms.wrap()

        return newatoms


class ReadFiles():

    def __init__(self, filenames):

        self.frames = [read(fname) for fname in filenames]
        self.count = 0

    def get(self):
        atoms = self.frames[self.count]
        self.count += 1
        return atoms


class Rattler(RandomStructure):

    def __init__(self, atoms, intensity=0.1,
                 firstseed=0, **kwargs):

        RandomStructure.__init__(self, atoms, **kwargs)

        self.intensity = intensity

    def get(self):
        atoms = self.atoms.copy()
        atoms.rattle(self.intensity,
                     seed=self.rng.randint(100000))
        atoms.wrap()
        return atoms
