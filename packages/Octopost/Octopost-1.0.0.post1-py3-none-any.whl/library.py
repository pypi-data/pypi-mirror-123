# -*- coding: utf-8 -*-
"""Definition of various useful code snipets.
"""

# Third Party Imports
import numpy as np
from vtk import vtkStructuredGridReader
from vtk.util.numpy_support import vtk_to_numpy


def cartesian_to_spherical(x, y, z):
    """Converts cartesian coordinates to spherical ones::

        r = sqrt(x^2 + y^2 + z^2)
        theta = arccos(z / r)
        phi = arctan(y / x)

    Args:
        x (nd.array or float): x-Coordinate.
        y (nd.array or float): y-Coordinate.
        z (nd.array or float): z-Coordinate.

    Returns:
        nd.array or float:
            Radius.
        nd.array or float:
            Polar angle theta.
        nd.array or float:
            Azimuthal angle phi.
    """

    r = np.sqrt(x**2 + y**2 + z**2)

    theta = np.arccos(z / r)
    theta[np.isnan(theta)] = np.pi

    phi = np.arctan2(y, x)
    phi[phi < 0] += 2 * np.pi

    return r, theta, phi


def k_to_E(k):
    """Converts momentum to (kinetic) energy of an electron::

        E = m * v^2 / 2 = m * (k / m)^2 / 2 = k^2 / (2 * m)

    Args:
        k (nd.array or float): Momentum to be converted in atomic units.

    Returns:
        nd.array or float:
            Energy in atomic units.
    """

    return k**2 / 2


def E_to_k(E):
    """Converts (kinetic) energy (of an electron) to momentum::

        k = m * v = m * sqrt(2 * E / m) = sqrt(2 * E * m)

    Args:
        E (nd.array or float): Energy to be converted in atomic units.

    Returns:
        nd.array or float:
            Momentum in atomic units.
    """

    return np.sqrt(2 * E)


def find_nearest_index(array, value):
    """Finds the index of the closes element to 'value'.

    Args:
        array (nd.array): Array of values.
        value (float): Value to be located inside the array.

    Returns:
        int:
            Index of the element inside 'array' that is closest to 'value'.
    """

    idx = (np.abs(array - value)).argmin()
    return idx


def read_vtk_file(path, array_name):
    """Reads a .vtk file containing a structured grid.

    Args:
        path (str): Absolute path to the file that is to be read.
        array_name (str): Name of the array inside the file to be read.

    Returns:
        nd.array:
            4D array. Last dimension holds length 3 tuple with
            x, y and z coordinate for that point.
        nd.array:
            3D array with data at each point.
    """

    reader = vtkStructuredGridReader()
    reader.SetFileName(str(path))
    reader.Update()

    grid = reader.GetOutput().GetPoints().GetData()
    data = reader.GetOutput().GetPointData().GetArray(array_name)
    shape = np.array(reader.GetOutput().GetDimensions())
    grid = vtk_to_numpy(grid).reshape((*shape, 3), order='F')
    data = vtk_to_numpy(data).reshape(shape, order='F')

    return grid, data
