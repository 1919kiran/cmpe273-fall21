from psycopg2.extras import LogicalReplicationConnection
from psycopg2.extras import StopReplication
from protos import replicator_pb2_grpc
from protos import replicator_pb2
import grpc
import configparser
import psycopg2

# PostgreSQL DB configs
config = configparser.ConfigParser()
config.read('config.ini')
postgres_config = config['PostgreSQL']
connection = psycopg2.connect(
    dbname=postgres_config['dbname'],
    user=postgres_config['user'],
    password=postgres_config['password'],
    host=postgres_config['host'],
    port=postgres_config['port'],
    connection_factory=LogicalReplicationConnection
)
cursor = connection.cursor()
try:
    cursor.create_replication_slot('pytest', output_plugin='wal2json')
except psycopg2.errors.DuplicateObject:
    pass


class ReplicatorClient:
    def run(self, msg):
        channel = grpc.insecure_channel('localhost:50051')
        stub = replicator_pb2_grpc.ReplicatorStub(channel)
        replication = stub.replicate(replicator_pb2.ReplicationRequest(request=msg))
        print("Response from server : " + str(replication.reply))


client = ReplicatorClient()


class StreamConsumer(object):
    def __call__(self, msg):
        # print(msg.payload)
        msg.cursor.send_feedback(flush_lsn=msg.data_start)
        client.run(msg.payload)
        if 'stop_repl' in msg.payload:
            raise StopReplication()


if __name__ == '__main__':
    print('Starting Replication Client...')
    client = ReplicatorClient()
    stream_consumer = StreamConsumer()
    cursor.start_replication(slot_name='pytest', decode=True)
    cursor.consume_stream(stream_consumer)
