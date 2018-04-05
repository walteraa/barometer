import os
import json
import schedule
import threading
import time
import pprint
from  pymongo import MongoClient
from flask import Flask, request
from utils.config import *
from utils.network import *
app = Flask(__name__)


PORT = 8080

#TODO: define default values when variables are empty
MONGO_HOST = os.environ['MONGODB_HOST']
MONGO_PORT = int(os.environ['MONGODB_PORT'])
mongo = MongoClient(MONGO_HOST, MONGO_PORT)


semaphore = True

@app.route('/metric', methods=['POST'])
def save_metric():

    #TODO: validate data before save
    if semaphore:
        content = request.get_json(silent=True)
        content["processed"] = False
        mongo.db.metrics_ping.insert_one(content)

    return "OK"

@app.route('/')
def liveness():
    return "OK"



#TODO: improve this process
def create_job(conf):
    def calc_average():
        #Lock the database 
        semaphore = False

        #Do the JOB
        pipeline = [
                {"$match": {"processed": False }},
                { "$group": { "_id" : {"cluster_id":"$cluster_id",  metric_name": "$metric_name","value_type"}, "count" : { "$sum": 1 }, "value": {"$avg": "$metric_value" }}}
                ]
        data = list(mongo.db.metrics_ping.aggregate(pipeline))
        mongo.db.metrics_ping.update(
                {"processed": False },
                {"$set": {"processed": True}  },
                upsert = False,
                multi = True
                )
        #Unlock the database 
        semaphore = True

        print(data)
        #Send Data
        if len(data) > 0:
            data = data[0]
            http_callback(conf.get_aggregate()['cluster_id'], conf.get_barograph(), data) 
    schedule.every(1).minutes.do(calc_average)
    print("job created...")

def dispatch_job():
    while True:
        schedule.run_pending()
        time.sleep(1)


#Starting the server
if __name__ == "__main__":
    conf = Config()
    conf.load_resources()
    create_job(conf)
    threading.Thread(target=dispatch_job).start()
    app.run(debug=True,use_reloader=False, host='0.0.0.0', port=PORT)
