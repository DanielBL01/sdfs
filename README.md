# Simple Distributed File System

### Technologies
	- Python
		**Why?** Quick for prototyping and implementing mechanisms
	- Flask
		**Why?** Simple micro web framework to build REST endpoints
	- gRPC
		**Why?** High performance rpc's with great support from Google
	- Bazel
		**Why?** Nice to have for building and testing efficiently

### What we are implementing
- Leader-based replication on a distributed file system 
- Heartbeat for DataNodes to let NameNode know of its condition
- Spliting files into chunks to handle large files

### Project Architecture
<img width="394" alt="Screen Shot 2022-07-09 at 11 08 00 PM" src="https://user-images.githubusercontent.com/58889021/178129703-06e5e0a1-a9f3-4ec1-9d16-60a192f67305.png">
