import os
import grpc
from concurrent import futures
import replication_pb2
import replication_pb2_grpc

class ContentReplicatorService(replication_pb2_grpc.ContentReplicatorServicer):
    def __init__(self):
        # Initialize the base class (superclass) constructor
        super().__init__()  # This is usually not necessary for gRPC service classes, but it's good practice.

        # Set up a base directory for replica contents
        self.base_directory = os.path.abspath("replica_2_contents")
        # Ensure the directory exists
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)

    def AddContent(self, request, context):
        # Create the full path from the base directory and the relative path
        safe_path = os.path.join(self.base_directory, request.path)
        
        # Ensure any subdirectories exist before writing the file
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)

        try:
            # Write the content to the file at the correct location
            with open(safe_path, 'wb') as f:
                f.write(request.content)
            return replication_pb2.ReplicationResponse(success=True, message="Content added successfully")
        except Exception as e:
            return replication_pb2.ReplicationResponse(success=False, message=str(e))

    def RemoveContent(self, request, context):
        # Create the full path from the base directory and the relative path
        safe_path = os.path.join(self.base_directory, request.path)

        if os.path.exists(safe_path):
            try:
                os.remove(safe_path)
                return replication_pb2.ReplicationResponse(success=True, message="Content removed successfully")
            except Exception as e:
                return replication_pb2.ReplicationResponse(success=False, message=str(e))
        else:
            return replication_pb2.ReplicationResponse(success=False, message="File not found")
            

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=3), options=[('grpc.max_receive_message_length', -1)])  # No limit
    replication_pb2_grpc.add_ContentReplicatorServicer_to_server(ContentReplicatorService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
