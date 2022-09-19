"""

namenode.py is the gRPC client for the NameNode, The NameNode does not store data itself. However,
the NameNode is responsible for handling the FSImage and EditLog. The FSImage stores the complete snapshot
of the file system metadata at specific moments of time. The EditLog stores the incremental changes like
renaming or appending to a file for durability. This is so that SDFS does not have to create a new FSImage
snapshot each time the namespace is modified. This means there will be some latency.

"""

import grpc
import file_system_protocol_pb2
from file_system_protocol_pb2 import File, FileMetaData, UploadRequest, ConnectionRequest, HeartBeatRequest
import file_system_protocol_pb2_grpc
import logging
import os
import argparse
import random
import threading
import time

_EDIT_LOG = None
_FS_IMAGE = None
_VOLUME_PORTS = None
_VOLUME_STUBS = None
_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

def _setup_logger(name, log_file, level=logging.INFO):
	"""Helper method to Setup logging for both fsimage and editlog"""
	handler = logging.FileHandler(log_file)
	handler.setFormatter(_FORMATTER)
	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(handler)
	return logger

def _setup_namespace():
	global _EDIT_LOG
	global _FS_IMAGE
	user = os.path.expanduser("~")
	parent_dir = user + "/.sdfs/"
	namenode_dir = parent_dir + "namenode/"
	if not os.path.isdir(parent_dir):
		os.mkdir(parent_dir)
	if not os.path.isdir(namenode_dir):
		os.mkdir(namenode_dir)
	edit_log_file = namenode_dir + "edit.log"
	_EDIT_LOG = _setup_logger("editlog", edit_log_file)
	fs_image_file = namenode_dir + "fsimage.log"
	_FS_IMAGE = _setup_logger("fsimage", fs_image_file)
	# _EDIT_LOG.info("Testing writing to logger")

def _update_internal_fsimage():
	# At time intervals, update the complete file system namespace using editlog
	# Since we want to continuously run an update fs image function in the background, we can keep it as a seperate thread
	return

def heartbeat_check_datanodes():
	# Implement heartbeat check of all gRPC server given their localhost ports
	while (True):
		if (_EDIT_LOG and _VOLUME_STUBS):
			request = HeartBeatRequest()
			for port in _VOLUME_STUBS.keys():
				stub = _VOLUME_STUBS[port]
				response = stub.HeartBeat(request)
				if (response):
					_EDIT_LOG.info("Volume server running on port {} is alive!".format(port))
			time.sleep(5)
		else:
			continue

def run_heartbeat():
	# Run the heartbeat check in a different thread to run asynchronously in the background
	# Run the thread as a daemon such that when __main__ ends, the daemon is killed
	heartbeat = threading.Thread(target=heartbeat_check_datanodes, daemon=True)
	heartbeat.start()

def _parse_arguments():
	# No way a client can know which servers are available unless specified
	parser = argparse.ArgumentParser(description = 'List volume servers.')
	parser.add_argument('-ports', nargs='+', type=int)
	args = parser.parse_args()
	return args.ports

def _init_volume_stubs():
	if (_VOLUME_PORTS):
		global _VOLUME_STUBS
		_VOLUME_STUBS = {}
		for port in _VOLUME_PORTS:
			channel = grpc.insecure_channel('localhost:{}'.format(port))
			stub = file_system_protocol_pb2_grpc.FileSystemStub(channel)
			_VOLUME_STUBS[port] = stub

def generate_file_iterator(text_list):
	user = os.path.expanduser("~")
	for text_file in text_list:
		metadata = FileMetaData(name = text_file)
		with open(user + "/" + text_file, "rb") as f:
			content = f.read()
			upload_file = File(content = content)
			yield UploadRequest(fileMetaData = metadata, uploadFile = upload_file)

# Uploading a file takes in a request as a stream and outputs a response. This is a request-streaming RPC
def _upload_file(stub):
	# This should be user input but that should be easy to implement
	text_list = ["dummy.txt", "dummy2.txt"]
	file_iterator = generate_file_iterator(text_list)
	response = stub.UploadFile(file_iterator)
	logs = response.logs
	# Upload file is a request stream so it's possible to have multiple "put" logs
	for log in logs:
		_EDIT_LOG.info(log)

def _run():
	global _VOLUME_PORTS
	_VOLUME_PORTS = _parse_arguments()
	_init_volume_stubs()
	random_port = random.choice(_VOLUME_PORTS)
	connection_volume = ConnectionRequest(volume = random_port)
	channel = grpc.insecure_channel('localhost:{}'.format(random_port))
	stub = file_system_protocol_pb2_grpc.FileSystemStub(channel)
	_setup_namespace()
	connection_response = stub.Connect(connection_volume)
	print(connection_response)
	_upload_file(stub)
	run_heartbeat()

if __name__ == '__main__':
	_run()
	while (True):
		continue
