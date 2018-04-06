import requests
from k8sdeployment.utils.config import *

def ack(config):
    
    URI = config['URI']
    
    headers = {
        'Connection': 'close'
    }

    URL = "http://%s:%d%s"%(config['host'], int(config['port']), URI)

    ok = range(200, 206)

    while requests.post(url=URL, headers=headers).status_code not in ok:
        pass

if __name__ == '__main__':
    conf = Config()
    conf.load_resources()
    ack(conf.get_info())
