# Simple Distributed File System

### Technologies
	- Python
		Why? Quick for prototyping and implementing mechanisms
	- gRPC
		Why? High performance rpc's with great support from Google
	- Bazel
		Why? Nice to have for building and testing efficiently

### What we are implementing
- Leader-based replication on a distributed file system 
- Heartbeat for DataNodes to let NameNode know of its condition
- Spliting files into chunks to handle large files
