import os
import json

from boottimeagent.exceptions.errors import  *

class Config:
    def __init__(self):
        try:
            self.config_file = os.environ['BAR_CONFIG']
            self.map_data = None
        except(KeyError):
            raise VariableMissingError("Variable BAR_CONFIG missing")
        

    def load_resources(self):
        if not os.path.isfile(self.config_file):
            raise InvalidConfigFileError("Invalid config file")
            
        self.map_data = json.load(open(self.config_file))

    def get_os(self):
        if self.map_data == None:
            raise InvalidStateError("Resources should be load before. Use load_resources method before running it.")
        
        return self.map_data['os']
