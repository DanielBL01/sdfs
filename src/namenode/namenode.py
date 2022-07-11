"""

gRPC Server Code for NameNode    

For now, the user does not specify a port for the server and it set at 9000

Note that the Client service is user-facing and implements REST
while namenode is a gRPC server AND Client for gRPC DataNode server

Note to self: A process is an instance of the python interpreter
that executes python instructions (Python byte-code)

A process has at least one thread called MainThread where a thread
is like a line of execution within a process.

Here a server is the process and we can have multiple threads which
may pick up requests from the client from a queue.

To do this, we're going to implement multiprocessing based servers.

"""

import argparse
import atexit
import os
from concurrent import futures
import multiprocessing

import grpc
from namenode_pb2 import File, Response 
import namenode_pb2_grpc
import datanode_pb2
import datanode_pb2_grpc

_PROCESS_COUNT = 3

_datanode_channel_singleton = None
_datanode_stub_singleton = None
_datanode_server_address = None

parent_dir = "/Users/daniellee/.sdfs/" 
host = os.getenv("HOST", "localhost")
namenode_dir = parent_dir + "namenode/"

def _handle_dirs():
    # Ensure required dirs exist or create if else
    if not os.path.isdir(namenode_dir):
        os.makedirs(namenode_dir)

def _parse_datanode_server_argument():
    # SDFS expects a -- [DATANODE_SERVER_ADDRESS] argument when running the NameNode
    global _datanode_server_address
    parser = argparse.ArgumentParser(
        description="Connect to a set of DataNode servers to replicate a distributed filesystem"
    )
    # This is a position argument so the datanode server must be the first argument after the script name
    parser.add_argument(
        "datanode_server_address",
        help="The address of the datanode server (e.g. '[::]:12345')",
        type=str
    )
    args = parser.parse_args()
    _datanode_server_address = args.datanode_server_address
    print("DataNode server on {}. Ensure this is the correct address for SDFS to work"
        .format(_datanode_server_address))

def _shutdown_datanode():
    print("Shutting down datanode process")
    if _datanode_channel_singleton is not None:
        _datanode_channel_singleton.close()

def _initialize_datanode():
    # Note to self: In Python, to modify global vars need global keyword
    global _datanode_channel_singleton
    global _datanode_stub_singleton
    _datanode_channel_singleton = grpc.insecure_channel(_datanode_server_address)
    _datanode_stub_singleton = datanode_pb2_grpc.DataNodeStub(
        _datanode_channel_singleton
    )
    atexit.register(_shutdown_datanode)

def _run_namenode_write_service(file_data):
    # Run the NameNodeWrite defined in the datanode protocol buffer for replication
    return _datanode_stub_singleton.NameNodeWrite(
        datanode_pb2.SystemFileData(
            filename = file_data[0],
            content = file_data[1] 
        )
    )

def _replicate(filename, content):
    # Pool object parallelizes the execution of a function across multiple input values, 
    # distributing the input data across processes called (data parallelism) (Use this for chunking?)
    datanode_pool = multiprocessing.Pool(
        processes=_PROCESS_COUNT,
        initializer=_initialize_datanode,
        initargs=_datanode_server_address
    )
    rep_input = []
    for _ in range(3):
        single_input = [filename, content]
        rep_input.append(single_input)
    return datanode_pool.map(_run_namenode_write_service, rep_input)
    
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
        _replicate(filename, source_binary_file_content)
        return Response(message = "Successfully wrote to filesystem")

    def ClientReadFromNameNode(self, request, context):
        # Read rpc gets a SystemFile message and returns File message
        filename = request.filename
        system_file_path = namenode_dir + filename 
        with open(system_file_path, "rb") as system_binary_file:
            system_binary_file_content = system_binary_file.read()
        return File(content = system_binary_file_content)

def serve():
    # There should only be one instance of the NameNode so no need for multiprocessing
    _parse_datanode_server_argument() 
    _handle_dirs()
    namenode_bind_address = "[::]:9000"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    namenode_pb2_grpc.add_NameNodeServicer_to_server(_NameNodeServicer(), server)
    # Currently just run the NameNode server on 9000 as default
    server.add_insecure_port(namenode_bind_address)
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()