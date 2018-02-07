import json
import time
import requests
from ping3 import ping

def send_ping(aggregate,cluster_id, target, callback):
    ping_response = ping(target.host)
    ping_response = 4 if ping_response == None else ping_response
    
    callback(aggregate, cluster_id, ping_response, target, {'sensor':'PING','metric':'ping-time'})


def http_callback(aggregate,cluster_id, monitoring_data, target, agent_type):
    
    #Preparing the data to be sent
    json_map = {}
    json_map["machine_id"] = target.machine_id
    json_map["time_stamp"] = int(time.time())
    json_map["sensor_name"] = agent_type['sensor']
    json_map["metric_name"] = agent_type['metric']
    json_map["value_type"] = type(monitoring_data).__name__
    json_map["metric_value"] = monitoring_data

    print("sending HTTP to: %s:%d with data: %s"%(aggregate['host'],aggregate['port'],json.dumps(json_map)))
    
    #TODO: Add it for a constant
    URI = "/metric"
    
    URL = "http://%s:%d%s"%(aggregate['host'], aggregate['port'], URI)
    req = requests.post(url = URL, data = json.dumps(json_map))
    print("\nResponse: %s\n\n"%req.text)
