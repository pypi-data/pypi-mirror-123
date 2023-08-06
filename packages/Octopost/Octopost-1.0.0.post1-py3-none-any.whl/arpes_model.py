# -*- coding: utf-8 -*-
"""Calculations related to the ARPES maps.

This module contains the 'ARPESModel' class, which handles all things
related to ARPES.
"""

# Python Imports
import glob
import warnings

# Third Party Imports
import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator

# Octopost Imports
import units
from library import (cartesian_to_spherical, E_to_k, k_to_E,
                     find_nearest_index, read_vtk_file)


class ARPESModel:
    """ARPES model handles all things related to ARPES.

    Should not be used directly by the user but called by the abstraction layer
    octopost class.

    Args:
        octopost (object): An instance of the octopost class.
    """

    def __init__(self, octopost):
        self.op = octopost

    def get_gasphase_arpes(self, file='PES_velocity_map.vtk',
                           E_num=10, E_range=[-10, 0], dE_b=0,
                           field='probe', omega=None, resolution=501,
                           out=False, out_file='output.hdf5'):
        """Calculates (kx, ky) ARPES maps at certain binding energies from a
        PES velocity file.

        Reads the PES velocity file specified with 'file' to calculate 'E_num'
        ARPES maps. The maps are calculated at binding energies specified in
        the semi open interval [E_range[0], E_range[1]). The energy of the
        incident light field can be specified via omega or read from the
        'parser.log' file by using the name 'field' the field was given.
        The resolution of each map is (resolution, resolution) and the data
        can be exported in a kMap.py compatible file 'out_file' using 'out'.

        Args:
            file (str): Relative path from the root directory of the
                calculation to the PES velocity map file (.vtk file).
            E_num (int): Number of energy cuts in the E_range interval.
            E_range (list): A list of length 2 specifying the semi-open
                interval [E_range[0], E_range[1]) of binding energies used for
                the energy cuts. All binding energies have to be E <= 0 and the
                units expected are 'eV'.
            dE_b (float): Integration over the open interval E_kin +- dE_b. In
                'eV'.
            field (str): Name the incident light field was given in the Octopus
                calculation. Is used to automatically find the photon energy of
                the incident light field. Can be overridden using 'omega'.
            omega (float): The energy of the incoming photon in 'eV'.
                Default is 'None', where Octopost tries to find the omega
                itself by reading the 'parser.log' file and looking up the
                field named 'field'.
            resolution (int): Resolution of the resulting maps. The maps have
                a equal resolution in kx and ky.
            out (bool): Whether or not to export the maps to a .hdf5 file. The
                file will contain the axis information and is compatible with
                kMap.
            out_file (str): If out is True the path to the output file
                relative to the root directory of the calculation.

        Returns:
            nd.array:
                A (E_num, resolution, resolution) shaped array. First
                index are the individual slices (even if E_num is 1). Second
                and third index are kx and ky respectively.
        Returns:
            nd.array:
                1D array containing the individual binding energies (not
                kinetic energy of the e) used for the slices in 'eV'.
            nd.array:
                1D array containing the kx (and therefore the identical
                ky) axis values in 1/Angstrom.
        """

        if omega is None:
            omega = self.op.parser.get_external_field(field)['omega']

        else:
            omega = units.energy(omega, from_='eV')

        E_range = units.energy(E_range, from_='eV')
        dE_b = units.energy(dE_b, from_='eV')
        E_axis = np.linspace(*E_range, E_num)
        # Maximum kinetic energy of photoelectron is energy of photon
        # plus the smallest (negative) binding energy
        E_kin_max = omega + max(E_range)
        slices = np.zeros((E_num, resolution, resolution))
        path = self.op._check_for_file('.', file)
        grid, intensity = read_vtk_file(path, array_name='PES_vel_map')
        # Grid from kx, ky, kz to v = |k|, theta, phi
        v, theta, phi = cartesian_to_spherical(
            grid[:, :, :, 0], grid[:, :, :, 1], grid[:, :, :, 2])
        v_axis = v[:, 0, 0]
        phi_axis = phi[0, :, 0]
        theta_axis = theta[0, 0, :]

        if theta_axis[-1] == 0:
            theta_axis[-1] = 2 * np.pi

        for i, E_b in enumerate(E_axis):
            E_kin = omega + E_b
            map_, k_axis = self._get_single_map(intensity, v_axis, theta_axis,
                                                phi_axis, E_kin, E_kin_max,
                                                dE_b, resolution)
            slices[i, :, :] = map_

        if out:
            self._write_sliced_data(out_file, slices, E_axis, k_axis)

        E_axis = units.energy(E_axis, from_='hartree')
        k_axis = units.inverse_length(k_axis, from_='bohr')

        return slices, E_axis, k_axis

    def get_3D_arpes(self, file='PES_velocity_map.vtk', E_num=10,
                     E_range=[-10, 0], dE_b=0, field='probe', omega=None,
                     out=False, out_file='output.hdf5'):
        """Calculates (kx, ky) ARPES maps at certain binding energies from a
        PES_ARPES file.

        Reads the PES ARPES file specified with 'file' to calculate 'E_num'
        ARPES maps. The maps are calculated at binding energies specified in
        the semi open interval [E_range[0], E_range[1]). The energy of the
        incident light field can be specified via omega or read from the
        'parser.log' file by using the name 'field' the field was given.
        The data can be exported in a kMap.py compatible file 'out_file'
        using 'out'.

        Args:
            file (str): Relative path from the root directory of the
                calculation to the PES velocity map file (.vtk file).
            E_num (int): Number of energy cuts in the E_range interval.
            E_range (list): A list of length 2 specifying the semi-open
                interval [E_range[0], E_range[1]) of binding energies used for
                the energy cuts. All binding energies have to be E <= 0 and the
                units expected are 'eV'.
            dE_b (float): Integration over the open interval E_kin +- dE_b. In
                'eV'.
            field (str): Name the incident light field was given in the Octopus
                calculation. Is used to automatically find the photon energy of
                the incident light field. Can be overridden using 'omega'.
            omega (float): The energy of the incoming photon in 'eV'.
                Default is 'None', where Octopost tries to find the omega
                itself by reading the 'parser.log' file and looking up the
                field named 'field'.
            out (bool): Whether or not to export the maps to a .hdf5 file. The
                file will contain the axis information and is compatible with
                kMap.
            out_file (str): If out is True the path to the output file
                relative to the root directory of the calculation.

        Returns:
            nd.array:
                A (E_num, resolution, resolution) shaped array. First
                index are the individual slices (even if E_num is 1). Second
                and third index are kx and ky respectively.
            nd.array:
                1D array containing the individual binding energies (not
                kinetic energy of the e) used for the slices in 'eV'.
            nd.array:
                1D array containing the kx (and therefore the identical
                ky) axis values in 1/Angstrom.
        """

        if omega is None:
            omega = self.op.parser.get_external_field(field)['omega']

        else:
            omega = units.energy(omega, from_='eV')

        E_range = units.energy(E_range, from_='eV')
        dE_b = units.energy(dE_b, from_='eV')
        Ebs = np.linspace(*E_range, E_num)

        path = self.op._check_for_file('.', file)
        grid, intensity = read_vtk_file(path, array_name='PES_vel_map')
        kx_axis = grid[:, 0, 0][:, 0]
        ky_axis = grid[0, :, 0][:, 1]
        E_axis = grid[0, 0, :][:, 2]

        slices = np.zeros((E_num, len(kx_axis), len(ky_axis)))
        for i, E_b in enumerate(Ebs):
            E_kin = omega + E_b
            map_ = self._cut_energy_3D(intensity, E_axis, E_kin, dE_b)
            slices[i, :, :] = map_

        if out:
            self._write_sliced_data(out_file, slices, E_axis, kx_axis)

        E_axis = units.energy(E_axis, from_='hartree')
        kx_axis = units.inverse_length(kx_axis, from_='bohr')
        ky_axis = units.inverse_length(ky_axis, from_='bohr')

        return slices, Ebs, kx_axis

    def get_state_resolved_arpes(self, states=-1, field='probe', omega=None,
                                 dE_b=0.02, resolution=501,
                                 out=False, out_file='output.hdf5'):
        """Calculate a state projected (kx, ky) ARPES map for each state.

        Using the state projected photoemission intensity files outputed by
        Octopus (if requested), for each state in 'states' the state projected
        ARPES map is calculated. The binding energy will be taken from the
        eigenvalues of the indiviudal states.

        Args:
            states (list): List of integers specifying the states to be used.
                For each entry a corresponding file has to be present. If -1
                all files found will be used. List can also contain the name
                of the orbital as string (e.g. 'HOMO-1')
            dE_b (float): See 'get_gasphase_arpes'.
            field (str): See 'get_gasphase_arpes'.
            omega (float): See 'get_gasphase_arpes'.
            resolution (int): See 'get_gasphase_arpes'
            out (bool): Whether or not to export the maps to a .hdf5 file. The
                file will contain the axis information and is compatible with
                kMap.
            out_file (str): If out is True the path to the output file
                relative to the root directory of the calculation.

        Returns:
            nd.array:
                A (E_num, resolution, resolution) shaped array. First
                index are the individual maps (even if len(states) is 1).
                Second and third index are kx and ky respectively.
            nd.array:
                1D array containing the individual binding energies (not
                kinetic energy of the e) used for the states in 'eV'.
            nd.array:
                1D array containing the kx (and therefore the identical
                ky) axis values in 1/Angstrom.
        """

        for i, state in enumerate(states):
            if type(state) is str:
                states[i] = self.op.get_orbital_state_number(state)

        if states == -1:
            aux = sorted(
                glob.glob(str(self.op.root_path /
                              'PES_velocity_map-st*.vtk')))
            states = [int(i[-8:-4]) for i in aux]

        E_bs = self.op.get_eigenvalues(n_max=states[-1], n_min=states[0],
                                       energy_units='eV')

        slices = np.zeros((len(states), resolution, resolution))
        for i, (state, E_b) in enumerate(zip(states, E_bs)):
            file = f'PES_velocity_map-st{state:04}.vtk'
            slice_, E_axis, k_axis = self.get_gasphase_arpes(
                file=file, E_num=1, E_range=[E_b, E_b], dE_b=dE_b,
                field=field, omega=omega, resolution=resolution)
            slices[i, :, :] = slice_

        if out:
            self._write_sliced_data(out_file, slices, E_bs, k_axis)

        return slices, np.array(E_bs), k_axis

    def get_gasphase_pes(self, file, integrate=('theta', 'phi'), plot=False):
        """Returns photoemission intensity.

        Reads the photoemission intensity from 'file' and, if requested,
        integrates over 0,1, 2 or all dimensions. Option to plot is only
        available for integration over 2 dimensions.

        Args:
            file (str): Relative path from the root directory of the
                calculation to the PES velocity map file (.vtk file).
            integrate (list): List containing any combination of 'theta',
                'phi' and 'energy' including empty and all of them. The
                dimensions specified will be integrated over.
            plot (bool): If len(integrate) != 2 this option will be ignored.
                Otherwise a basic line plot over the remaining dimension will
                be returned.

        Returns:
            nd.array or float:
                The intensity integrated over the dimensions
                specified in arbitrary units. If integrated over all
                dimensions this will be a float, otherwise a nd.array with
                3 - len(integrate) dimensions. The first dim will be 'energy'
                or, if integrated over, 'phi'. The last dim will be 'theta' or,
                if integrated over, 'phi'.
            tuple or nd.array:
                Remaining axes in the correct order. If only
                one remains this will be a nd.array, if none remains no return
                value and otherwise a tuple of axes.
            fig, ax:
                If plot == True and integration over two dimensions, the
                handles for the matplotlib plot.
        """

        path = self.op._check_for_file('.', file)
        grid, intensity = read_vtk_file(path, array_name='PES_vel_map')
        v, theta, phi = cartesian_to_spherical(
            grid[:, :, :, 0], grid[:, :, :, 1], grid[:, :, :, 2])
        E_axis = units.energy(k_to_E(v[:, 0, 0]), from_='hartree')
        phi_axis = phi[0, :, 0]
        theta_axis = theta[0, 0, :]

        if 'theta' in integrate:
            intensity = np.sum(intensity, axis=2)
            theta_axis = False

        if 'phi' in integrate:
            intensity = np.sum(intensity, axis=1)
            phi_axis = False

        if 'energy' in integrate:
            intensity = np.sum(intensity, axis=0)
            E_axis = False

        if np.isscalar(intensity):
            return intensity

        elif intensity.ndim == 3:
            return intensity, (E_axis, phi_axis, theta_axis)

        elif intensity.ndim == 2:

            if theta_axis is False:
                return intensity, (E_axis, phi_axis)

            elif phi_axis is False:
                return intensity, (E_axis, theta_axis)

            else:
                return intensity, (phi_axis, theta_axis)

        else:
            if plot:
                fig, ax = plt.subplots()
                ax.set_ylabel('$I$ (a.u.)', fontsize=14)

                if theta_axis is not False:
                    ax.plot(theta_axis, intensity)
                    ax.set_xlabel(r'$\theta$ (rad)', fontsize=14)

                    return intensity, theta_axis, (fig, ax)

                if phi_axis is not False:
                    ax.plot(phi_axis, intensity)
                    ax.set_xlabel(r'$\phi$ (rad)', fontsize=14)

                    return intensity, phi_axis, (fig, ax)

                else:
                    ax.plot(E_axis, intensity)
                    ax.set_xlabel(r'$E_{kin}$ (eV)', fontsize=14)

                    return intensity, E_axis, (fig, ax)

            else:
                return intensity, E_axis

    def get_3D_pes(self, file, plot=False):
        """Returns photoemission intensity over the energy.

        Args:
            file (str): Relative path from the root directory of the
                calculation to the PES velocity map file (.vtk file).
            plot (bool): If len(integrate) != 2 this option will be ignored.
                Otherwise a basic line plot over the remaining dimension will
                be returned.

        Returns:
            nd.array:
                The intensity integrated over the kx and ky axes.
            nd.array:
                The energy axis in eV.
                fig, ax: If plot == True and integration over two dimensions,
                the handles for the matplotlib plot.
        """

        path = self.op._check_for_file('.', file)
        grid, intensity = read_vtk_file(path, array_name='PES_vel_map')
        E_axis = units.energy(grid[0, 0, :][:, 2], from_='hartree')

        intensity = np.sum(intensity, axis=(0, 1))

        if plot:
            fig, ax = plt.subplots()
            ax.set_xlabel(r'$E_{kin}$ (eV)', fontsize=14)
            ax.set_ylabel('$I$ (a.u.)', fontsize=14)
            ax.plot(E_axis, intensity)

            return intensity, E_axis, (fig, ax)

        else:
            return intensity, E_axis

    def get_arpes_plot(self, map_, k_axis):
        """Convenience method to plot a ARPES map.

        Uses the output of 'get_gasphase_arpes' to quickly plot an ARPES map.

        Args:
            map_ (nd.array): 2D array containing the ARPES map.
            k_axis (nd.array): 1D array containing the kx and ky axis in 1/A.

        Returns:
            fig, ax:
                Matplotlib handles for the plot.
        """

        fig, ax = plt.subplots()
        ax.imshow(map_, extent=(k_axis[0], k_axis[-1], k_axis[0], k_axis[-1]))
        ax.set_xlabel('$k_x$ (1/A)', fontsize=14)
        ax.set_ylabel('$k_y$ (1/A)', fontsize=14)

        return fig, ax

    def get_arpes_bandstructure(self, file='PES_ARPES.path', k_points=[],
                                labels=[], omega=None, field='probe',
                                plot=True, plot_fermi=True, plot_points=True,
                                axes=None):
        """Reads the ARPES intensity for a path through the first Brillouin
        zone, i.e. the bandstructure.

        Reads the PES_ARPES.path file which contains the intensity of the
        photoemission process for a path through the first Brillouin zone.
        In theory this should resemble the bandstructure.

        Args:
            file (str): Relative path from the root directory of the
                calculation to the PES velocity map file (.vtk file).
            k_points (list): A list of special points (e.g. 'Γ', 'K' or other)
                in terms of steps from the last point (same as in 'inp' file).
                Sum of all steps needs to be total number of steps, i.e. one
                less than total number of points. If list is empty octopost
                tries to find the path information from the parser.log.
            labels (list): A list of strings with the same length as k_points.
                Specifies a label in the plot for each point in k_points. Use
                empty string if no label (and line) is required.
            omega (float): The photon energy in eV. If None is passed octopost
                tries to find the energy from parser.log.
            field (str): Name of the external field octopost tries to find the
                photon energy by if not explicitly passed.
            plot (bool): Whether to return a basic plot.
            plot_fermi (bool): Plot a dashed line indicating the fermi energy.
            plot_points (bool): Plot dashed line at each special point along
                the path that has a non empty label.
            axes (fig, ax): Matplotlib handles to lay the plot on.

        Returns:
            nd.array:
                A nd.array with the k path through from the starting point in
                one over Angstrom.
            nd.array:
                2D array with the intensity for each energy and k point.
            fig, ax:
                Matplotlib handles for the plot.
        """

        dir_ = '.'
        path = self.op._check_for_file(dir_, file)

        if not k_points:
            k_points = self.op.parser.get_k_path()
        elif type(k_points) is int:
            k_points = [k_points]

        if omega is None:
            omega = self.op.parser.get_external_field(field)['omega']

        total_k_points = np.sum(k_points) + 1
        data = np.reshape(np.loadtxt(path), (total_k_points, -1, 5))
        path = units.inverse_length(data[:, 0, 0], from_='bohr')
        # Shift the energy by the photon energy
        energy = units.energy(data[0, :, 3], from_='hartree') - omega
        data = data[:, :, 4].T

        if not plot:
            return path, data

        if axes:
            fig, ax = axes

        else:
            fig, ax = plt.subplots()

        ax.imshow(data, origin='lower', aspect='auto',
                  extent=(path[0], path[-1], energy[0], energy[-1]))

        if plot_fermi:
            fermi = self.op.get_fermi(energy_units='eV')
            ax.axhline(fermi, linestyle='--', color='k')

        if plot_points:
            total_point_pointer = 0
            for i, point in enumerate(k_points):
                total_point_pointer += point
                if labels and labels[i] != '':
                    ax.axvline(path[total_point_pointer],
                               linestyle='--', color='k')
                    ax.text(path[total_point_pointer], -0.05, labels[i],
                            transform=ax.get_xaxis_transform(),
                            ha='center', va='top')

        ax.set_xlabel('k_{||} (1/A)', labelpad=20)
        ax.set_ylabel('E (eV)')

        return path, data, (fig, ax)

    def _get_single_map(self, intensity, v_axis, theta_axis, phi_axis, E_kin,
                        E_kin_max, dE_b, resolution):
        """Private helper method to calculate APRES from for single binding
        energy.

        Should not be used directly. Please refer to the 'get_gasphase_arpes'
        function instead.
        """

        intensity_cut = self._cut_energy_gasphase(intensity, v_axis, E_kin,
                                                  dE_b)
        phi_axis_connect, intensity_cut = self._connect_phi(
            phi_axis, theta_axis, intensity_cut)
        map_, k_axis = self._interp_spherical_to_cartesian(
            intensity_cut, theta_axis, phi_axis_connect,
            E_kin_max, resolution)

        return map_, k_axis

    def _cut_energy_gasphase(self, intensity, v_axis, E_kin, dE_b=0):
        """Private helper method to cut a single energy slice from data.

        Cuts a hemisphere at E_kin from the intensity data. If dE_b is not 0,
        then there will be a integration of a the radius E_kin +- dE_b.
        Should not be used directly. Please refer to the 'get_gasphase_arpes'
        function instead.
        """

        if dE_b != 0:
            mask = np.where((v_axis < E_to_k(E_kin + dE_b)) &
                            (v_axis > E_to_k(E_kin - dE_b)))[0]

        if dE_b == 0 or len(mask) == 0:
            if dE_b != 0:
                # => len(mask) == 0
                print('WARNING: No energy slice inside (E-dE, E+dE).')

            k_at_cut = E_to_k(E_kin)
            idx = find_nearest_index(v_axis, k_at_cut)
            return intensity[idx, :, :]

        return np.sum(intensity[mask, :, :], axis=0)

    def _cut_energy_3D(self, intensity, E_axis, E_kin, dE_b=0):
        """Private helper method to cut a single energy slice from data.

        Cuts at a certain E_kin from the intensity data. If dE_b is not 0,
        then there will be a integration of a the radius E_kin +- dE_b.
        Should not be used directly. Please refer to the 'get_3D_arpes'
        function instead.
        """

        if dE_b != 0:
            mask = np.where((E_axis < (E_kin + dE_b)) &
                            (E_axis > (E_kin - dE_b)))[0]

        if dE_b == 0 or len(mask) == 0:
            if dE_b != 0:
                # => len(mask) == 0
                print('WARNING: No energy slice inside (E-dE, E+dE).')

            idx = find_nearest_index(E_axis, E_kin)
            return intensity[:, :, idx]

        return np.sum(intensity[:, :, mask], axis=2)

    def _write_sliced_data(self, file, slices, E_axis, k_axis):
        """Private helper method to write a kMap.py combatible .hdf5 file.

        Should not be used directly. Please refer to the 'get_gasphase_arpes'
        function instead.
        """

        with h5py.File(self.op.root_path / file, 'w') as f:
            f.create_dataset('name', data='Test Export')
            f.create_dataset('axis_1_label', data='Binding Energy')
            f.create_dataset('axis_2_label', data='k_x')
            f.create_dataset('axis_3_label', data='k_y')
            f.create_dataset('axis_1_units', data='eV')
            f.create_dataset('axis_2_units', data='1/A')
            f.create_dataset('axis_3_units', data='1/A')

            axis_1_range = units.energy([np.nanmin(E_axis), np.nanmax(E_axis)])
            axis_2_range = units.inverse_length(
                [np.nanmin(k_axis), np.nanmax(k_axis)])
            f.create_dataset('axis_1_range', data=axis_1_range)
            f.create_dataset('axis_2_range', data=axis_2_range)
            f.create_dataset('axis_3_range', data=axis_2_range)
            f.create_dataset(
                'data', data=slices, dtype='f8', compression='gzip',
                compression_opts=9)

        return

    def _connect_phi(self, phi_axis, theta_axis, intensity):
        """Private helper method to complete the phi coordinate.

        The phi coordinate runs in the interval [0, 2pi). The points at 2pi
        has no further information (is identical to 0) but for plotting the
        phi coordinate should run in a closed interval.
        Should not be used directly. Please refer to the 'get_gasphase_arpes'
        function instead.
        """

        phi_axis = np.append(phi_axis, 2 * np.pi)
        intensity = np.vstack((intensity, intensity[0, :]))

        return phi_axis, intensity

    def _interp_spherical_to_cartesian(self, intensity, theta_axis,
                                       phi_axis, E_max, resolution):
        """Private helper method to interpolate a hemispherical energy cut
        down to a regular x,y grid.

        Should not be used directly. Please refer to the 'get_gasphase_arpes'
        function instead.
        """
        interp = RegularGridInterpolator(
            (phi_axis, theta_axis), intensity,
            bounds_error=False, fill_value=np.nan)
        k_max = E_to_k(E_max)
        # x and y axis for the new kx, ky grid
        k_axis = np.linspace(-k_max, k_max, resolution)
        KX, KY = np.meshgrid(k_axis, k_axis)
        # k_max is equivalent to the radius of the energy cut
        # Spherical coordinates for the new grid
        phi_new = np.arctan2(KY, KX)
        # Transform phi from [-pi,pi] to [0,2 pi] range
        # since phi runs from [0,2pi] in OCTOPUS
        phi_new += np.pi
        k = np.sqrt(KX**2 + KY**2)

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            theta_new = np.arcsin(k / k_max)

        points = np.reshape(np.stack((phi_new, theta_new)), (2, -1)).T

        map_ = np.reshape(interp(points), (len(k_axis), len(k_axis)))
        # Compensate phi transformation above
        map_ = np.rot90(map_, 2)

        return map_, k_axis
