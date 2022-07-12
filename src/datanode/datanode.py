"""

gRPC Server Code for DataNode

The gRPC DataNode Servers will be multiprocessing based servers where
we instantiate one server per subprocess, balancing requests between
the servers using the SO_REUSEPORT socket option 

For whatever reason, we figured out that we can't do any os operations or
it returns as 'TypeError("cannot pickle '_thread.RLock' object")'. This
means we'll have to give the server the PID from the client?

"""

from datetime import timedelta
import multiprocessing
import time
import os
from concurrent import futures
import socket
import contextlib
import argparse
import logging

import grpc
from datanode_pb2 import File, Response
import datanode_pb2_grpc

_ONE_DAY = timedelta(days=1)

logging.basicConfig(
    filename="datanode.log", 
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")
_LOGGER = logging.getLogger(__name__)

datanode_dirs = {} 

class DataNodeServicer(datanode_pb2_grpc.DataNodeServicer):

    def NameNodeWrite(self, request, context):
        filename = request.filename
        content = request.content
        id = request.datanode_id
        system_file_path = datanode_dirs[id] + filename
        with open(system_file_path, "wb") as system_binary_file:
            system_binary_file.write(content)
        return Response(message = "Successfully replicated to {}".format(id))

    def ClientReadFromDataNode(self, request, context):
        # Read rpc gets a SystemFile message and returns File message
        active_process = os.getenv("SUB_PROCESS_NUM")
        filename = request.filename
        system_file_path = datanode_dirs[active_process] + filename
        with open(system_file_path, "rb") as system_binary_file:
            system_binary_file_content = system_binary_file.read()
        return File(content = system_binary_file_content) 

def _setup_datanode_dirs():
    if datanode_dirs is not None:
        for datanode_dir in datanode_dirs.values():
            if not os.path.isdir(datanode_dir):
                os.makedirs(datanode_dir)

def _wait_forever(server, pid):
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        print("[PID {}] DataNode server ended with KeyboardInterrupt\n".format(pid))
        server.stop(None)

def _run_server(bind_address, thread_concurrency, dir):
    # Set env var in a subprocess
    print("[PID {}]: Running server at {} hosting local file storage at {}\n".format(os.getpid(), bind_address, dir))
    # datanode_pid = "datanode_{}".format(os.getpid())
    # datanode_dirs[datanode_pid] = "{}datanode_{}/".format(parent_dir, datanode_pid) 
    # Start a server in a subprocess
    options = (("grpc.so_reuseport", 1),)
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=thread_concurrency,),
        options=options)
    datanode_pb2_grpc.add_DataNodeServicer_to_server(DataNodeServicer(), server)
    server.add_insecure_port(bind_address)
    server.start()
    _wait_forever(server, os.getpid())

@contextlib.contextmanager
def _reserve_port():
    # Find and reserve a port for all subprocesses to use
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set value of socket option SO_REUSEPORT to balance request between servers
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT")
    # binding socket to port 0 will assign it a free port
    sock.bind(("", 0))
    try:
        # This is the free port number that has been assigned
        yield sock.getsockname()[1]
    finally:
        sock.close()

def serve():
    # Let sdfs figure out how many cores the machine has to maximize operations i.e. the more datanodes, the better in scaling out
    process_count = multiprocessing.cpu_count()
    # The current plan here is to make a subprocess for each core and let each subprocess run a gRPC server on a separate port 

    global datanode_dirs
    msg = "Specify the parent directory for sdfs - simple distributed file system"
    parser = argparse.ArgumentParser(description=msg)
    # This is a position argument so the datanode server must be the first argument after the script name
    parser.add_argument("parent_dir", help="The parent directory for your files (e.g. /Users/whoami/.sdfs)")
    args = parser.parse_args()
    parent_dir = args.parent_dir
    # Set up datanode dirs based on the number of cores / processes
    for i in range(1, process_count + 1):
        datanode_dirs["datanode_{}".format(i)] = "{}/datanode_{}/".format(parent_dir, i)

    _setup_datanode_dirs()

    datanode_servers = {}
    try:
        for i in range(1, process_count + 1):
            # For each iteration, reserve a port for each gRPC server
            with _reserve_port() as port:
                server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
                datanode_pb2_grpc.add_DataNodeServicer_to_server(
                DataNodeServicer(), server)
                server.add_insecure_port('[::]:{}'.format(port))
                server.start()
                print("Running server at [::]:{} to host local file storage at datanode_{}\n".format(port, i))
                datanode_servers[port] = server
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        for port in datanode_servers:
            print("Stopping server on port {}\n".format(port))
            datanode_servers[port].stop(None)
    
    """
    with _reserve_port() as datanode_port:
        bind_address = "[::]:{}".format(datanode_port)
        print("Server binding to {}".format(bind_address))
        sys.stdout.flush()
        workers = []
        for _ in range(_PROCESS_COUNT):
            # Worker subprocesses are forked before gRPC DataNode servers start up
            worker = multiprocessing.Process(
                target=_run_server,
                args=(bind_address,)) 
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
    """
 
if __name__ == "__main__":
    serve()