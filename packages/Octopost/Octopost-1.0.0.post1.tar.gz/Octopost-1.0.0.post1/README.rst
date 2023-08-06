============
Octopost
============

**Octopost** contains a pool of python3 tools for post-processing data obtained with the TDDFT code OCTOPUS[1].

Octopost can be imported like any Python package into your analysis scripts
and provides a set of easy-to-use methods for extracting, preparing and even
plotting standard information like bandstructure, various (projected) density
of states, reciprocal cell for periodic systems and so on. The main focus,
however, lies in the ARPES (Angle-Resolved PhotoEmission Spectroscopy) methods
which make calculating ARPES maps (also called k-maps) easy and quick. The
calculated maps can be plotted and exported in a .hdf5 file compatible with
the POT (Photoemssion Orbital Tomography) simulation and analysis software
kMap.py[2].

| GitLab Page: https://gitlab.com/ckern/octopost
| Documentation: https://octopost.readthedocs.io/en/latest/


Authors
===============
- Christian Kern, MSc. (christian.kern@uni-graz.at)
- Peter Puschnig, Assoz. Prof. Dipl.-Ing. Dr. (peter.puschnig@uni-graz.at)
- Dominik Brandstetter, BSc. (dominik.brandstetter@edu.uni-graz.at)

Quick-start
===============
::

   pip install octopost

Installation
===============

It is generally recommended but not required to use a virtual enviroment like
venv or conda for this package. For a tutorial on how to use them please see `here <https://realpython.com/python-virtual-environments-a-primer/>`_.

User
----

As a user you only need the subset of packages nessecary to run the package.
The package will also not be installed in an editable form. The package will be
added to your current enviroment and will be available throughout it.::

   make install

on Linux, or::

   pip install .

on Windows.

Developer & Maintainer
----------------------

In order to develop for Octopost it is required to use the '-e' flag for pip
to install in editable mode. Furthermore, it is recommended to install the 'dev' and 'test' packages as well. Simply use::

   make install-dev

on Linux or::

   pip install -e .[test,dev]

on Windows.


Test
=====

If you wish to run the test suite please make sure you have Octopost and its
'test' dependencies installed. The latter is automatically the case if you followed the 'Developer & Maintainer' section of the installation guide. If you installed the 'User' version please additionally run::

   pip install .[test]

In order to run the test use::

   pytest

On Linux you can also use::

   make test


Demo
=====

Inside the './demo' folder you can find a number of small scripts showcasing different
Octopost functionalities and how to use them. Due to storage constraints the actual
Octopus output files required for the scripts will not be available on GitLab, however,
for most scripts the output plots can be found in the './demo/output' folder.

References
===============
[1] Nicolas Tancogne-Dejean, Micael J. T. Oliveira, Xavier Andrade, Heiko Appel, Carlos H. Borca, Guillaume Le Breton, Florian Buchholz, Alberto Castro, Stefano Corni, Alfredo A. Correa, Umberto De Giovannini, Alain Delgado, Florian G. Eich, Johannes Flick, Gabriel Gil, Adrián Gomez, Nicole Helbig, Hannes Hübener, René Jestädt, Joaquim Jornet-Somoza, Ask H. Larsen, Irina V. Lebedeva, Martin Lüders, Miguel A. L. Marques, Sebastian T. Ohlmann, Silvio Pipolo, Markus Rampp, Carlo A. Rozzi, David A. Strubbe, Shunsuke A. Sato, Christian Schäfer, Iris Theophilou, Alicia Welden, and Angel Rubio , "Octopus, a computational framework for exploring light-driven phenomena and quantum dynamics in extended and finite systems", J. Chem. Phys. 152, 124119 (2020) https://doi.org/10.1063/1.5142502

[2] Dominik Brandstetter, Xiaosheng Yang, Daniel Lüftner, F. Stefan Tautz, and Peter Puschnig , "kMap.py: A Python program for simulation and data analysis in photoemission tomography", Computer Physics Communications 263, 107905 (2021) https://doi.org/10.1016/j.cpc.2021.107905