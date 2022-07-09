"""

Implement the servicer interface generated from service definition with functions 
that perform the actual "work" of the service

Also need a running gRPC server to listen for requests from clients and transmit responses

"""

import os
from concurrent import futures

import grpc
from serveGet_pb2 import GetFileResponse 
from servePut_pb2 import PutFileResponse 
import serveGet_pb2_grpc
import servePut_pb2_grpc

parent_dir = "/Users/daniellee/.sdfs/"

class GetFileService(serveGet_pb2_grpc.ServeGetServicer):
	""" Functions in services classes must be defined in the RPC """
	def GetFile(self, request, context):
		try:
			filename = request.filename
			if os.path.exists(parent_dir + filename.strip()):
				binary_file = open(parent_dir + filename, "rb")
				with open(parent_dir + filename, "rb") as binary_file:
					response = GetFileResponse(filename = filename, file_as_bytes = binary_file.read())
					binary_file.close()
					return response
			else:
				print("Could not find the file in the filesystem")
		except Exception as e:
			print(e)

class PutFileService(servePut_pb2_grpc.ServePutServicer):
	def PutFile(self, request, context):
		try:
			filename = request.filename
			file_in_bytes = request.file_as_bytes
			with open(parent_dir + filename, "wb") as binary_file:
				binary_file.write(file_in_bytes)
				response = PutFileResponse(status = filename + " has been saved to filesystem")
				binary_file.close()
				return response
		except Exception as e:
			print(e)

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	serveGet_pb2_grpc.add_ServeGetServicer_to_server(GetFileService(), server)
	servePut_pb2_grpc.add_ServePutServicer_to_server(PutFileService(), server)	
	server.add_insecure_port("[::]:50051")
	server.start()
	server.wait_for_termination()

if __name__ == "__main__":
	if not os.path.isdir(parent_dir):
		os.makedirs(parent_dir)
	else:
		print("/Users/daniellee/.sdfs/ already exists")
	serve()	
