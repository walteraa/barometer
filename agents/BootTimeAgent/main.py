import time
from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client

from boottimeagent.utils.config import *
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

    def check_nova_instance(self):
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

    def create_instance(self, flavor, image, network, instance_name='instance-monitor'):
        try:
            self.instance = self._nova_client.servers.create(
                name=instance_name,
                flavor=flavor,
                image=image,
                nics=[{'net-id':network.id}])
        except Exception as e:
            raise VMCreationError("Cannot create vm %s (%s)" % (instance_name, e)) 

if __name__ == '__main__':
    conf = Config()
    nova_client = NovaClient(conf).setup()
    monitor = BootTimeAgent(nova_client)
    img = nova_client.images.list()[0]
    fl = nova_client.flavors.list()[3]
    net = nova_client.networks.list()[0]
    monitor.create_instance(fl, img, net)
    monitor.check_nova_instance()
    print(monitor.get_duration())
