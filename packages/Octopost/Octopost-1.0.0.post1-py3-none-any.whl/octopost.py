# -*- coding: utf-8 -*-

import os
from pathlib import Path

from dos_model import DOSModel
from input_parser import Parser
from arpes_model import ARPESModel
from output_read_model import OutputReadModel
from bandstructure_model import BandstructureModel


class Octopost():

    def __init__(self, root=''):

        self.set_root(root)

    def set_root(self, root):
        self.root_path = self._validate_source_directory(root)

        try:
            self.parser = Parser(self)

        except FileNotFoundError:
            pass

    def get_bandstructure(self, *args, **kwargs):

        if not hasattr(self, 'bandstructure_model'):
            self.bandstructure_model = BandstructureModel(self)

        return self.bandstructure_model.get_bandstructure(*args, **kwargs)

    def get_fermi(self, *args, **kwargs):

        if not hasattr(self, 'output_read_model'):
            self.output_read_model = OutputReadModel(self)

        return self.output_read_model.get_fermi(*args, **kwargs)

    def get_eigenvalues(self, *args, **kwargs):

        if not hasattr(self, 'output_read_model'):
            self.output_read_model = OutputReadModel(self)

        return self.output_read_model.get_eigenvalues(*args, **kwargs)

    def get_orbital_state_number(self, *args, **kwargs):

        if not hasattr(self, 'output_read_model'):
            self.output_read_model = OutputReadModel(self)

        return self.output_read_model.get_orbital_state_number(*args, **kwargs)

    def get_convergence(self, *args, **kwargs):

        if not hasattr(self, 'output_read_model'):
            self.output_read_model = OutputReadModel(self)

        return self.output_read_model.get_convergence(*args, **kwargs)

    def get_cell(self, *args, **kwargs):

        if not hasattr(self, 'output_read_model'):
            self.output_read_model = OutputReadModel(self)

        return self.output_read_model.get_cell(*args, **kwargs)

    def get_reciprocal_cell(self, *args, **kwargs):

        if not hasattr(self, 'output_read_model'):
            self.output_read_model = OutputReadModel(self)

        return self.output_read_model.get_reciprocal_cell(*args, **kwargs)

    def get_first_brillouin(self, *args, **kwargs):

        if not hasattr(self, 'output_read_model'):
            self.output_read_model = OutputReadModel(self)

        return self.output_read_model.get_first_brillouin(*args, **kwargs)

    def plot_reciprocal(self, *args, **kwargs):

        if not hasattr(self, 'output_read_model'):
            self.output_read_model = OutputReadModel(self)

        return self.output_read_model.plot_reciprocal(*args, **kwargs)

    def get_total_dos(self, *args, **kwargs):

        if not hasattr(self, 'dos_model'):
            self.dos_model = DOSModel(self)

        return self.dos_model.get_total_dos(*args, **kwargs)

    def get_band_dos(self, *args, **kwargs):

        if not hasattr(self, 'dos_model'):
            self.dos_model = DOSModel(self)

        return self.dos_model.get_band_dos(*args, **kwargs)

    def get_atomic_dos(self, *args, **kwargs):

        if not hasattr(self, 'dos_model'):
            self.dos_model = DOSModel(self)

        return self.dos_model.get_atomic_dos(*args, **kwargs)

    def get_orbital_dos(self, *args, **kwargs):

        if not hasattr(self, 'dos_model'):
            self.dos_model = DOSModel(self)

        return self.dos_model.get_orbital_dos(*args, **kwargs)

    def get_gasphase_arpes(self, *args, **kwargs):

        if not hasattr(self, 'arpes_model'):
            self.arpes_model = ARPESModel(self)

        return self.arpes_model.get_gasphase_arpes(*args, **kwargs)

    def get_3D_arpes(self, *args, **kwargs):

        if not hasattr(self, 'arpes_model'):
            self.arpes_model = ARPESModel(self)

        return self.arpes_model.get_3D_arpes(*args, **kwargs)

    def get_state_resolved_arpes(self, *args, **kwargs):

        if not hasattr(self, 'arpes_model'):
            self.arpes_model = ARPESModel(self)

        return self.arpes_model.get_state_resolved_arpes(*args, **kwargs)

    def get_gasphase_pes(self, *args, **kwargs):

        if not hasattr(self, 'arpes_model'):
            self.arpes_model = ARPESModel(self)

        return self.arpes_model.get_gasphase_pes(*args, **kwargs)

    def get_3D_pes(self, *args, **kwargs):

        if not hasattr(self, 'arpes_model'):
            self.arpes_model = ARPESModel(self)

        return self.arpes_model.get_3D_pes(*args, **kwargs)

    def get_arpes_plot(self, *args, **kwargs):

        if not hasattr(self, 'arpes_model'):
            self.arpes_model = ARPESModel(self)

        return self.arpes_model.get_arpes_plot(*args, **kwargs)

    def get_arpes_bandstructure(self, *args, **kwargs):

        if not hasattr(self, 'arpes_model'):
            self.arpes_model = ARPESModel(self)

        return self.arpes_model.get_arpes_bandstructure(*args, **kwargs)

    def _validate_source_directory(self, root):

        try:
            # TODO: Check validity
            return Path(root).resolve()

        except (RuntimeError, FileNotFoundError):
            print('Invalid source directory.')
            raise FileNotFoundError

    def _check_for_file(self, dir_, file):

        path = self.root_path / dir_ / file
        if os.path.isfile(path):
            return path

        else:
            raise FileNotFoundError
