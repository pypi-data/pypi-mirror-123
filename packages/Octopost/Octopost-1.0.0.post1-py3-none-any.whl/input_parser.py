# -*- coding: utf-8 -*-
"""Parser for the input of the Octopus calculation.

A small text parser specifically for the 'parser.log' file of a Octopus
calculation containing the inputs done by the user. Used for automatic
extraction of certain values necessary for the data post processing.
"""

# Python Imports
import re


class Parser():
    """Textparser class.

    Args:
        octopost (object): An instance of the octopost class.

    Attributes:
        input (dict): A dictionary containing all parsed variables from the
            parser.log file. Public to directly access not yet abstracted
            variables.
    """

    def __init__(self, ocotpost):

        self.op = ocotpost
        self.input = {}

        self._parse()

    def get_external_field(self, field):
        """Returns the external filed specified in the Octopus calculation.

        Args:
            field (str): Each field in a Octopus calculation is given a name.
                This name is used to find the field data.

        Returns:
            dict:
                All available data to this field in form of a dictionary. The
                available keys depend on the type of field. For more
                information please see the Octopus documentation:
                https://octopus-code.org/doc/11.1/html/vars.php?page=alpha
        """

        field_key = None
        field = f'"{field}"'
        for key, _ in self.input.items():
            if key.startswith('TDExternalFields') and self.input[key] == field:
                field_key = key
                name_index = re.search(
                    r'TDExternalFields\[[0-9]+\]\[([0-9]+)\]',
                    field_key).group(1)
                type_ = 'scalar' if name_index == 2 else 'vector'

        if field_key is None:
            print('ERROR: Field not found in parser.log file.')
            raise ValueError

        else:
            field_number = re.search(
                r'TDExternalFields\[([0-9]+)\]', field_key).group(1)

        if type_ == 'scalar':
            keys = ('scalar_potential', 'spatial_expression',
                    'omega', 'envelope_function_name', 'phase')
        else:
            keys = ('type', 'nx', 'ny', 'nz', 'omega',
                    'envelope_function_name', 'phase')

        field_dict = {}
        for i, key in enumerate(keys):
            try:
                field_dict.update({key: self.input[
                    f'TDExternalFields[{field_number}][{i}]']})

            except KeyError:
                if key == 'phase':
                    # Phase is an optional parameter
                    pass
                else:
                    print(f'The key "{key}" was has not been found for the '
                          f'external field {field}')
                    raise KeyError

        return field_dict

    def get_k_path(self):

        k_points = []
        for key, _ in self.input.items():
            if key.startswith('KPointsPath[0]'):
                k_points.append(int(self.input[key]) + 1)

        return k_points

    def _parse(self):

        file = 'parser.log'
        dir_ = 'exec'
        path = self.op._check_for_file(dir_, file)

        with open(path) as f:
            for line in f:
                if line == '' or line[0] == '#':
                    pass

                else:
                    aux = self._parse_line(line)

                    if aux:
                        self.input.update(aux)

    def _parse_line(self, line):

        if('=' in line):
            groups = re.search('(.*) = (.+?)[\t+|\n#]', line).groups()
            key = groups[0]

            try:
                value = int(groups[1])

            except ValueError:
                try:
                    value = float(groups[1])

                except ValueError:
                    value = groups[1]

            return {key: value}

        else:
            return False
