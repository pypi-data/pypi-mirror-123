# -*- coding: utf-8 -*-
from pathlib import Path
from pytest import approx

import octopost


def test_get_eigenvalues():

    dir_path = Path(__file__).parent
    op = octopost.Octopost(dir_path / '../demo/data/MoS2')

    eigenvalues = op.get_eigenvalues(n_max=None, k_point=1)

    assert(len(eigenvalues) == 13)

    eigenvalues = op.get_eigenvalues(n_max=1, k_point=3)
    assert(eigenvalues[0] == -2.433198)

    eigenvalues = op.get_eigenvalues(n_max=1, k_point=3, energy_units='eV')
    assert(eigenvalues[0] == approx(-66.21072162))


def test_get_fermi():

    dir_path = Path(__file__).parent
    op = octopost.Octopost(dir_path / '../demo/data/C60')

    fermi = op.get_fermi()
    assert(fermi == approx(-0.226267))
