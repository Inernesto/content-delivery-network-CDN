import grpc
import os
import replication_pb2
import replication_pb2_grpc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor
import time

class DirectoryMonitor:
    def __init__(self, grpc_clients, directory_path):
        self.grpc_clients = grpc_clients
        self.directory_path = directory_path
        self.handler = Handler(grpc_clients)

    def push_existing_files(self):
        for file_name in os.listdir(self.directory_path):
            file_path = os.path.join(self.directory_path, file_name)
            if os.path.isfile(file_path):
                self.handler.process_created_file(file_path)

    def monitor_directory(self):
        observer = Observer()
        observer.schedule(self.handler, self.directory_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, grpc_clients):
        self.grpc_clients = grpc_clients
        self.executor = ThreadPoolExecutor(max_workers=len(grpc_clients))

    def on_created(self, event):
        if not event.is_directory:
            self.process_created_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            for client in self.grpc_clients:
                self.executor.submit(self.delete_content, client, event.src_path)

    def process_created_file(self, file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        for client in self.grpc_clients:
            self.executor.submit(self.upload_content, client, file_path, content)

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

if __name__ == "__main__":
    replica_addresses = ["localhost:50051", "localhost:50052", "localhost:50053"]
    grpc_clients = setup_grpc_clients(replica_addresses)
    ## directory_path = '/path/to/watch'
    directory_path = os.path.abspath("origin_contents")
    monitor = DirectoryMonitor(grpc_clients, directory_path)
    monitor.push_existing_files()
    monitor.monitor_directory()
