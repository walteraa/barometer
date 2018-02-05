import schedule
import time
import threading
from utils.config import *
from utils.network import *


def dispatch_jobs(conf):
    while True:
        schedule.run_pending()
        time.sleep(1)
def create_job(conf):
    def create_ping_threads():
        for target in conf.get_targets():
            threading.Thread(target=send_ping, 
                             args=(conf.get_aggregate(),
                                   conf.get_cluster_id(),
                                   target,
                                   http_callback,)).start()
    schedule.every().minute.do(create_ping_threads)




if __name__ == '__main__':
    conf = Config()
    conf.load_resources()
    create_job(conf)
    dispatch_jobs(conf)

