# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import file_system_protocol_pb2 as file__system__protocol__pb2


class FileSystemStub(object):
    """Best practice states to keep everything as optional as no one can accurately predict the far future
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DownloadFile = channel.unary_stream(
                '/sdfs.FileSystem/DownloadFile',
                request_serializer=file__system__protocol__pb2.DownloadRequest.SerializeToString,
                response_deserializer=file__system__protocol__pb2.DownloadResponse.FromString,
                )
        self.UploadFile = channel.stream_unary(
                '/sdfs.FileSystem/UploadFile',
                request_serializer=file__system__protocol__pb2.UploadRequest.SerializeToString,
                response_deserializer=file__system__protocol__pb2.UploadResponse.FromString,
                )
        self.Connect = channel.unary_unary(
                '/sdfs.FileSystem/Connect',
                request_serializer=file__system__protocol__pb2.ConnectionRequest.SerializeToString,
                response_deserializer=file__system__protocol__pb2.ConnectionResponse.FromString,
                )
        self.Rename = channel.unary_unary(
                '/sdfs.FileSystem/Rename',
                request_serializer=file__system__protocol__pb2.RenameRequest.SerializeToString,
                response_deserializer=file__system__protocol__pb2.GenericResponse.FromString,
                )
        self.HeartBeat = channel.unary_unary(
                '/sdfs.FileSystem/HeartBeat',
                request_serializer=file__system__protocol__pb2.HeartBeatRequest.SerializeToString,
                response_deserializer=file__system__protocol__pb2.HeartBeatResponse.FromString,
                )


class FileSystemServicer(object):
    """Best practice states to keep everything as optional as no one can accurately predict the far future
    """

    def DownloadFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UploadFile(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Connect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Rename(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def HeartBeat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileSystemServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'DownloadFile': grpc.unary_stream_rpc_method_handler(
                    servicer.DownloadFile,
                    request_deserializer=file__system__protocol__pb2.DownloadRequest.FromString,
                    response_serializer=file__system__protocol__pb2.DownloadResponse.SerializeToString,
            ),
            'UploadFile': grpc.stream_unary_rpc_method_handler(
                    servicer.UploadFile,
                    request_deserializer=file__system__protocol__pb2.UploadRequest.FromString,
                    response_serializer=file__system__protocol__pb2.UploadResponse.SerializeToString,
            ),
            'Connect': grpc.unary_unary_rpc_method_handler(
                    servicer.Connect,
                    request_deserializer=file__system__protocol__pb2.ConnectionRequest.FromString,
                    response_serializer=file__system__protocol__pb2.ConnectionResponse.SerializeToString,
            ),
            'Rename': grpc.unary_unary_rpc_method_handler(
                    servicer.Rename,
                    request_deserializer=file__system__protocol__pb2.RenameRequest.FromString,
                    response_serializer=file__system__protocol__pb2.GenericResponse.SerializeToString,
            ),
            'HeartBeat': grpc.unary_unary_rpc_method_handler(
                    servicer.HeartBeat,
                    request_deserializer=file__system__protocol__pb2.HeartBeatRequest.FromString,
                    response_serializer=file__system__protocol__pb2.HeartBeatResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sdfs.FileSystem', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileSystem(object):
    """Best practice states to keep everything as optional as no one can accurately predict the far future
    """

    @staticmethod
    def DownloadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/sdfs.FileSystem/DownloadFile',
            file__system__protocol__pb2.DownloadRequest.SerializeToString,
            file__system__protocol__pb2.DownloadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UploadFile(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/sdfs.FileSystem/UploadFile',
            file__system__protocol__pb2.UploadRequest.SerializeToString,
            file__system__protocol__pb2.UploadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Connect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdfs.FileSystem/Connect',
            file__system__protocol__pb2.ConnectionRequest.SerializeToString,
            file__system__protocol__pb2.ConnectionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Rename(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdfs.FileSystem/Rename',
            file__system__protocol__pb2.RenameRequest.SerializeToString,
            file__system__protocol__pb2.GenericResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def HeartBeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sdfs.FileSystem/HeartBeat',
            file__system__protocol__pb2.HeartBeatRequest.SerializeToString,
            file__system__protocol__pb2.HeartBeatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
