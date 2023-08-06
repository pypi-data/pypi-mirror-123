# -*- coding: utf-8 -*-
"""Definition of various useful units used for conversion.

Source for all values unless specified otherwise:
https://physics.nist.gov/cuu/Constants/index.html

Attributes:
    bohr (float): Bohr atomic radius in [Angstrom].
    hartree (float): Hartree in [eV].
    m_e (float): Electron mass in [kg].
    e (float): Elementary charge in [Coulomb].
"""

# Third Party Imports
import numpy as np

bohr = 0.529177210903
hartree = 27.211386245988
m_e = 9.1093837015e-31
e = 1.602176634e-19


def energy(data, from_='hartree', to='eV'):
    """Converts energy units.

    Args:
        data (float or list): The initual value to be converted in units
            'from\_'.
        from\_ (str): The unit of the values supplied. Available options are:
            'hartree' (= Hartree), 'eV' (= Electron Volt).
        to (str): The unit of the output. Available options are:
            'hartree', 'eV'.

    Returns:
        float or list:
            The data but converted from 'from\_' to 'to'.
    """

    available_units = ('hartree', 'eV')
    if from_ not in available_units or to not in available_units:
        print('Unit requested or supplied not supported.')
        raise ValueError

    if from_ == 'hartree':
        return np.array(data) * hartree

    else:
        return np.array(data) / hartree


def inverse_length(data, from_='bohr', to='A'):
    """Converts inverse length (reciprocal distance).

    Args:
        data (float or list): The initual value to be converted in units
            'from\_'.
        from\_ (str): The unit of the values supplied. Available options are:
            'bohr' (= 1/Bohr radius), 'A' (= 1/Angstrom).
        to (str): The unit of the output. Available options are:
            'bohr' (= 1/Bohr radius), 'A' (= 1/Angstrom).

    Returns:
        float or list:
            The data but converted from 'from\_' to 'to'.
    """

    available_units = ('bohr', 'A')
    if from_ not in available_units or to not in available_units:
        print('Unit requested or supplied not supported.')
        raise ValueError

    if from_ == 'bohr':
        return np.array(data) / bohr

    else:
        return np.array(data) * bohr
