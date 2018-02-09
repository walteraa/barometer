import json
import time
import requests
from ping3 import ping

def send_ping(aggregate, target, callback):
    ping_response = ping(target.host)
    ping_response = 4 if ping_response == None else ping_response
    
    callback(aggregate, ping_response, target, {'sensor':'PING','metric':'ping-time'})


def http_callback(aggregate, monitoring_data, target, agent_type):
    
    #Preparing the data to be sent
    json_map = {}
    json_map["machine_id"] = target.machine_id
    json_map["time_stamp"] = int(time.time())
    json_map["sensor_name"] = agent_type['sensor']
    json_map["metric_name"] = agent_type['metric']
    json_map["value_type"] = type(monitoring_data).__name__
    json_map["metric_value"] = monitoring_data
    json_map["cluster_id"] = aggregate['cluster_id']

    print("sending HTTP to: %s:%d with data: %s"%(aggregate['host'],aggregate['port'],json.dumps(json_map)))
    
    #TODO: Add it for a constant
    URI = "/metric"
    
    headers = {
        'Content-Type': 'application/json',
    }

    URL = "http://%s:%d%s"%(aggregate['host'], aggregate['port'], URI)
    req = requests.post(url = URL, headers=headers, data = json.dumps(json_map))
    print(req.text)
