import aerospike
from aerospike import exception as ex
from contextlib import contextmanager

class AerospikeDBConnection:
    def __init__(self, hostname=None, namespace='test', set_name='demo'):
        if hostname is None:
            print("!!Please provide a hostname")
        else:
            self.hostname = hostname
            self.namespace = namespace
            self.set_name = set_name
            self.client = None
            
    def connect(self):
        try:
            config = {
                'hosts' : [(self.hostname, 3000)]
            }
            self.client = aerospike.client(config).connect()
            print("connected to aerospike")
        except ex.AerospikeError as e:
            print(f"Error connecting to Aerospikev: {e}")
            raise
    def disconnect(self):
        if self.client:
            self.client.close()
            print("Aerospike connection closed now.")
    
    @contextmanager
    def get_connection(self):
        try:
            if not self.client:
                self.connect()
            yield self.client
        finally:
            if self.client:
                self.disconnect()
    
    def create_record(self, key, record_data):
        try:
            key_tuple = (self.namespace, self.set_name, key)
            self.client.put(key_tuple, record_data)
            print(f"Record with key {key} created successfully.")
        except ex.AerospikeError as e:
            print(f"Error creating record: {e}")
    
    def fetch_record(self,key):
        try: 
            key_tuple = (self.namespace, self.set_name, key) 
            (key, metadata, record) = self.client.get(key_tuple)
            return record
        except ex.RecordNotFound :
            print(f"Record with key {key} not found.")
        except ex.AerospikeError as e:
            print(f"Error reading record: {e}")
    def update_record(self, key, record_data):
        try:
            key_tuple = (self.namespace, self.set_name, key)
            self.client.put(key_tuple, record_data)
            print(f"Record with key {key} updated successfully.")
        except ex.AerospikeError as e:
            print(f"Error updating record: {e}")
    def delete_record(self, key):
        try:
            key_tuple = (self.namespace, self.set_name, key)
            self.client.remove(key_tuple)
            print(f"Record with key {key} deleted successfully.")        
        except ex.RecordNotFound:
            print(f"Record with key {key} not found.")
        except ex.AerospikeError as e:
            print(f"Error deleting record: {e}") 