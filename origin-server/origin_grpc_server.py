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
        self.handler = Handler(grpc_clients, directory_path)

    def push_existing_files(self):
        # Handle all files in subdirectories from the start
        for root, dirs, files in os.walk(self.directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    relative_path = os.path.relpath(file_path, self.directory_path)
                    self.handler.process_created_file(relative_path)

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
    def __init__(self, grpc_clients, directory_path):
        self.grpc_clients = grpc_clients
        self.base_directory = directory_path
        self.executor = ThreadPoolExecutor(max_workers=len(grpc_clients))

    def on_created(self, event):
        if not event.is_directory:
            relative_path = os.path.relpath(event.src_path, self.base_directory)
            self.process_created_file(relative_path)

    def on_modified(self, event):
        if not event.is_directory:
            relative_path = os.path.relpath(event.src_path, self.base_directory)
            self.process_created_file(relative_path)

    def on_deleted(self, event):
        if not event.is_directory:
            relative_path = os.path.relpath(event.src_path, self.base_directory)
            for client in self.grpc_clients:
                self.executor.submit(self.delete_content, client, relative_path)

    def process_created_file(self, relative_path):
        full_path = os.path.join(self.base_directory, relative_path)
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
            for client in self.grpc_clients:
                self.executor.submit(self.upload_content, client, relative_path, content)
        except Exception as e:
            print(f"Failed to process file {full_path}: {e}")

    def upload_content(self, client, relative_path, content):
        try:
            response = client.AddContent(replication_pb2.ReplicationRequest(path=relative_path, content=content))
            print(f"Received response from replica: {response.message}")
        except grpc.RpcError as e:
            print(f"gRPC error encountered: {e}")
        except Exception as e:
            print(f"Unexpected error sending content to replica: {e}")

    def delete_content(self, client, relative_path):
        try:
            response = client.RemoveContent(replication_pb2.ReplicationRequest(path=relative_path))
            print(f"Received delete response from replica: {response.message}")
        except grpc.RpcError as e:
            print(f"gRPC error encountered: {e}")
        except Exception as e:
            print(f"Unexpected error sending delete request to replica: {e}")

def setup_grpc_clients(replica_addresses):
    clients = []
    for address in replica_addresses:
        channel = grpc.insecure_channel(address, options=[('grpc.max_send_message_length', -1)])  # No limit
        clients.append(replication_pb2_grpc.ContentReplicatorStub(channel))
    return clients

if __name__ == "__main__":
    replica_addresses = ["localhost:50051", "localhost:50052", "localhost:50053"]
    grpc_clients = setup_grpc_clients(replica_addresses)
    directory_path = os.path.abspath("origin_contents")
    monitor = DirectoryMonitor(grpc_clients, directory_path)
    monitor.push_existing_files()
    monitor.monitor_directory()
