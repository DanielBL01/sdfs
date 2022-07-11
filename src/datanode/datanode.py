"""

gRPC Server Code for DataNode

The gRPC DataNode Servers will be multiprocessing based servers where
we instantiate one server per subprocess, balancing requests between
the servers using the SO_REUSEPORT socket option 

"""

from datetime import timedelta
import sys
import time
import os

from concurrent import futures
import multiprocessing
import socket
import contextlib

import grpc
from datanode_pb2 import File, Response
import datanode_pb2_grpc

_ONE_DAY = timedelta(days=1)
_PROCESS_COUNT = multiprocessing.cpu_count()
print("sdfs detects {} cores in this machine".format(_PROCESS_COUNT))
# For now, limit the of DataNode processes to three
if _PROCESS_COUNT > 3:
    print("Machine meets the hardware requirements")
    _PROCESS_COUNT = 3
    _THREAD_CONCURRENCY = _PROCESS_COUNT
else:
    print("Machine does not meet the hardware requirements")
    sys.exit()

parent_dir = "/Users/daniellee/.sdfs/"
datanode_dirs = {
    "datanode_1": "{}datanode_1/".format(parent_dir), 
    "datanode_2": "{}datanode_2/".format(parent_dir),
    "datanode_3": "{}datanode_3/".format(parent_dir)
}

class _DataNodeServicer(datanode_pb2_grpc.DataNodeServicer):

    def NameNodeWrite(self, request, context):
        active_process = os.environ("SUB_PROCESS_NUM")
        filename = request.filename
        content = request.content
        system_file_path = datanode_dirs[active_process] + filename
        with open(system_file_path, "wb") as system_binary_file:
            system_binary_file.write(content)
        return Response(message = "Successfully replicated to DataNode")

    def ClientReadFromDataNode(self, request, context):
        # Read rpc gets a SystemFile message and returns File message
        active_process = os.environ("SUB_PROCESS_NUM")
        filename = request.filename
        system_file_path = datanode_dirs[active_process] + filename
        with open(system_file_path, "rb") as system_binary_file:
            system_binary_file_content = system_binary_file.read()
        return File(content = system_binary_file_content) 

def _handle_dirs():
    for datanode_dir in datanode_dirs:
        if not os.path.isdir(datanode_dir):
            os.makedirs(datanode_dir)

def _wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        print("DataNode server ended with KeyboardInterrupt")
        server.stop(None)

def _run_server(bind_address, datanode_env_id):
    # Set env var in a subprocess
    os.environ["SUB_PROCESS_NUM"] = datanode_env_id 
    print("PID: {}, SUB_PROCESS_NUM: {}".format(os.getpid(), os.environ["SUB_PROCESS_NUM"]))
    # Start a server in a subprocess
    options = (("grpc.so_reuseport", 1),)
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=_THREAD_CONCURRENCY,),
        options=options
    )
    datanode_pb2_grpc.add_DataNodeServicer_to_server(
        _DataNodeServicer(),
        server)
    server.add_insecure_port(bind_address)
    server.start()
    _wait_forever(server)

@contextlib.contextmanager
def _reserve_port():
    # Find and reserve a port for all subprocesses to use
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT")
    sock.bind(("", 0))
    try:
        yield sock.getsockname()[1]
    finally:
        sock.close()

def serve():
    # Confirm/create necessary dirs
    _handle_dirs()
    with _reserve_port() as port:
        bind_address = "localhost:{}".format(port)
        print("Server binding to {}".format(bind_address))
        workers = []
        for i in range(_PROCESS_COUNT):
            worker = multiprocessing.Process(
                target=_run_server,
                args=(bind_address, "datanode_{}".format(i))
            )
            worker.start()
            workers.append(worker)
        for worker in workers:
            worker.join()
 
if __name__ == "__main__":
    serve()