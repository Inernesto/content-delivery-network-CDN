# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: replication.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'replication.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11replication.proto\x12\x0breplication\"3\n\x12ReplicationRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"7\n\x13ReplicationResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\xbc\x01\n\x11\x43ontentReplicator\x12Q\n\nAddContent\x12\x1f.replication.ReplicationRequest\x1a .replication.ReplicationResponse\"\x00\x12T\n\rRemoveContent\x12\x1f.replication.ReplicationRequest\x1a .replication.ReplicationResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'replication_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REPLICATIONREQUEST']._serialized_start=34
  _globals['_REPLICATIONREQUEST']._serialized_end=85
  _globals['_REPLICATIONRESPONSE']._serialized_start=87
  _globals['_REPLICATIONRESPONSE']._serialized_end=142
  _globals['_CONTENTREPLICATOR']._serialized_start=145
  _globals['_CONTENTREPLICATOR']._serialized_end=333
# @@protoc_insertion_point(module_scope)