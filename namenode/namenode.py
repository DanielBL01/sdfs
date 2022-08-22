"""

namenode.py is the gRPC client for the NameNode, The NameNode does not store data itself. However,
the NameNode is responsible for handling the FSImage and EditLog. The FSImage stores the complete snapshot
of the file system metadata at specific moments of time. The EditLog stores the incremental changes like
renaming or appending to a file for durability. This is so that SDFS does not have to create a new FSImage
snapshot each time the namespace is modified. This means there will be some latency.

"""

import grpc
import file_system_protocol_pb2
from file_system_protocol_pb2 import File, FileMetaData, UploadRequest
import file_system_protocol_pb2_grpc
import logging
import os

_EDIT_LOG = None
_FS_IMAGE = None
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
	return

def generate_file_iterator():
	file_name = "dummy.txt"
	file_name_2 = "dummy2.txt"
	metadata1 = FileMetaData(name = file_name)
	metadata2 = FileMetaData(name = file_name_2)
	content1 = None
	content2 = None
	with open("/Users/daniellee/dummy.txt", "rb") as f:
		content1 = f.read()
	with open("/Users/daniellee/dummy2.txt", "rb") as f2:
		content2 = f2.read()
	file1 = File(content = content1)
	file2 = File(content = content2)
	# Yield to return a generator for stream request
	yield UploadRequest(fileMetaData = metadata1, uploadFile = file1)
	yield UploadRequest(fileMetaData = metadata2, uploadFile = file2)

# Uploading a file takes in a request as a stream and outputs a response
# In gRPC lang, this is called a request-streaming RPC
def upload_file(stub):
	# Uploading a file takes in a request as a stream and outputs a response
	# In gRPC lang, this is called a request-streaming RPC
	
	# This should be done with argparse, but for now, let's do it manually
	# This should be done using yield to create the generator when we read the files one by one
	file_iterator = generate_file_iterator()
	response = stub.UploadFile(file_iterator)
	print(response)
	
def run():
	with grpc.insecure_channel('localhost:50051') as channel:
		stub = file_system_protocol_pb2_grpc.FileSystemStub(channel)
		upload_file(stub)

if __name__ == '__main__':
	_setup_namespace()
    # run()
