import json
import time

import requests


def send_target_request(target):
    headers = {'Connection': 'close'}
    URL = 'http://%s:%d%s' % (target['host'],
                              int(target['port']), target['URI'])
    resp = requests.get(url=URL, headers=headers)
    print(resp.text)
    if resp.ok:
        return resp.json()
    else:
        return json.dumps({'Total': 0})


def send_sensor_data(target, aggregate, monitoring_data):
    agent_type = {'sensor': 'sensor', 'metric': 'number-macs'}
    data = monitoring_data['Total']
    # Preparing the data to be sent
    json_map = {}
    json_map['machine_id'] = target['host']
    json_map['time_stamp'] = int(time.time())
    json_map['sensor_name'] = agent_type['sensor']
    json_map['metric_name'] = agent_type['metric']
    json_map['value_type'] = type(data).__name__
    json_map['metric_value'] = data
    json_map['cluster_id'] = aggregate['cluster_id']

    print('sending HTTP to: %s:%d with data: %s' %
          (aggregate['host'], int(aggregate['port']), json.dumps(json_map)))

    # TODO: Add it for a constant
    URI = '/metric'

    headers = {
        'Content-Type': 'application/json',
    }

    URL = 'http://%s:%d%s' % (aggregate['host'], int(aggregate['port']), URI)
    req = requests.post(url=URL, headers=headers, data=json.dumps(json_map))
    print(req.text)
