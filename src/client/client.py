"""

The NameNode will be the gRPC client that will be connected to multiple 
DataNode services which will act as the gRPC servers

The NameNode creates a stub to call service methods. From the stub, 
we call the service methods which was defined in the proto called 
GetFile which takes as an argument FileRequest to return a FileResponse

--- UPDATE 1 ---

What changed? Last time I tried to create multiple instances of a server
on a single backend on datanode using different ports i.e. creating
the grpc server, adding the get and post services to the server
and starting the server on a specific port.

What I did differently now is create two separate services (microservices)
for the namenode and datanode and create a separate client instead of 
having a namenode as the client. So a namenode server is running as well
as a datanode server.

--- UPDATE 2 --- 

Now we are using multiprocessing based servers for our datanodes. This
means the client will have to change to handle this new implementation

"""

import os

import grpc
import namenode_pb2
import namenode_pb2_grpc
#import datanode_pb2
#import datanode_pb2_grpc

from flask import Flask, request

app = Flask(__name__)

parent_dir = "/Users/daniellee/.sdfs/"
host = os.getenv("HOST", "localhost")

@app.route("/", methods=["GET", "POST"])
def handle():
	""" Each method will create an instance of a channel and close """
	namenode_channel = grpc.insecure_channel(f"{host}:9000")
	#datanode_channel = grpc.insecure_channel(f"{host}:8080")
	""" A stub exists to call service defined in .proto """
	namenode_stub = namenode_pb2_grpc.NameNodeStub(namenode_channel)
	#datanode_stub = datanode_pb2_grpc.DataNodeStub(datanode_channel)

	""" Accept application/json in curl requests """
	if request.method == "POST":
		filename = request.get_json()["name"]
		sourcepath = request.get_json()["path"] 
		write_request = namenode_pb2.SourceFile(
			filename = filename,
			sourcepath = sourcepath 
		)
		namenode_stub.ClientWrite(write_request)
		namenode_channel.close()
		return "post sucess"
	
	#elif request.method == "GET":
	#	filename = request.get_json()["name"]
	#	read_request = datanode_pb2.SystemFile(filename = filename)
	#	print(datanode_stub.ClientReadFromDataNode(read_request))
	#	return "get success"

if __name__ == "__main__":
	app.run(debug=True)