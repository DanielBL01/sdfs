# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: serveGet.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eserveGet.proto\"\"\n\x0eGetFileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\":\n\x0fGetFileResponse\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x15\n\rfile_as_bytes\x18\x02 \x01(\x0c\x32\x38\n\x08ServeGet\x12,\n\x07GetFile\x12\x0f.GetFileRequest\x1a\x10.GetFileResponseb\x06proto3')



_GETFILEREQUEST = DESCRIPTOR.message_types_by_name['GetFileRequest']
_GETFILERESPONSE = DESCRIPTOR.message_types_by_name['GetFileResponse']
GetFileRequest = _reflection.GeneratedProtocolMessageType('GetFileRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETFILEREQUEST,
  '__module__' : 'serveGet_pb2'
  # @@protoc_insertion_point(class_scope:GetFileRequest)
  })
_sym_db.RegisterMessage(GetFileRequest)

GetFileResponse = _reflection.GeneratedProtocolMessageType('GetFileResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETFILERESPONSE,
  '__module__' : 'serveGet_pb2'
  # @@protoc_insertion_point(class_scope:GetFileResponse)
  })
_sym_db.RegisterMessage(GetFileResponse)

_SERVEGET = DESCRIPTOR.services_by_name['ServeGet']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETFILEREQUEST._serialized_start=18
  _GETFILEREQUEST._serialized_end=52
  _GETFILERESPONSE._serialized_start=54
  _GETFILERESPONSE._serialized_end=112
  _SERVEGET._serialized_start=114
  _SERVEGET._serialized_end=170
# @@protoc_insertion_point(module_scope)
