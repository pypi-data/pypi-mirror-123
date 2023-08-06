# -*- coding: utf-8 -*-
"""Calculations related to the bandstructure.

This module contains the 'BandstructureModel' class, which handles all things
related to the bandstructure.
"""

# Third Party Imports
import numpy as np
import matplotlib.pyplot as plt

# Own Imports
import units


class BandstructureModel:
    """Bandstructure model handles all things related to the bandstructure.

    Should not be used directly by the user but called by the abstraction layer
    octopost class.

    Args:
        octopost (object): An instance of the octopost class.
    """

    def __init__(self, ocotpost):
        self.op = ocotpost

    def get_bandstructure(self, bands=None, plot=False, energy_units='eV'):
        """Returns the bandstructure.

        Reads the 'bandstructure' file found in 'static/' and returns the path
        along the k points as coordinate and (kx, ky, kz) as well as the bands.
        Optionally a pre-made standard plot can be returned as well.

        Args:
            bands (list): List of band indices to be returned. Pass None for
                all bands.
            plot (bool): Returns matplotlib handles for a basic plot of the
                bandstructure.
            energy_units (str): Energy units to be plotted and returned.
                Options: 'hartree' (= Hartree), 'eV' (= Electron Volt)

        Returns:
            nd.array:
                Numpy array with all k-points. First column is
                the coordinate, remaining columns are kx, ky, kz.
            nd.array:
                Numpy array with each column being one band.
            fig, ax:
                Matplotlib handles for the plot. Only returned if
                plot==True.
        """

        file = 'bandstructure'
        dir_ = 'static'
        path = self.op._check_for_file(dir_, file)

        with open(path, 'r') as f:
            data = np.loadtxt(f)

        # First column == coordinate along path in k-space
        # Second to Fourth column = (kx, ky, kz) of coordinate in k-space
        # Fith column onwards = individual bands
        k_path = data[:, :4]
        band_data = data[:, 4:]

        if bands is not None:
            band_data = band_data[:, bands]

        if energy_units == 'eV':
            band_data = units.energy(band_data, from_='hartree')
            E_label = 'E (eV)'

        else:
            E_label = 'E (Hartree)'

        if plot:
            fig, ax = plt.subplots()
            for i in range(0, band_data.shape[1]):
                ax.plot(k_path[:, 0], band_data[:, i])

            ax.set_xlabel(r'% of path', fontsize=14)
            ax.set_ylabel(E_label, fontsize=14)

            return k_path, band_data, (fig, ax)

        else:
            return k_path, band_data
