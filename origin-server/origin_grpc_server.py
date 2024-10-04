import grpc
import replication_pb2
import replication_pb2_grpc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor
import time

class Handler(FileSystemEventHandler):
    def __init__(self, grpc_clients):
        self.grpc_clients = grpc_clients
        self.executor = ThreadPoolExecutor(max_workers=len(grpc_clients))

    def on_created(self, event):
        if not event.is_directory:
            with open(event.src_path, 'rb') as f:
                content = f.read()
            for client in self.grpc_clients:
                self.executor.submit(self.upload_content, client, event.src_path, content)

    def on_deleted(self, event):
        if not event.is_directory:
            for client in self.grpc_clients:
                self.executor.submit(self.delete_content, client, event.src_path)

    def upload_content(self, client, path, content):
        client.AddContent(replication_pb2.ReplicationRequest(path=path, content=content))

    def delete_content(self, client, path):
        client.RemoveContent(replication_pb2.ReplicationRequest(path=path))

def setup_grpc_clients(replica_addresses):
    clients = []
    for address in replica_addresses:
        channel = grpc.insecure_channel(address)
        clients.append(replication_pb2_grpc.ContentReplicatorStub(channel))
    return clients

def monitor_directory(path, grpc_clients):
    event_handler = Handler(grpc_clients)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    replica_addresses = ["localhost:50051", "localhost:50052", "localhost:50053"]  # Example addresses
    grpc_clients = setup_grpc_clients(replica_addresses)
    monitor_directory('/path/to/watch', grpc_clients)
