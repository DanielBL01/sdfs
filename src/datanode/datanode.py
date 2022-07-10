"""

gRPC Server Code for DataNode

The gRPC DataNode Servers will be multiprocessing based servers which
will detect number of cores in a machine and spin up instances

"""

from datetime import timedelta
import time
import os
from concurrent import futures
import multiprocessing

import grpc
from datanode_pb2 import File, Response
import datanode_pb2_grpc

_ONE_DAY = timedelta(days=1)
_PROCESS_COUNT = multiprocessing.cpu_count()
""" For now, limit the of DataNode processes to three """
if _PROCESS_COUNT > 4:
    _PROCESS_COUNT = 3
_THREAD_CONCURRENCY = _PROCESS_COUNT

parent_dir = "/Users/daniellee/.sdfs/"
datanode_dir = parent_dir + "datanode/"

class _DataNodeServicer(datanode_pb2_grpc.DataNodeServicer):

    def NameNodeWrite(self, request, context):
        filename = request.filename
        content = request.content
        system_file_path = datanode_dir + filename
        with open(system_file_path, "wb") as system_binary_file:
            system_binary_file.write(content)
            system_binary_file.close()
        return Response(message = "Successfully replicated to DataNode")

    def ClientReadFromDataNode(self, request, context):
        """ Read rpc gets a SystemFile message and returns File message """
        filename = request.filename
        system_file_path = datanode_dir + filename
        with open(system_file_path, "rb") as system_binary_file:
            system_binary_file_content = system_binary_file.read()
            return File(content = system_binary_file_content) 

def _handle_dirs():
    if not os.path.isdir(datanode_dir):
        os.makedirs(datanode_dir)
    else:
        print("{} exists".format(datanode_dir))

def _wait_forever(server):
    try:
        while True:
            time.sleep(_ONE_DAY.seconds())
    except KeyboardInterrupt:
        server.stop(None)

def _run_server(bind_address):
    """ Start a server in a subprocess """
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

def serve():
    _handle_dirs()
    bind_address = "[::]:8080"
    workers = []
    for _ in range(_PROCESS_COUNT):
        worker = multiprocessing.Process(
            target=_run_server,
            args=(bind_address,)
        )
        worker.start()
        workers.append(worker)
    for worker in workers:
        worker.join()
 
if __name__ == "__main__":
    serve()