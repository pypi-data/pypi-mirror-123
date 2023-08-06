# -*- coding: utf-8 -*-
"""Calculations related to the density of states.

This module contains the 'DOSModel' class, which handles all things
related to density of states calculations.
"""

# Python Imports
import re
import glob

# Third Party Imports
import numpy as np
import matplotlib.pyplot as plt

# Octopost Imports
import units


class DOSModel:
    """DOS model handles all things related to DOS.

    Should not be used directly by the user but called by the abstraction layer
    octopost class.

    Args:
        octopost (object): An instance of the octopost class.
    """

    def __init__(self, ocotpost):
        self.op = ocotpost

    def get_total_dos(self, plot=False, shift_by_fermi=True, plot_fermi=True,
                      energy_units='hartree'):
        """Extracts and possibly plots the total density of states.

        Reads the 'static/total-dos.dat' file, if available and returns the
        total density of states.

        Args:
            plot (bool): If True a basic plot will be returned.
            shift_by_fermi (bool): If True the energy will be shifted by the
                fermi energy (automatically extracted) for both the plot and
                the returned values.
            plot_fermi (bool): If True (and plot == True) a dashed line will
                be plotted as well where the fermi energy is.
            energy_units (str): Energy units to be plotted and returned.
                Options: 'hartree' (= Hartree), 'eV' (= Electron Volt)

        Returns:
            nd.array:
                2D array containing the enery in the units chosen in the first
                column and the density of states in the second.
            fig, ax:
                If plot == True the matplotlib handles for the plot will be
                returned as well.
        """

        file = 'total-dos.dat'
        dir_ = 'static'
        path = self.op._check_for_file(dir_, file)

        with open(path, 'r') as f:
            dos = np.loadtxt(f)

        fermi, dos, unit = self._dos_input_helper(
            dos, shift_by_fermi, plot_fermi, energy_units)

        if plot:
            fig, ax = self._dos_plot_helper(
                shift_by_fermi, plot_fermi, fermi, unit, axes=None)
            ax.set_title('Total Density of States')
            ax.plot(dos[:, 0], dos[:, 1], color='black', label='DOS')
            ax.legend()

            return dos, (fig, ax)

        else:
            return dos

    def get_band_dos(self, n_min=1, n_max=-1, plot=False,
                     shift_by_fermi=True, combined=False,
                     plot_fermi=True, energy_units='hartree', axes=None):
        """Extracts and possibly plots the band projected density of states.

        Reads the band specific dos files in 'static', if available and
        returns the total densities of states.

        Args:
            n_min (int): The lowest band number to be extracted.
            n_max (int): The highest band number to be extracted. -1 means
                all bands larger n_min in the directory will be used.
            plot (bool): If True a basic plot will be returned.
            shift_by_fermi (bool): If True the energy will be shifted by the
                fermi energy (automatically extracted) for both the plot and
                the returned values.
            combined (bool): Whether or not to combine all selected bands into
                a single total dos.
            plot_fermi (bool): If True (and plot == True) a dashed line will
                be plotted as well where the fermi energy is.
            energy_units (str): Energy units to be plotted and returned.
                Options: 'hartree' (= Hartree), 'eV' (= Electron Volt)
            axes (fig, ax): Matplotlib handles of a already existing plot to
                overlay the information of this onto it.

        Returns:
            nd.array:
                (n_max - n_min + 1)D array containing the energy in the units
                chosen in the first column and the density of states projected
                onto state i in the ith column.
            fig, ax:
                If plot == True the matplotlib handles for the plot will be
                returned as well.
        """

        dir_ = 'static'
        if n_max == -1:
            aux = sorted(
                glob.glob(str(self.op.root_path / dir_ / 'dos-*.dat')))[-1]
            n_max = int(aux[-8:-4])

        for i in range(n_min, n_max + 1):
            file = 'dos-' + f'{i}'.zfill(4) + '.dat'
            path = self.op._check_for_file(dir_, file)
            with open(path, 'r') as f:
                data = np.loadtxt(f)

            if i == n_min:
                dos = data

            else:
                dos = np.column_stack((dos, data[:, 1]))

        fermi, dos, unit = self._dos_input_helper(
            dos, shift_by_fermi, plot_fermi, energy_units)

        if plot:
            fig, ax = self._dos_plot_helper(
                shift_by_fermi, plot_fermi, fermi, unit, axes)
            ax.set_title('Band Resolved Density of States')

            if combined:
                dos[:, 1] = np.nansum(dos[:, 1:], axis=1)
                ax.plot(dos[:, 0], dos[:, 1],
                        label=fr'Combined Bands {n_min} to {n_max}')

            else:
                for i in range(n_max - n_min + 1):
                    ax.plot(dos[:, 0], dos[:, i + 1],
                            label=fr'Band {i + n_min}')

            ax.legend()

            return dos, (fig, ax)

        else:
            return dos

    def get_atomic_dos(self, atom, plot=False, shift_by_fermi=True,
                       plot_fermi=True, energy_units='hartree', axes=None,
                       combine_orbitals=True):
        """Extracts and possibly plots the atom projected density of states.

        Returns the density of states projected onto a specific atom.

        Args:
            atom (int): Number of the atom the DOS is to be returned.
            plot (bool): If True a basic plot will be returned.
            shift_by_fermi (bool): If True the energy will be shifted by the
                fermi energy (automatically extracted) for both the plot and
                the returned values.
            plot_fermi (bool): If True (and plot == True) a dashed line will
                be plotted as well where the fermi energy is.
            energy_units (str): Energy units to be plotted and returned.
                Options: 'hartree' (= Hartree), 'eV' (= Electron Volt)
            axes (fig, ax): Matplotlib handles of a already existing plot to
                overlay the information of this onto it.
            combine_orbitals (True): If True all the orbital projections will
                be summed up to a single density of states for this atom.

        Returns:
            nd.array:
                2D (if combine_orbitals) or (#orbitals of atom + 1)D array
                containing the energy in the units chosen in the first column
                and the density of states projected onto the orbitals or the
                entire atom in the remaining columns.
            fig, ax:
                If plot == True the matplotlib handles for the plot will be
                returned as well.
        """
        dir_ = 'static'
        paths = sorted(glob.glob(str(self.op.root_path /
                                     dir_ / ('pdos-at' +
                                             f'{atom}'.zfill(3) + '*.dat'))))

        orbitals = []
        for i in paths:
            orbitals.append(re.search(
                'pdos-at[0-9]{3}-(.*?).dat', i).groups()[0])

        for i, path in enumerate(paths):
            with open(path, 'r') as f:
                data = np.loadtxt(f)

            if i == 0:
                dos = data

            else:
                dos = np.column_stack((dos, data[:, 1]))

        fermi, dos, unit = self._dos_input_helper(
            dos, shift_by_fermi, plot_fermi, energy_units)

        if combine_orbitals:
            dos = np.column_stack((dos[:, 0], np.sum(dos[:, 1:], axis=1)))

        if plot:
            fig, ax = self._dos_plot_helper(
                shift_by_fermi, plot_fermi, fermi, unit, axes)
            ax.set_title(f'Atom {atom} Resolved Density of States')

            if combine_orbitals:
                ax.plot(dos[:, 0], dos[:, 1], label=fr'{atom}')

            else:
                for i in range(len(paths)):
                    ax.plot(dos[:, 0], dos[:, i + 1],
                            label=fr'Atom {atom} - Orbital {orbitals[i]}')

            ax.legend()

            return dos, (fig, ax)

        else:
            return dos

    def get_orbital_dos(self, orbital, plot=False, shift_by_fermi=True,
                        plot_fermi=True, energy_units='hartree', axes=None,
                        combine_atoms=True):
        """Extracts and possibly plots the orbital projected density of states.

        Returns and plots all the densities of states (possibly) combined
        projected onto a secific atom orbital.

        Args:
            orbital (str): Name of the atom orbital to be extracted in the
                form: 'element symbol' + 'energy level' + 'orbital type'.
                For example: Cu2p
            plot (bool): If True a basic plot will be returned.
            shift_by_fermi (bool): If True the energy will be shifted by the
                fermi energy (automatically extracted) for both the plot and
                the returned values.
            plot_fermi (bool): If True (and plot == True) a dashed line will
                be plotted as well where the fermi energy is.
            energy_units (str): Energy units to be plotted and returned.
                Options: 'hartree' (= Hartree), 'eV' (= Electron Volt)
            axes (fig, ax): Matplotlib handles of a already existing plot to
                overlay the information of this onto it.
            combine_atoms (bool): If true all atoms with such a orbital will
                be summed up to a single density of states.

        Returns:
            nd.array:
                2D (if combine_atoms) or (#orbitals of atom + 1)D array
                containing the energy in the units chosen in the first column
                and the density of states projected onto the orbitals or the
                entire atom in the remaining columns.
            fig, ax:
                If plot == True the matplotlib handles for the plot will be
                returned as well.
        """

        dir_ = 'static'
        paths = sorted(glob.glob(str(self.op.root_path / dir_ /
                                     ('pdos-at*' +
                                      f'{orbital}' + '.dat'))))

        atoms = []
        for i in paths:
            atoms.append(int(re.search(
                'pdos-at([0-9]{3})-.*?.dat', i).groups()[0]))

        for i, path in enumerate(paths):
            with open(path, 'r') as f:
                data = np.loadtxt(f)

            if i == 0:
                dos = data

            else:
                dos = np.column_stack((dos, data[:, 1]))

        fermi, dos, unit = self._dos_input_helper(
            dos, shift_by_fermi, plot_fermi, energy_units)

        if plot:
            fig, ax = self._dos_plot_helper(
                shift_by_fermi, plot_fermi, fermi, unit, axes)
            ax.set_title(f'Orbital {orbital} Resolved Density of States')

            if combine_atoms:
                dos[:, 1] = np.sum(dos[:, 1:], axis=1)
                ax.plot(dos[:, 0], dos[:, 1], label=fr'{orbital}')

            else:
                for i in range(len(paths)):
                    ax.plot(dos[:, 0], dos[:, i + 1],
                            label=fr'Atom {atoms[i]} - Orbital {orbital}')

            ax.legend()

            return dos, (fig, ax)

        else:
            return dos

    def _dos_input_helper(self, dos, shift_by_fermi, plot_fermi, energy_units):

        if shift_by_fermi or plot_fermi:
            fermi = self.op.get_fermi(energy_units)

        else:
            fermi = None

        if energy_units == 'eV':
            dos[:, 0] = units.energy(dos[:, 0], from_='hartree', to='eV')
            unit = 'eV'

        else:
            unit = 'Hartree'

        if shift_by_fermi:
            dos[:, 0] -= fermi
            fermi = 0

        return fermi, dos, unit

    def _dos_plot_helper(self, shift_by_fermi, plot_fermi, fermi, unit, axes):

        if axes is None:
            fig, ax = plt.subplots()

        else:
            fig, ax = axes

        if plot_fermi:
            ax.axvline(fermi, ls='--', color='lightgrey', label=r'$E_F$')

        if shift_by_fermi:
            ax.set_xlabel(fr'$E_B-E_F\;[\mathrm{{{unit}}}]$')

        else:
            ax.set_xlabel(fr'$E_B\;[\mathrm{{{unit}}}]$')
        ax.set_ylabel(r'$\mathrm{DOS}\;[\mathrm{arb. u.}]$')

        return fig, ax
