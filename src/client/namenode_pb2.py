# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: namenode.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0enamenode.proto\x12\x11namenode.namenode\"2\n\nSourceFile\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x12\n\nsourcepath\x18\x02 \x01(\t\"\x1e\n\nSystemFile\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"\x17\n\x04\x46ile\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\x0c\"\x1b\n\x08Response\x12\x0f\n\x07message\x18\x01 \x01(\t2\xab\x01\n\x08NameNode\x12K\n\x0b\x43lientWrite\x12\x1d.namenode.namenode.SourceFile\x1a\x1b.namenode.namenode.Response\"\x00\x12R\n\x16\x43lientReadFromNameNode\x12\x1d.namenode.namenode.SystemFile\x1a\x17.namenode.namenode.File\"\x00\x62\x06proto3')



_SOURCEFILE = DESCRIPTOR.message_types_by_name['SourceFile']
_SYSTEMFILE = DESCRIPTOR.message_types_by_name['SystemFile']
_FILE = DESCRIPTOR.message_types_by_name['File']
_RESPONSE = DESCRIPTOR.message_types_by_name['Response']
SourceFile = _reflection.GeneratedProtocolMessageType('SourceFile', (_message.Message,), {
  'DESCRIPTOR' : _SOURCEFILE,
  '__module__' : 'namenode_pb2'
  # @@protoc_insertion_point(class_scope:namenode.namenode.SourceFile)
  })
_sym_db.RegisterMessage(SourceFile)

SystemFile = _reflection.GeneratedProtocolMessageType('SystemFile', (_message.Message,), {
  'DESCRIPTOR' : _SYSTEMFILE,
  '__module__' : 'namenode_pb2'
  # @@protoc_insertion_point(class_scope:namenode.namenode.SystemFile)
  })
_sym_db.RegisterMessage(SystemFile)

File = _reflection.GeneratedProtocolMessageType('File', (_message.Message,), {
  'DESCRIPTOR' : _FILE,
  '__module__' : 'namenode_pb2'
  # @@protoc_insertion_point(class_scope:namenode.namenode.File)
  })
_sym_db.RegisterMessage(File)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), {
  'DESCRIPTOR' : _RESPONSE,
  '__module__' : 'namenode_pb2'
  # @@protoc_insertion_point(class_scope:namenode.namenode.Response)
  })
_sym_db.RegisterMessage(Response)

_NAMENODE = DESCRIPTOR.services_by_name['NameNode']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SOURCEFILE._serialized_start=37
  _SOURCEFILE._serialized_end=87
  _SYSTEMFILE._serialized_start=89
  _SYSTEMFILE._serialized_end=119
  _FILE._serialized_start=121
  _FILE._serialized_end=144
  _RESPONSE._serialized_start=146
  _RESPONSE._serialized_end=173
  _NAMENODE._serialized_start=176
  _NAMENODE._serialized_end=347
# @@protoc_insertion_point(module_scope)
