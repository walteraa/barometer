import os
from bson.json_util import dumps
import pymongo
from  pymongo import MongoClient
from flask import Flask, request

app = Flask(__name__)

#TODO: define default values when variables are empty
MONGO_HOST = os.environ['MONGODB_HOST']
MONGO_PORT = int(os.environ['MONGODB_PORT'])
mongo = MongoClient(MONGO_HOST, MONGO_PORT)


@app.route('/metric', methods=['POST'])
def save_metric():

    #TODO: validate data before save
    content = request.get_json(silent=True)
    print(content)
    mongo.db.metrics_barograph.insert_one(content)
    return "OK"

@app.route('/metric')
def get_metric():
    list_clusters = list(mongo.db.metrics_barograph.distinct("cluster_id"))
    result = []
    for cluster in list_clusters:
        result.append(list(mongo.db.metrics_barograph.find({"cluster_id": cluster}).sort("timestamp",pymongo.DESCENDING).limit(1))[0])

    return dumps(result)
@app.route('/')
def liveness():
    return "OK"


#Starting the server
if __name__ == "__main__":
    app.run(debug=True,use_reloader=False, host='0.0.0.0', port=8080)

