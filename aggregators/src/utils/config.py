import os
import json
from exceptions.errors import *


class Config:
    def __init__(self):
        try:
            self.config_file = os.environ['BAR_CONFIG']
            self.barograph = None
            self.aggregate = None
        except(KeyError):
            raise VariableMissingError('Variable BAR_CONFIG missing')

    def load_resources(self):
        if not os.path.isfile(self.config_file):
            raise InvalidConfigFileError('Invalid config file')

        map_data = json.load(open(self.config_file))
        self.barograph = map_data['barograph']
        self.aggregate = map_data['aggregate']

    def get_barograph(self):
        if self.barograph == None:
            raise InvalidStateError(
                'Resources should be load before. \
                Use load_resources method before running it.')
        return self.barograph

    def get_aggregate(self):
        if self.aggregate == None:
            raise InvalidStateError(
                'Resources should be load before. \
                Use load_resources method before running it.')
        return self.aggregate
