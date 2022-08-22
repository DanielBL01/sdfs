"""

datanode.py is the gRPC server that will act as the volume server to store the data. Each server running
will be tied to a specific namespace.

"""
import grpc
import file_system_protocol_pb2
from file_system_protocol_pb2 import File, FileMetaData, UploadResponse 
import file_system_protocol_pb2_grpc 
from concurrent import futures
import socket
import time
from datetime import timedelta

_ONE_DAY = timedelta(days=1)

class FileSystemServicer(file_system_protocol_pb2_grpc.FileSystemServicer):
	"""Provide method implementations of file system server"""
	def __init__(self):
		print("File System Servicer")

	def UploadFile(self, request_iterator, context):
		"""Supports uploading multiple files into file system"""
		for upload_request in request_iterator:
			meta_data = upload_request.fileMetaData.name
			content = upload_request.uploadFile.content
			content_str = content.decode('utf-8')
			print("Meta data: " + meta_data + ", content: " + content_str)
		return UploadResponse(status = 'success')

def _reserve_volume_ports():
	for _ in range(3):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(("", 0))
		try:
			yield sock.getsockname()[1]
		finally:
			sock.close()

def _serve():
	volume_servers = {}
	try:
		# For now, we'll set SDFS to have 3 volume servers
		for port in _reserve_volume_ports():
			print(port)
			server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
			file_system_protocol_pb2_grpc.add_FileSystemServicer_to_server(FileSystemServicer(), server)
			server.add_insecure_port('[::]:{}'.format(port))
			server.start()
			print("Running volume server at port {}".format(port))
			volume_servers[port] = server
		while True:
			# Instead of waiting for termination, start servers and explicitly wait for KeyboardInterrupt to handle stop
			time.sleep(_ONE_DAY.total_seconds())	
	except KeyboardInterrupt:
		for port in volume_servers:
			print("Stopping volume server running at port {}".format(port))
			volume_servers[port].stop(None)

if __name__ == '__main__':
	_serve()
