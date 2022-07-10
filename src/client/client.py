"""

The NameNode will be the gRPC client that will be connected to multiple DataNode services which will act as
the gRPC servers

The NameNode creates a stub to call service methods. From the stub, we call the service methods
which was defined in the proto called GetFile which takes as an argument FileRequest to return 
a FileResponse

"""

import os

import grpc
import namenode_pb2
import namenode_pb2_grpc
import datanode_pb2
import datanode_pb2_grpc

from flask import Flask, request

app = Flask(__name__)

parent_dir = "/Users/daniellee/.sdfs/"
host = os.getenv("HOST", "localhost")
namenode_channel = grpc.insecure_channel(f"{host}:9000")
datanode_channel = grpc.insecure_channel(f"{host}:8080")
""" A stub exists to call service defined in .proto """
namenode_stub = namenode_pb2_grpc.NameNodeStub(namenode_channel) 
datanode_stub = datanode_pb2_grpc.DataNodeStub(datanode_channel)

@app.route("/", methods=["GET", "POST"])
def handle():
	if request.method == "POST":
		filename = request.get_json()["name"]
		sourcepath = request.get_json()["path"] 
		write_request = namenode_pb2.SourceFile(
			filename = filename,
			sourcepath = sourcepath 
		)
		namenode_stub.ClientWrite(write_request)
		return "post sucess\n"
	elif request.method == "GET":
		filename = request.get_json()["name"]
		read_request = datanode_pb2.SystemFile(filename = filename)
		print(datanode_stub.ClientReadFromDataNode(read_request))
		return "get success\n"

if __name__ == "__main__":
	app.run(debug=True)