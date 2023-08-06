===================================================================
gpatom: Tools for atomistic simulations based on Gaussian processes
===================================================================

gpatom is a Python package which provides several tools for
geometry optimisation and related tasks in atomistic systems using machine learning surrogate models.
gpatom is an extension to the `Atomic Simulation Environment <https://wiki.fysik.dtu.dk/ase/>`_.

gpatom contains the following tools:

 * GPMin: An atomistic optimization algorithm based on Gaussian processes.
 * AIDMin: Energy structure minimization through the Artificial-Intelligence framework. 
 * AIDNEB: Nudged Elastic Band calculations through the Artificial-Intelligence framework. 
 * AIDTS: Transition State Search through the Artificial-Intelligence framework. 
 * AIDMEP: Minimum Energy Pathway through the Artificial-Intelligence framework.
 * BEACON: Bayesian Exploration of Atomic CONfigurations.
           BEACON does global optimization by Bayesian optimization
           by training the model with the DFT forces on atoms.
	   Represents the atoms with a global structural fingerprint.
	   Works generally well for different kinds of atomic systems:
	   clusters, surfaces, bulk systems.
	   For usage, see Gitlab Wiki:
	   https://gitlab.com/gpatom/ase-gpatom/-/wikis/How-to-use-BEACON


List of related publications:

 * BEACON:
        Global optimization of atomic structures with
        gradient-enhanced Gaussian process regression
        S. Kaappa, E. G. del R\'io, K. W. Jacobsen
        Physical Review B, vol. 103, 174114 (2021)
        https://doi.org/10.1103/PhysRevB.103.174114


Contact
=======

Please join our
`#gpatom <https://app.element.io/#/room/#gpatom:matrix.org>`_
channel on Matrix.


Installation cheat sheet
========================

There are no published releases yet.  To install a developer version (allows
in-place edits of the code), go to the toplevel AID directory and run:

  pip install --editable .


Testing cheat sheet
===================

Run the tests from the toplevel AID directory::

  $ pytest

Run the tests in parallel on ``n`` cores (requires pytest-xdist)::

  $ pytest -n 4

Show tests without running them::

  $ pytest --collectonly

Run tests in particular module::

  $ pytest test_module.py

Run tests matching pattern::

  $ pytest -k <pattern>

Show output from tests::

  $ pytest -s

Note that since many tests write files, temporary directories are
created for each test.  The temporary directories are located in
``/tmp/pytest-of-<username>/``.  pytest takes care of cleaning up
these test directories.

Use pytest.ini and test/conftest.py to customize how the tests run.
