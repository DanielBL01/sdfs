"""

The NameNode will be the gRPC client that will be connected to multiple DataNode services which will act as
the gRPC servers

The NameNode creates a stub to call service methods. From the stub, we call the service methods
which was defined in the proto called GetFile which takes as an argument FileRequest to return 
a FileResponse

"""

import os

import grpc
from serveGet_pb2 import GetFileRequest
from servePut_pb2 import PutFileRequest
from serveGet_pb2_grpc import ServeGetStub 
from servePut_pb2_grpc import ServePutStub

from flask import Flask, request

app = Flask(__name__)

parent_dir = "~/.sdfs/"
host = os.getenv("HOST", "localhost")
channel = grpc.insecure_channel(f"{host}:50051")
getFileStub = ServeGetStub(channel)
putFileStub = ServePutStub(channel)

@app.route("/", methods=["GET", "POST"])
def handle():
	if request.method == "POST":
		filename = request.get_json()["name"]
		filepath = request.get_json()["path"] 
		with open(filepath, "rb") as binary_file:
			put_request = PutFileRequest(filename = filename, file_as_bytes = binary_file.read()) 
			putFileStub.PutFile(put_request)
			return "post sucess"
	elif request.method == "GET":
		filename = request.get_json()["name"]
		get_request = GetFileRequest(filename = filename)
		print(getFileStub.GetFile(get_request))
		return "get success"
