import time
from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client

from boottimeagent.utils.config import *
from boottimeagent.utils.network import *
from boottimeagent.exceptions import errors


class NovaClient(object):

    def __init__(self, config):
        self._config = config.get_os()

    def setup(self, api_version=2.1):
        loader = loading.get_plugin_loader('password')
        auth = loader.load_from_options(auth_url=self._config['auth_url'],
                                        username=self._config['username'],
                                        password=self._config['password'],
                                        project_id=self._config['project_id'],
                                        user_domain_name=self._config['user_domain_name'])
        sess = session.Session(auth=auth)
        nova_client = client.Client(api_version, session=sess)
        return nova_client


class BootTimeAgent(object):

    def __init__(self, nova_client):
        self._nova_client = nova_client

    def get_duration(self):
        return self._end - self._start

    def create_instance(self):
        try:
            flavor, image, network = self._get_vm_attributes()

            self.instance = self._nova_client.servers.create(
                name='instance-monitor',
                flavor=flavor,
                image=image,
                nics=[{'net-id':network.id}])
            self._check_nova_instance()
        except Exception as e:
            raise VMCreationError("Cannot create vm %s (%s)" % (instance_name, e))

    def _get_vm_attributes(self):
        try:
            image = nova_client.images.list()[0]
            flavor = nova_client.flavors.list()[3]
            network = nova_client.networks.list()[0]
        except Exception as e:
            raise RetrieveAttributesError("Error fetching vm attributes: %"
                                         % e)
        return flavor, image, network

    def _check_nova_instance(self):
        self._start = time.time()
        active = False
        while not active:
            if self._instance_status() == 'ACTIVE':
                active = True
                self._end = time.time()

    def _instance_status(self):
        status = None
        try:
            status = self._nova_client.servers.get(self.instance.id).status
        except Exception as e:
            raise VMStatusError("Problem getting status of vm: %s"
                                % e)
        return status


if __name__ == '__main__':
    conf = Config()
    conf.load_resources()
    nova_client = NovaClient(conf).setup()
    monitor = BootTimeAgent(nova_client)
    monitor.create_instance()
    send_boot_time(conf.get_aggregate(), monitor.get_duration())
    print(monitor.get_duration())
