import os
from bson.json_util import dumps
import pymongo
from  pymongo import MongoClient
from flask import Flask, request
from flask_api import status

app = Flask(__name__)

#TODO: define default values when variables are empty
MONGO_HOST = os.environ['MONGODB_HOST']
MONGO_PORT = int(os.environ['MONGODB_PORT'])
mongo = MongoClient(MONGO_HOST, MONGO_PORT)


@app.route('/metric', methods=['POST'])
def save_metric():

    #TODO: validate data before save
    content = request.get_json(silent=True)
    mongo.db.metrics_barograph.insert_one(content)
    return "OK"

@app.route('/metric')
def get_metric():
    list_clusters = list(mongo.db.metrics_barograph.distinct("cluster_id"))
    result = []
    for cluster in list_clusters:
        result.append(list(mongo.db.metrics_barograph.find({"cluster_id": cluster}).sort("timestamp",pymongo.DESCENDING).limit(1))[0])

    return dumps(result)


@app.route('/node_info/<id>', methods=['POST'])
def save_node_info(id):

    cluster = mongo.db.clusters.find_one({"cluster-id":id})
    if cluster == None:
        return {"Error": "Cnuster not found" }, status.HTTP_404_NOT_FOUND

    #TODO: validate data before save
    content = request.get_json(silent=True)
    result = mongo.db.clusters.update_one({'cluster-id': id}, { '$set': {'node_info': content} }, upsert= False )
    
    print(content)
    if result.matched_count == 1:
        return "",status.HTTP_200_OK
    else:
        return "Error",status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route('/node_info', methods=['GET'])
def list_clusters():
    clusters_list = list(mongo.db.clusters.find())
    return dumps(clusters_list)

@app.route('/node_info/<id>', methods=['GET'])
def get_cluster(id):
    cluster = mongo.db.clusters.find_one({"cluster-id":id})
    return dumps(cluster)

@app.route('/cluster_status/<id>', methods=[ 'POST'])
def update_cluster_status(id):

    cluster = mongo.db.clusters.find_one({"cluster-id":id})
    if cluster == None:
        return {"Error": "Cnuster not found" }, status.HTTP_404_NOT_FOUND


    result = mongo.db.clusters.update_one({'cluster-id': cluster['cluster-id']}, { '$set': {'cluster_status': True} }, upsert= False )

    
    if result.matched_count == 1:
        return "",status.HTTP_200_OK
    else:
        return "Error"

@app.route('/agg_status/<id>', methods=[ 'POST'])
def update_agg_status(id):

    cluster = mongo.db.clusters.find_one({"cluster-id":id})
    if cluster == None:
        return {"Error": "Cnuster not found" }, status.HTTP_404_NOT_FOUND


    result = mongo.db.clusters.update_one({'cluster-id': cluster['cluster-id']}, { '$set': {'agg_status': True} }, upsert= False )

    
    if result.matched_count == 1:
        return "",status.HTTP_200_OK
    else:
        return "Error"


@app.route('/agent_status/<id>', methods=[ 'POST'])
def update_agent_status(id):

    cluster = mongo.db.clusters.find_one({"cluster-id":id})
    if cluster == None:
        return {"Error": "Cnuster not found" }, status.HTTP_404_NOT_FOUND


    result = mongo.db.clusters.update_one({'cluster-id': cluster['cluster-id']}, { '$set': {'agent_status': True} }, upsert= False )

    
    if result.matched_count == 1:
        return "",status.HTTP_200_OK
    else:
        return "Error"

@app.route('/')
def liveness():
    return "OK"


#Starting the server
if __name__ == "__main__":
    app.run(debug=True,use_reloader=False, host='0.0.0.0', port=8080)

