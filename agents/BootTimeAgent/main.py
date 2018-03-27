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

    def __init__(self, conf, nova_client):
        self._conf = conf
        self._nova_client = nova_client

    def get_duration(self):
        return self._end - self._start

    def create_instance(self):
        instance_name = 'instance-monitor'
        try:
            flavor, image, network = self._get_vm_attributes()
            self.instance = self._nova_client.servers.create(
                name=instance_name,
                flavor=flavor,
                image=image,
                nics=[{'net-id':network.id}])
            self._check_nova_instance()
            send_boot_time(instance_name, self._conf.get_aggregate(), self.get_duration())
            self._delete_instance(self.instance)
        except Exception as e:
            raise VMCreationError("Cannot create vm %s (%s)" % (instance_name, e))

    def _delete_instance(self, instance):
        try:
            self._nova_client.servers.delete(instance.id)
        except Exception:
            raise VmDeleteError("Cannont delete vm (%s)" % (e))

    def _get_vm_attributes(self):
        try:
            image = self._nova_client.images.list()[0]
            flavor = self._nova_client.flavors.list()[3]
            network = self._nova_client.networks.list()[0]
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
    nova_client = NovaClient(conf).setup()
    monitor = BootTimeAgent(conf, nova_client)
    monitor.create_instance()
    print(monitor.get_duration())
