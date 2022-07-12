"""

Node Manager

Currently, we're going to have two gRPC based servers running. One for NameNode
and the other for DataNode. Although we have a client service which is user-facing,
internally, sdfs will use a separate client called Node Manager to open stubs to 
communicate between the two servers to implement mechanisms like Replication,
heartbeat and more

First we've going to implement something really simple for replication for proof of concept.
There won't be any replication log and everything will be manual

"""

import logging
import argparse
import os
from datetime import timedelta
import time
import multiprocessing

import grpc
import datanode_pb2
import datanode_pb2_grpc

# Configure logger to be at the lowest level i.e. INFO to log everything
logging.basicConfig(
    filename="node_manager.log", 
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")
_LOGGER = logging.getLogger(__name__)

_ONE_DAY = timedelta(days=1)

datanode_stubs = {}
host = os.getenv("HOST", "localhost")

"""
_PROCESS_COUNT = 3

_datanode_channel_singleton = None
_datanode_stub_singleton = None

def _stop_datanode_channel():
    _LOGGER.info("Shutting down datanode process")
    if _datanode_channel_singleton is not None:
        _datanode_channel_singleton.close()

def _initialize_datanode(datanode_server_address):
    # Note to self: In Python, to modify global vars need global keyword
    global _datanode_channel_singleton
    global _datanode_stub_singleton
    _datanode_channel_singleton = grpc.insecure_channel(datanode_server_address)
    _datanode_stub_singleton = datanode_pb2_grpc.DataNodeStub(
        _datanode_channel_singleton)
    atexit.register(_stop_datanode_channel)

def _run_namenode_write_service(filename):
    print(os.getpid())
    _LOGGER.info("Replicating {}".format(filename))
    # Run the NameNodeWrite defined in the datanode protocol buffer for replication
    response = _datanode_stub_singleton.NameNodeWrite(
        datanode_pb2.SystemFileData(
            filename = "test_one.txt",
            content = str.encode("This is {} garbage text".format(filename))))
    _LOGGER.info(response.message)
    return response

def _replicate_to_datanodes(datanode_server_address):	
    datanode_pool = multiprocessing.Pool(processes=_PROCESS_COUNT, initializer=_initialize_datanode, initargs=(datanode_server_address,))
    filenames = range(3)
    return datanode_pool.map(_run_namenode_write_service, filenames)

"""
def _replication():
    if datanode_stubs is not None:
        for datanode_stub in datanode_stubs:
            datanode_stubs[datanode_stub].NameNodeWrite(
                datanode_pb2.SystemFileData(
                    filename = "test_one.txt",
                    content = str.encode("This is some garbage text for testing"),
                    datanode_id = datanode_stub))
            print("test_one.txt has been replicated on {}".format(datanode_stub))

def serve():
    # I know this looks very hard coded but the current implementation simply calls for a strict set of 3 DataNodes 
    msg = "Connect to a set of DataNode servers to replicate a distributed filesystem"
    parser = argparse.ArgumentParser(description=msg)
    process_count = multiprocessing.cpu_count()
    for i in range(1, process_count + 1):
        # This is a position argument so the datanode server must be the first argument after the script name
        parser.add_argument("datanode_{}_port".format(i), help="The datanode_{} server port number (e.g. 12345)".format(i))
    args = parser.parse_args()
    datanode_channels = []
    # A simple way to iterate through args namespace
    global datanode_stubs
    incr_id = 0
    for arg in vars(args):
        datanode_channels.append(grpc.insecure_channel("{}:{}".format(host, getattr(args, arg))))
        datanode_stubs["datanode_{}".format(incr_id + 1)] = datanode_pb2_grpc.DataNodeStub(datanode_channels[incr_id])
        incr_id = incr_id + 1
    
    _replication()

    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        print("Closing all datanode channels")
        for datanode_channel in datanode_channels:
            datanode_channel.close()
    
if __name__ == "__main__":
    serve()