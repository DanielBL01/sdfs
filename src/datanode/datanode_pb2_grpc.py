# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import datanode_pb2 as datanode__pb2


class DataNodeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NameNodeWrite = channel.unary_unary(
                '/proto3.datanode.DataNode/NameNodeWrite',
                request_serializer=datanode__pb2.SystemFileData.SerializeToString,
                response_deserializer=datanode__pb2.Response.FromString,
                )
        self.ClientReadFromDataNode = channel.unary_unary(
                '/proto3.datanode.DataNode/ClientReadFromDataNode',
                request_serializer=datanode__pb2.SystemFile.SerializeToString,
                response_deserializer=datanode__pb2.File.FromString,
                )


class DataNodeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def NameNodeWrite(self, request, context):
        """NOTE: DataNode is not client facing, this write only happens from NameNode
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClientReadFromDataNode(self, request, context):
        """Client reads from DataNode
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataNodeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'NameNodeWrite': grpc.unary_unary_rpc_method_handler(
                    servicer.NameNodeWrite,
                    request_deserializer=datanode__pb2.SystemFileData.FromString,
                    response_serializer=datanode__pb2.Response.SerializeToString,
            ),
            'ClientReadFromDataNode': grpc.unary_unary_rpc_method_handler(
                    servicer.ClientReadFromDataNode,
                    request_deserializer=datanode__pb2.SystemFile.FromString,
                    response_serializer=datanode__pb2.File.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto3.datanode.DataNode', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DataNode(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def NameNodeWrite(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto3.datanode.DataNode/NameNodeWrite',
            datanode__pb2.SystemFileData.SerializeToString,
            datanode__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClientReadFromDataNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto3.datanode.DataNode/ClientReadFromDataNode',
            datanode__pb2.SystemFile.SerializeToString,
            datanode__pb2.File.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
