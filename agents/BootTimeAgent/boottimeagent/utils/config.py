import json
import os

from boottimeagent.exceptions import errors


class Config:

    def __init__(self):
        try:
            self.config_file = os.environ['BAR_CONFIG']
            self.map_data = None
            self.targets = None
        except(KeyError):
            raise errors.VariableMissingError('Variable BAR_CONFIG missing')

    def load_resources(self):
        if not os.path.isfile(self.config_file):
            raise errors.InvalidConfigFileError('Invalid config file')
        self.map_data = json.load(open(self.config_file))

    def get_os(self):
        if self.map_data is None:
            raise errors.InvalidStateError(
                'Resources should be load before. \
                Use load_resources method before running it.')

        return self.map_data['os']

    def get_aggregate(self):
        if self.map_data is None:
            raise errors.InvalidStateError(
                'Resources should be load before. \
                Use load_resources method before running it.')

        return self.map_data['aggregate']
