import time

from sensoragent.utils.config import *
from sensoragent.utils.network import *

def create_job(conf):
    monitoring_data = send_target_request(conf.get_target())
    send_sensor_data(conf.get_target(), conf.get_aggregate(), monitoring_data)

if __name__ == '__main__':
    conf = Config()
    conf.load_resources()
    create_job(conf) 
