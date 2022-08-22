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

channel = grpc.insecure_channel('localhost:50051')
stub = file_system_protocol_pb2_grpc.FileSystemStub(channel)

# Uploading a file takes in a request as a stream and outputs a response
# In gRPC lang, this is called a request-streaming RPC

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
	run()
