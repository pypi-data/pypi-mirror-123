# -*- coding: utf-8 -*-
"""Convienence class to extract various data from Octopus output.
"""

# Python Imports
import re
from itertools import product

# Third Party Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi

# Octopost Imports
import units


class OutputReadModel:
    """OutputRead model handles all things related to basic information output.

    Should not be used directly by the user but called by the abstraction layer
    octopost class.

    Args:
        octopost (object): An instance of the octopost class.
    """

    def __init__(self, ocotpost):
        self.op = ocotpost

    def get_fermi(self, energy_units='hartree'):
        """Returns fermi energy found in the 'total-dos-efermi.dat' file.

        Args:
            energy_units (str): Specify the units in which the energy is
                returned. Options: 'hartree', 'eV'

        Returns:
            float:
                Fermi energy in the specified units.
        """

        file = 'total-dos-efermi.dat'
        dir_ = 'static'
        path = self.op._check_for_file(dir_, file)

        with open(path, 'r') as f:
            # Fermi energy is the first value in the file
            fermi = np.loadtxt(f)[0, 0]

        if energy_units == 'eV':
            fermi = units.energy(fermi, from_='hartree', to='eV')

        return fermi

    def get_eigenvalues(self, n_max=None, n_min=1, k_point=None,
                        energy_units='hartree'):
        """Returns the eigenvalues found in the 'info' file.

        Args:
            n_max (int): How many eigenvalues to be returned. If 'None' all of
                them are returned. If n_max > available eigenvalues all
                available ones are returned.
            k_points (int): At which k_point the eigenvalues are to be read.
            energy_units (str): Specify the units in which the energy is
                returned. Options: 'hartree', 'eV'

        Returns:
            list:
                List of eigenvalues (float).
        """

        dir_ = 'static'
        file = 'info'
        path = self.op._check_for_file(dir_, file)

        with open(path, 'r') as f:
            line = f.readline()

            if k_point is not None:
                # Periodic system
                while line and ('#k =' + f'{k_point}'.rjust(4)) not in line:
                    line = f.readline()

            else:
                # Non-periodic system
                while (line and
                       line != ' #st  Spin   Eigenvalue      Occupation\n'):
                    line = f.readline()

            if not line:
                print(f'{path} is not a valid \'info\' file.')
                raise

            eigenvalues = []
            if n_max is not None:
                line = f.readline()
                n = 1
                while (line and line != '\n' and '#k' not in line and
                       n <= n_max):

                    if n >= n_min:
                        eigenvalues.append(float(
                            re.search('-- *(.*?) ', line).groups()[0]))

                    line = f.readline()
                    n += 1

                if '#k' in line:
                    print('INFO: Not enough eigenvalues.')

            else:
                line = f.readline()
                n = 1
                while (line and line != '\n' and
                       '#k' not in line):

                    if n >= n_min:
                        eigenvalues.append(float(
                            re.search('-- *(.*?) ', line).groups()[0]))

                    line = f.readline()
                    n += 1

        eigenvalues = np.array(eigenvalues)
        if energy_units == 'eV':
            eigenvalues = units.energy(eigenvalues, from_='hartree', to='eV')

        return eigenvalues

    def get_orbital_state_number(self, state='HOMO'):
        """Returns state number of the chosen state. Only works for non
        periodic systems. Mostly for other Octopost methods.

        Args:
            state (str): State for which the number is to be found. Options:
                'homo', 'lumo', 'homo-x', 'lumo+x' where 'x' is any integer > 0

        Returns:
            int:
                State number.
        """

        dir_ = 'static'
        file = 'info'
        path = self.op._check_for_file(dir_, file)

        with open(path, 'r') as f:
            line = f.readline()

            while (line and
                    line != ' #st  Spin   Eigenvalue      Occupation\n'):
                line = f.readline()

            if not line:
                print(f'{path} is not a valid \'info\' file.')
                raise

            line = f.readline()
            while (line and line != '\n' and
                   float(re.search(r' ([.0-9]*?)$', line).group(1)) != 0.):
                homo = int(re.search(r'^ *?([0-9]+)', line).group(1))
                line = f.readline()

            state = state.lower()

            if state == 'homo':
                return homo

            elif state[:4] == 'homo':
                return homo - int(re.search(r'-(\d*?)$', state).group(1))

            elif state == 'lumo':
                return homo + 1

            elif state[:4] == 'lumo':
                return homo + 1 + int(
                    re.search(r'\+(\d*?)$', state).group(1))

            else:
                raise ValueError

    def get_cell(self):
        """Returns lattice vectors.

        Returns:
            nd.array:
                3x3 array where first index runs through the vectors
                and second through their coordinate.
        """

        dir_ = 'static'
        file = 'info'
        path = self.op._check_for_file(dir_, file)

        found = False
        with open(path) as f:
            for line in f:
                if line.startswith('  Lattice Vectors'):
                    lattice = np.zeros((3, 3))
                    for i in range(3):
                        lattice[i, :] = self._parse_vector(f.readline())

                    found = True
        if found:
            return lattice

        else:
            print('No reciprocal lattice found. Is this system periodic?')
            raise TypeError

    def get_reciprocal_cell(self):
        """Returns reciprocal lattice vectors.

        Returns:
            nd.array:
                3x3 array where first index runs through the vectors and second
                through their coordinate.
        """

        dir_ = 'static'
        file = 'info'
        path = self.op._check_for_file(dir_, file)

        found = False
        with open(path) as f:
            for line in f:
                if line.startswith('  Reciprocal-Lattice Vectors'):
                    lattice = np.zeros((3, 3))
                    for i in range(3):
                        lattice[i, :] = self._parse_vector(f.readline())

                    found = True
        if found:
            return lattice

        else:
            print('No reciprocal lattice found. Is this system periodic?')
            raise TypeError

    def get_first_brillouin(self):
        """Returns the first Brillouin zone in the xy plane.

        Calculates the vertices and order of connection between the vertices
        for the first Brillouin zone in the xy plane.

        Returns:
            nd.array:
                Nx2 array where first index runs through the vertices of the
                Brillouin zone (a prior not clear how many) and the second
                index are the coordinates x and y.
            list:
                Indicies of vertices in order of connection, i.e. vertex number
                list[0] (in the vertex array) is connected to vertex number
                list[1] and list[-1].
        """

        # Keep only x, y components of x, y unit vectors
        x, y = self.op.get_reciprocal_cell()[:2, :2]
        # Construct unique list of all next lattice points
        factors = product([-1, 0, 1], repeat=2)
        points = list(set([tuple(f[0] * x + f[1] * y) for f in factors]))

        vor = Voronoi(points)
        vertices = vor.vertices

        # Find the connected region
        connection = []
        for region in vor.regions:
            if region and -1 not in region:
                connection = region
                break

        return vertices, connection

    def plot_reciprocal(self, unit_vectors=True, brillouin=True,
                        origin=False, axes=None):
        """Plots the unit cell, origin and first Brillouin zone in 2D.

       Args:
            unit_vectors (bool): Whether or not to plot the reciprocal unit
                vectors.
            brillouin (bool): Whether or not to plot the first Brillouin zone.
            origin (bool): Whether or not to plot the origin.
            axes (fig, ax): Matplotlib handles for the figure the plots are to
                be added.

        Returns:
            fig, ax:
                Matplotlib handles for the figure and axis.
        """

        if axes is None:
            fig, ax = plt.subplots()

        else:
            fig, ax = axes

        if origin:
            ax.scatter(0, 0, 0, marker='x', color='k')

        if unit_vectors:
            vectors = self.op.get_reciprocal_cell()[:2, :2]
            for vector in vectors:
                ax.arrow(0, 0, *vector, color='k')

        if brillouin:
            vertices, con = self.get_first_brillouin()
            for i in range(len(con)):
                ax.plot(*np.stack((vertices[con[i - 1], :],
                                   vertices[con[i], :])).T,
                        color='k')

        return fig, ax

    def get_convergence(self, plot=False, values=('energy', 'density')):
        """Returns the convergence parameter energy and density.

        Args:
            plot (bool): If True a basic convergence plot for energy and
                density will be returned.
            values (list): List containing strings denoting which values should
                be examined for convergence. Any combination of:
                'energy', 'density'
        Returns:
            nd.array:
                First column is the SCF cycle. Then energy, energy
                difference, density and relative density in this order.
            fig, ax, ax:
                Matplotlib handles for the figure, the left axis
                and the right axis in this order.
        """

        dir_ = 'static'
        file = 'convergence'
        path = self.op._check_for_file(dir_, file)
        data = np.loadtxt(path)[:, :5]

        if plot and values:
            fig, ax_left = plt.subplots()
            axes = []

            if 'energy' in values:
                line_1 = ax_left.plot(data[:, 0], data[:, 1], marker='o',
                                      linestyle='', color='tab:red',
                                      label='Total Energy')
                line_2 = ax_left.plot(data[:, 0], data[:, 2], color='tab:red',
                                      label='Energy Difference', marker='x',
                                      linestyle='')

                ax_left.set_xlabel('SCF Cycle')
                ax_left.set_ylabel('Energy (Hartree)')
                axes.append(ax_left)

                if 'density' in values:
                    ax_right = ax_left.twinx()
                    ax_left.tick_params(axis='y', labelcolor='tab:red')
                    ax_left.yaxis.label.set_color('tab:red')

                    line_3 = ax_right.plot(data[:, 0], data[:, 3], marker='o',
                                           linestyle='', color='tab:blue',
                                           label='Total Density')
                    line_4 = ax_right.plot(data[:, 0], data[:, 4],
                                           color='tab:blue',
                                           marker='x', linestyle='',
                                           label='Relative Density')

                    ax_right.set_ylabel('Density', color='tab:blue')
                    ax_right.tick_params(axis='y', labelcolor='tab:blue')
                    axes.append(ax_right)
                    lines = line_1 + line_2 + line_3 + line_4

                else:
                    lines = line_1 + line_2

            elif 'density' in values:
                line_1 = ax_left.plot(data[:, 0], data[:, 3], marker='o',
                                      linestyle='', color='tab:red',
                                      label='Total Density')
                line_2 = ax_left.plot(data[:, 0], data[:, 4], color='tab:red',
                                      label='Relative Density', marker='x',
                                      linestyle='')

                ax_left.set_xlabel('SCF Cycle')
                ax_left.set_ylabel('Density')
                axes.append(ax_left)
                lines = line_1 + line_2

            else:
                return data

            labels = [line.get_label() for line in lines]
            ax_left.legend(lines, labels, loc='center left')

            return data, (fig, axes)

        else:
            return data

    def _parse_vector(self, line):

        vector = re.search(
            r' {1,4}([0-9\.\-]*) {1,4}([0-9\.\-]*) {1,4}([0-9\.\-]*)',
            line).groups((1, 2, 3))
        vector = [float(number) for number in vector]

        return vector
