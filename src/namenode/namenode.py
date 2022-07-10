"""

gRPC Server Code for NameNode    

For now, the user does not specify a port for the server and it set at 9000

"""

from concurrent import futures
import os

import grpc
from namenode_pb2 import File, Response 
import namenode_pb2_grpc

parent_dir = "/Users/daniellee/.sdfs/" 
namenode_dir = parent_dir + "namenode/"
datanode_dir = parent_dir + "datanode/"

def _handle_dirs():
    if not os.path.isdir(namenode_dir):
        os.makedirs(namenode_dir)
    else:
        print("{} exists".format(namenode_dir))

def _replicate(filename, content):
    """ Replicate file written to NameNode to available DataNodes """
    system_file_path = datanode_dir + filename
    with open(system_file_path, "wb") as system_binary_file:
        system_binary_file.write(content)
        system_binary_file.close()
    
class NameNodeServicer(namenode_pb2_grpc.NameNodeServicer):

    def ClientWrite(self, request, context):
        """ Write rpc is given a SourceFile message and returns Response message """
        filename = request.filename
        source_path = request.sourcepath
        with open(source_path, "rb") as source_binary_file:
            source_binary_file_content = source_binary_file.read()
            system_file_path = namenode_dir + filename
            with open(system_file_path, "wb") as system_binary_file:
                system_binary_file.write(source_binary_file_content) 
                system_binary_file.close()
            source_binary_file.close()
        _replicate(filename, source_binary_file_content)
        return Response(message = "Successfully wrote to filesystem")

    def ClientReadFromNameNode(self, request, context):
        """ Read rpc is given a SystemFile message and returns File message """
        filename = request.filename
        system_file_path = namenode_dir + filename 
        with open(system_file_path, "rb") as system_binary_file:
            system_binary_file_content = system_binary_file.read()
            return File(content = system_binary_file_content)

def serve():
    _handle_dirs()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    namenode_pb2_grpc.add_NameNodeServicer_to_server(NameNodeServicer(), server)
    server.add_insecure_port("[::]:9000")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()