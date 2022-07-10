"""

gRPC Server Code for DataNode

"""

from concurrent import futures
import os

import grpc
from datanode_pb2 import File, Response
import datanode_pb2_grpc

parent_dir = "/Users/daniellee/.sdfs/"
datanode_dir = parent_dir + "datanode/"

def _handle_dirs():
    if not os.path.isdir(datanode_dir):
        os.makedirs(datanode_dir)
    else:
        print("{} exists".format(datanode_dir))

class DataNodeServicer(datanode_pb2_grpc.DataNodeServicer):

    def NameNodeWrite(self, request, context):
        return Response()

    def ClientReadFromDataNode(self, request, context):
        """ Read rpc is given a SystemFile message and returns File message """ 
        filename = request.filename
        system_file_path = datanode_dir + filename
        with open(system_file_path, "rb") as system_binary_file:
            system_binary_file_content = system_binary_file.read()
            return File(content = system_binary_file_content) 

def serve():
    _handle_dirs()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datanode_pb2_grpc.add_DataNodeServicer_to_server(DataNodeServicer(), server)
    server.add_insecure_port("[::]:8080")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()