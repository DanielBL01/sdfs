# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: datanode.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x64\x61tanode.proto\x12\x0fproto3.datanode\"H\n\x0eSystemFileData\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\x12\x13\n\x0b\x64\x61tanode_id\x18\x03 \x01(\t\"\x1e\n\nSystemFile\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"\x17\n\x04\x46ile\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\x0c\"\x1b\n\x08Response\x12\x0f\n\x07message\x18\x01 \x01(\t2\xa9\x01\n\x08\x44\x61taNode\x12M\n\rNameNodeWrite\x12\x1f.proto3.datanode.SystemFileData\x1a\x19.proto3.datanode.Response\"\x00\x12N\n\x16\x43lientReadFromDataNode\x12\x1b.proto3.datanode.SystemFile\x1a\x15.proto3.datanode.File\"\x00\x62\x06proto3')



_SYSTEMFILEDATA = DESCRIPTOR.message_types_by_name['SystemFileData']
_SYSTEMFILE = DESCRIPTOR.message_types_by_name['SystemFile']
_FILE = DESCRIPTOR.message_types_by_name['File']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
SystemFileData = _reflection.GeneratedProtocolMessageType('SystemFileData', (_message.Message,), {
  'DESCRIPTOR' : _SYSTEMFILEDATA,
  '__module__' : 'datanode_pb2'
  # @@protoc_insertion_point(class_scope:proto3.datanode.SystemFileData)
  })
_sym_db.RegisterMessage(SystemFileData)

SystemFile = _reflection.GeneratedProtocolMessageType('SystemFile', (_message.Message,), {
  'DESCRIPTOR' : _SYSTEMFILE,
  '__module__' : 'datanode_pb2'
  # @@protoc_insertion_point(class_scope:proto3.datanode.SystemFile)
  })
_sym_db.RegisterMessage(SystemFile)

File = _reflection.GeneratedProtocolMessageType('File', (_message.Message,), {
  'DESCRIPTOR' : _FILE,
  '__module__' : 'datanode_pb2'
  # @@protoc_insertion_point(class_scope:proto3.datanode.File)
  })
_sym_db.RegisterMessage(File)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'datanode_pb2'
  # @@protoc_insertion_point(class_scope:proto3.datanode.Response)
  })
_sym_db.RegisterMessage(Response)

_DATANODE = DESCRIPTOR.services_by_name['DataNode']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SYSTEMFILEDATA._serialized_start=35
  _SYSTEMFILEDATA._serialized_end=107
  _SYSTEMFILE._serialized_start=109
  _SYSTEMFILE._serialized_end=139
  _FILE._serialized_start=141
  _FILE._serialized_end=164
  _RESPONSE._serialized_start=166
  _RESPONSE._serialized_end=193
  _DATANODE._serialized_start=196
  _DATANODE._serialized_end=365
# @@protoc_insertion_point(module_scope)