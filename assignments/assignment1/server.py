from concurrent import futures
import time
import grpc
import json
import pymongo
import configparser

from protos import replicator_pb2_grpc
from protos import replicator_pb2


_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# MongoDB configs
config = configparser.ConfigParser()
config.read('config.ini')
mongodb_config = config['MongoDB']
client = pymongo.MongoClient(
    "mongodb+srv://" + mongodb_config['username'] + ":"
     + mongodb_config['password']+ "@" + mongodb_config['cluster'] + "/" + mongodb_config['database'])
db = client["college"]
collection = db["students"]

class ReplicatorServer(replicator_pb2_grpc.ReplicatorServicer):
    def replicate(self, request, context):
        data = json.loads(request.request)
        response = crud(data)
        # print(request.request)
        return replicator_pb2.ReplicationReply(reply=response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replicator_pb2_grpc.add_ReplicatorServicer_to_server(ReplicatorServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


def crud(data):
    # print("Request from Client: " +str(data))
    try:
        for change in data["change"]:
            kind = change["kind"]
            table = change["table"]
            if kind == 'insert':
                columnnames = change["columnnames"]
                columnvalues = change["columnvalues"]
                print('*** Inserting document... *** ')
                data = dict(zip(columnnames, columnvalues))
                # Changing id
                data['_id'] = data.pop('id')
                x = collection.insert_one(data)
                print(data)

            elif kind == 'update':
                columnnames = change["columnnames"]
                columnvalues = change["columnvalues"]
                print('Updating record...')
                oldkey = change["oldkeys"]["keynames"][0]
                oldkeyvalue = change["oldkeys"]["keyvalues"][0]
                data = dict(zip(columnnames, columnvalues))
                # Changing id
                data['_id'] = data.pop('id')
                # data["postgres_id"] = oldkeyvalue
                filter = {"_id": oldkeyvalue}
                x = collection.update_one(filter, {"$set": data})
                print(data)

            elif kind == 'delete':
                print('Deleting record...')
                oldkey = change["oldkeys"]["keynames"][0]
                oldkeyvalue = change["oldkeys"]["keyvalues"][0]
                filter = {"_id": oldkeyvalue}
                x = collection.delete_one(filter)
                print(change)
            else:
                print('Invalid kind')
    except:
        return 'Exception occured at Replication Server'


    return 'Operation is executed'

if __name__ == '__main__':
    try:
        # PostgreSQL DB configs
        config = configparser.ConfigParser()
        config.read('config.ini')
        mongodb_config = config['MongoDB']

        client = pymongo.MongoClient(
            "mongodb+srv://" + mongodb_config['username'] + ":"
            + mongodb_config['password'] + "@" + mongodb_config['cluster'] + "/" + mongodb_config['database'])

        client = pymongo.MongoClient()
        db = client.test
        print('Starting Replication Server...')
        serve()

    except:
        print('Replication Server has stopped')
