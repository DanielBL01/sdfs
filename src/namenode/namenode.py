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
import socket
import sys
import logging
from datetime import timedelta
import time

import grpc
from namenode_pb2 import File, Response 
import namenode_pb2_grpc
import datanode_pb2
import datanode_pb2_grpc

_ONE_DAY = timedelta(days=1)
_PROCESS_COUNT = 3
_THREAD_CONCURRENCY = _PROCESS_COUNT

# Configure logger to be at the lowest level i.e. INFO to log everything
logging.basicConfig(
    filename="namenode.log", 
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")
_LOGGER = logging.getLogger(__name__)

_datanode_channel_singleton = None
_datanode_stub_singleton = None

parent_dir = "/Users/daniellee/.sdfs/" 
host = os.getenv("HOST", "localhost")
namenode_dir = parent_dir + "namenode/"

class _NameNodeServicer(namenode_pb2_grpc.NameNodeServicer):

    def ClientWrite(self, request, context):
        _datanode_server_address = _parse_datanode_server_argument()
        # Write rpc gets SourceFile message and returns Response message
        filename = request.filename
        source_path = request.sourcepath
        with open(source_path, "rb") as source_binary_file:
            source_binary_file_content = source_binary_file.read()
            system_file_path = namenode_dir + filename
            with open(system_file_path, "wb") as system_binary_file:
                system_binary_file.write(source_binary_file_content) 
        _replicate(filename, _datanode_server_address)
        return Response(message = "Successfully wrote to filesystem")

    def ClientReadFromNameNode(self, request, context):
        # Read rpc gets a SystemFile message and returns File message
        filename = request.filename
        system_file_path = namenode_dir + filename 
        with open(system_file_path, "rb") as system_binary_file:
            system_binary_file_content = system_binary_file.read()
        return File(content = system_binary_file_content)

def _handle_dirs():
    # Ensure required dirs exist or create if else
    if not os.path.isdir(namenode_dir):
        os.makedirs(namenode_dir)

def _parse_datanode_server_argument():
    # SDFS expects a -- [DATANODE_SERVER_ADDRESS] argument when running the NameNode
    parser = argparse.ArgumentParser(
        description="Connect to a set of DataNode servers to replicate a distributed filesystem")
    # This is a position argument so the datanode server must be the first argument after the script name
    parser.add_argument(
        "datanode_server_address",
        help="The address of the datanode server (e.g. 'localhost:12345')",
        type=str)
    args = parser.parse_args()
    _datanode_server_address = args.datanode_server_address
    _LOGGER.info("DataNode server on {}. Ensure this is the correct address for SDFS to work"
        .format(_datanode_server_address))
    return _datanode_server_address

def _shutdown_datanode():
    _LOGGER.info("Shutting down datanode process")
    if _datanode_channel_singleton is not None:
        _datanode_channel_singleton.close()

def _initialize_datanode(_datanode_server_address):
    # Note to self: In Python, to modify global vars need global keyword
    global _datanode_channel_singleton
    global _datanode_stub_singleton
    _datanode_channel_singleton = grpc.insecure_channel(_datanode_server_address)
    _datanode_stub_singleton = datanode_pb2_grpc.DataNodeStub(
        _datanode_channel_singleton)
    atexit.register(_shutdown_datanode)

def _run_namenode_write_service(filename):
    _LOGGER.info("Replicating {}".format(filename))
    # Run the NameNodeWrite defined in the datanode protocol buffer for replication
    response = _datanode_stub_singleton.NameNodeWrite(
        datanode_pb2.SystemFileData(
            filename = filename,
            content = str.encode("This is garbage text")))
    _LOGGER.info(response.message)
    return response

def _replicate(filename, _datanode_server_address):
    # Pool object parallelizes the execution of a function across multiple input values, 
    # distributing the input data across processes called (data parallelism) 
    # (Use this for chunking?)
    _LOGGER.info("Starting replication process")
    datanode_pool = multiprocessing.Pool(
        processes=_PROCESS_COUNT,
        initializer=_initialize_datanode,
        initargs=(_datanode_server_address,))
    _LOGGER.info("Does it reach here after init Pool?")
    filenames = []
    for _ in range(3):
        filenames.append(filename)
    responses = datanode_pool.map(_run_namenode_write_service, filenames)
    _LOGGER.info(responses)

def _check_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        res = sock.connect_ex(("localhost", port))
        # connect_ex will return 0 if successful i.e the port is in use
        if res == 0:
            sys.exit()

def _wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        _LOGGER.info("NameNode server ended with KeyboardInterrupt")
        server.stop(None)

def _run_server(bind_address):
    os.environ["SUB_PROCESS_NUM"] = "namenode"
    _LOGGER.info("PID: {}, SUB_PROCESS_NUM: {}".format(os.getpid(), os.environ["SUB_PROCESS_NUM"]))
    options = (("grpc.so_reuseport", 1),)
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=_THREAD_CONCURRENCY,),
        options=options)
    namenode_pb2_grpc.add_NameNodeServicer_to_server(_NameNodeServicer(), server)
    server.add_insecure_port(bind_address)
    server.start()
    _wait_forever(server)
    
def serve():
    # I think the solution is that this namenode shouldn't be a process itself.
    # There should only be one instance of the NameNode so no need for multiprocessing
    _parse_datanode_server_argument() 
    _handle_dirs()
    _check_port_in_use(9000)
    # NameNode is meant to run on 9000 so check if its available
    namenode_bind_address = "[::]:9000"
    namenode_subprocess = multiprocessing.Process(
        target=_run_server,
        args=(namenode_bind_address,)
    )
    namenode_subprocess.start()
    namenode_subprocess.join()
    
if __name__ == "__main__":
    serve()