import os
import json
from exceptions.errors import *
from utils.target import *

class Config:
    def __init__(self):
        try:
            self.config_file = os.environ['BAR_CONFIG']
            self.map_data = None
            self.targets = None
        except(KeyError):
            raise VariableMissingError("Variable BAR_CONFIG missing")
        

    def load_resources(self):
        if not os.path.isfile(self.config_file):
            raise InvalidConfigFileError("Invalid config file")
            
        self.map_data = json.load(open(self.config_file)) 

    def get_targets(self):
        if self.map_data == None:
            raise InvalidStateError("Resources should be load before. Use load_resources method before running it.")

        if self.targets == None:
            self.targets = list(
                    map(
                        lambda t: Target(t['host'], t['machine_id'], t['description']),
                        self.map_data['targets'])
                    )
        return self.targets
                
    def get_aggregate(self):
        if self.map_data == None:
            raise InvalidStateError("Resources should be load before. Use load_resources method before running it.")
        
        return self.map_data['aggregate']
