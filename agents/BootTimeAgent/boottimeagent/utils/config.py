import os
import json

from boottimeagent.exceptions.errors import  *

class Config:

    def __init__(self):
        self._load_resources()

    def _load_resources(self):
        self.map_data = {"os":{}, "aggregate":{}}
        try:
            self.map_data['os']['auth_url'] = os.environ['OS_AUTH_URL']
            self.map_data['os']['username'] = os.environ['OS_USERNAME']
            self.map_data['os']['password'] = os.environ['OS_PASSWORD']
            self.map_data['os']['project_id'] = os.environ['OS_PROJECT_ID']
            self.map_data['os']['user_domain_name'] = os.environ['OS_USER_DOMAIN_NAME']
            self.map_data['aggregate']['cluster_id'] = os.environ['CLUSTER_ID']
            self.map_data['aggregate']['host'] = os.environ['HOST']
            self.map_data['aggregate']['port'] = os.environ['PORT']
        except(KeyError):
            raise VariableMissingError("Variable  missing")

    def get_os(self):
        if self.map_data == None:
            raise InvalidStateError("Resources should be load before. Use load_resources method before running it.")
        
        return self.map_data['os']

    def get_aggregate(self):
        if self.map_data == None:
            raise InvalidStateError("Resources should be load before. Use load_resources method before running it.")

        return self.map_data['aggregate']
