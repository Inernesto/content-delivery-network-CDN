import os
import grpc
from concurrent import futures
import replication_pb2
import replication_pb2_grpc

class ContentReplicatorService(replication_pb2_grpc.ContentReplicatorServicer):
    def AddContent(self, request, context):
        # Example: Save the content to a file
        directory_path = os.path.abspath("replica_2_contents")
        with open(f'{directory_path}/{request.path}', 'wb') as f:
            f.write(request.content)
        return replication_pb2.ReplicationResponse(success=True, message="Content added successfully")

    def RemoveContent(self, request, context):
        # Example: Remove the content file
        directory_path = os.path.abspath("replica_2_contents")
        os.remove(f'{directory_path}/{request.path}')
        return replication_pb2.ReplicationResponse(success=True, message="Content removed successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replication_pb2_grpc.add_ContentReplicatorServicer_to_server(ContentReplicatorService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
