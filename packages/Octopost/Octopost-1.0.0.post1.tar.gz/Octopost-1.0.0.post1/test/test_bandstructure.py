# -*- coding: utf-8 -*-
from pathlib import Path

import octopost


def test_runs():

    dir_path = Path(__file__).parent
    op = octopost.Octopost(dir_path / '../demo/data/MoS2')

    op.get_bandstructure(plot=True)
    op.get_bandstructure(plot=False)
