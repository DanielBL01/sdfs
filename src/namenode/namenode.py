"""

gRPC Server Code for NameNode    

For now, the user does not specify a port for the server and it set at 9000

Note that the Client service is user-facing and implements REST
while namenode is a gRPC server AND Client for gRPC DataNode server

Note to self: A process is an instance of the python interpreter
that executes python instructions (Python byte-code) i.e. a running
instance of your python program

A process has at least one thread called MainThread where a thread
is like a line of execution within a process.

Here a server is the process and we can have multiple threads which
may pick up requests from the client from a queue.

To do this, we're going to implement multiprocessing based servers.

"""

import os
from concurrent import futures
import socket
import sys
import logging
from datetime import timedelta
import time
import argparse
from pathlib import Path

import grpc
from namenode_pb2 import File, Response 
import namenode_pb2_grpc

_ONE_DAY = timedelta(days=1)

# Configure logger to be at the lowest level i.e. INFO to log everything
logging.basicConfig(
    filename="namenode.log", 
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")
_LOGGER = logging.getLogger(__name__)

host = os.getenv("HOST", "localhost")
namenode_dir = None 

class _NameNodeServicer(namenode_pb2_grpc.NameNodeServicer):

    def ClientWrite(self, request, context):
        # Write rpc gets SourceFile message and returns Response message
        filename = request.filename
        source_path = request.sourcepath
        with open(source_path, "rb") as source_binary_file:
            source_binary_file_content = source_binary_file.read()
            system_file_path = namenode_dir + filename
            with open(system_file_path, "wb") as system_binary_file:
                system_binary_file.write(source_binary_file_content) 
        return Response(message = "Successfully wrote to filesystem")

    def ClientReadFromNameNode(self, request, context):
        # Read rpc gets a SystemFile message and returns File message
        filename = request.filename
        system_file_path = namenode_dir + filename 
        with open(system_file_path, "rb") as system_binary_file:
            system_binary_file_content = system_binary_file.read()
        return File(content = system_binary_file_content)

def _setup_namenode_dir():
    if namenode_dir is not None:
        if not os.path.isdir(namenode_dir):
            os.makedirs(namenode_dir)
        rep_log_path = namenode_dir + "replication.log"
        if not os.path.exists(rep_log_path):
            Path(rep_log_path).touch()

def _check_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        res = sock.connect_ex(("localhost", port))
        # connect_ex will return 0 if successful i.e the port is in use
        if res == 0:
            print("Please ensure that port 9000 is open for NameNode")
            sys.exit()

def _wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        print("Stopping the NameNode server")
        server.stop(None)

def serve():
    global namenode_dir
    msg = "Specify the parent directory for sdfs - simple distributed file system"
    parser = argparse.ArgumentParser(description=msg)
    # This is a position argument so the datanode server must be the first argument after the script name
    parser.add_argument("parent_dir", help="The parent directory for your files (e.g. /Users/whoami/.sdfs)")
    args = parser.parse_args()
    parent_dir = args.parent_dir
    namenode_dir = parent_dir + "/namenode/"

    _setup_namenode_dir()

    _check_port_in_use(9000)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    namenode_pb2_grpc.add_NameNodeServicer_to_server(
        _NameNodeServicer(), server)
    server.add_insecure_port('[::]:9000')
    server.start()
    _wait_forever(server)
if __name__ == "__main__":
    serve()