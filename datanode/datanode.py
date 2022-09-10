"""

datanode.py is the gRPC server that will act as the volume server to store the data. Each server running
will be tied to a specific namespace.

"""
import grpc
import file_system_protocol_pb2
from file_system_protocol_pb2 import File, FileMetaData, UploadResponse, ConnectionResponse 
import file_system_protocol_pb2_grpc 
from concurrent import futures
import socket
import time
from datetime import timedelta
import os
import math

_ONE_DAY_IN_SECONDS = timedelta(days=1).total_seconds()
_VOLUME_SERVERS = None
# Current volume via port number
_CURRENT_VOLUME = None

class FileSystemServicer(file_system_protocol_pb2_grpc.FileSystemServicer):
	"""Provide method implementations of file system server"""
	def UploadFile(self, request_iterator, context):
		"""Supports uploading multiple files into file system. NOTE: This is write, not append in Pythond"""
		for upload_request in request_iterator:
			filename = upload_request.fileMetaData.name
			content = upload_request.uploadFile.content
			chunked_contents = self._chunk(content)
			datanode_store = _VOLUME_SERVERS[_CURRENT_VOLUME]['store']
			counter = 1
			for chunked_content in chunked_contents:
				filename_path = datanode_store + filename + "." + str(counter)
				# Write byte to text file
				with open(filename_path, 'wb') as f:
					f.write(chunked_content)
				counter = counter + 1
		return UploadResponse(status = 'upload success')
	
	def _chunk(self, content):
		# HDFS has a block size of 128 MB. Since this is a dummy project, we'll set this to 1 MB for text files (not images)
		block_size = 1000000
		for i in range(0, len(content), block_size):
			yield content[i:i+block_size]

	def Connect(self, request, context):
		global _CURRENT_VOLUME
		_CURRENT_VOLUME = request.volume 
		return ConnectionResponse(status = 'connection success') 

def _setup_datanode(count):
	user = os.path.expanduser("~")
	volume_dir = user + "/.sdfs/volumes/"
	namenode_dir = volume_dir + "datanode_" + count + "/"
	if not os.path.isdir(volume_dir):
		os.mkdir(volume_dir)
	if not os.path.isdir(namenode_dir):
		os.mkdir(namenode_dir)
	return namenode_dir

def _reserve_volume_ports():
	for _ in range(10):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(("", 0))
		try:
			yield sock.getsockname()[1]
		finally:
			sock.close()

def _print_ports_to_copy():
	ports = []
	for port in _VOLUME_SERVERS.keys():
		ports.append(str(port))
	print(*ports)

def _serve():
	global _VOLUME_SERVERS
	_VOLUME_SERVERS = {}
	count = 1
	try:
		# For now, we'll set SDFS to have 10 volume servers
		for port in _reserve_volume_ports():
			server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
			file_system_protocol_pb2_grpc.add_FileSystemServicer_to_server(FileSystemServicer(), server)
			server.add_insecure_port('[::]:{}'.format(port))
			server.start()
			datanode = _setup_datanode(str(count))
			_VOLUME_SERVERS[port] = {'server': server, 'store': datanode} 
			count = count + 1
		_print_ports_to_copy()
		while True:
			# Instead of waiting for termination, start servers and explicitly wait for KeyboardInterrupt to handle stop
			time.sleep(_ONE_DAY_IN_SECONDS)	
	except KeyboardInterrupt:
		for port in _VOLUME_SERVERS:
			print("Stopping volume server running at port {}".format(port))
			_VOLUME_SERVERS[port]['server'].stop(0)

if __name__ == '__main__':
	_serve()
