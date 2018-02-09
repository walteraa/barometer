import json
import time
import requests


def http_callback(cluster_id, target,data):
    data['timestamp'] = int(time.time())
    data['cluster_id'] = cluster_id
    data.pop('_id')
    headers = {
        'Content-Type': 'application/json',
    }
    
    URI = "/metric"
    URL = "http://%s:%d%s"%(target['host'], target['port'], URI)
    print("Sending metric to %s"%URL)
    req = requests.post(url = URL, headers=headers, data = json.dumps(data))
    print(req.text)
