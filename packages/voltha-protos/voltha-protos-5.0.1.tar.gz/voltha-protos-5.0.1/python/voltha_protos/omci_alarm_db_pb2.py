# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: voltha_protos/omci_alarm_db.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from voltha_protos import meta_pb2 as voltha__protos_dot_meta__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='voltha_protos/omci_alarm_db.proto',
  package='omci',
  syntax='proto3',
  serialized_options=b'\n\030org.opencord.voltha.omciZ,github.com/opencord/voltha-protos/v5/go/omci',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n!voltha_protos/omci_alarm_db.proto\x12\x04omci\x1a\x18voltha_protos/meta.proto\"8\n\x12\x41larmAttributeData\x12\x13\n\x04name\x18\x01 \x01(\tB\x05\xe8\xf6\xcd\x1d\x01\x12\r\n\x05value\x18\x02 \x01(\t\"\x8d\x01\n\x11\x41larmInstanceData\x12\x1a\n\x0binstance_id\x18\x01 \x01(\rB\x05\xe8\xf6\xcd\x1d\x01\x12\x0f\n\x07\x63reated\x18\x02 \x01(\t\x12\x10\n\x08modified\x18\x03 \x01(\t\x12\x39\n\nattributes\x18\x04 \x03(\x0b\x32\x18.omci.AlarmAttributeDataB\x0b\xe2\xf6\xcd\x1d\x06\n\x04name\"i\n\x0e\x41larmClassData\x12\x17\n\x08\x63lass_id\x18\x01 \x01(\rB\x05\xe8\xf6\xcd\x1d\x01\x12>\n\tinstances\x18\x02 \x03(\x0b\x32\x17.omci.AlarmInstanceDataB\x12\xe2\xf6\xcd\x1d\r\n\x0binstance_id\"B\n\x12\x41larmManagedEntity\x12\x17\n\x08\x63lass_id\x18\x01 \x01(\rB\x05\xe8\xf6\xcd\x1d\x01\x12\x13\n\x04name\x18\x02 \x01(\tB\x05\xe8\xf6\xcd\x1d\x01\"/\n\x10\x41larmMessageType\x12\x1b\n\x0cmessage_type\x18\x01 \x01(\rB\x05\xe8\xf6\xcd\x1d\x01\"\x9d\x02\n\x0f\x41larmDeviceData\x12\x18\n\tdevice_id\x18\x01 \x01(\tB\x05\xe8\xf6\xcd\x1d\x01\x12\x0f\n\x07\x63reated\x18\x02 \x01(\t\x12\x1b\n\x13last_alarm_sequence\x18\x03 \x01(\r\x12\x16\n\x0elast_sync_time\x18\x04 \x01(\t\x12\x0f\n\x07version\x18\x05 \x01(\r\x12\x36\n\x07\x63lasses\x18\x06 \x03(\x0b\x32\x14.omci.AlarmClassDataB\x0f\xe2\xf6\xcd\x1d\n\n\x08\x63lass_id\x12\x32\n\x10managed_entities\x18\x07 \x03(\x0b\x32\x18.omci.AlarmManagedEntity\x12-\n\rmessage_types\x18\x08 \x03(\x0b\x32\x16.omci.AlarmMessageType\"?\n\x16\x41larmOpenOmciEventType\"%\n\x11OpenOmciEventType\x12\x10\n\x0cstate_change\x10\x00\"`\n\x12\x41larmOpenOmciEvent\x12<\n\x04type\x18\x01 \x01(\x0e\x32..omci.AlarmOpenOmciEventType.OpenOmciEventType\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\tBH\n\x18org.opencord.voltha.omciZ,github.com/opencord/voltha-protos/v5/go/omcib\x06proto3'
  ,
  dependencies=[voltha__protos_dot_meta__pb2.DESCRIPTOR,])



_ALARMOPENOMCIEVENTTYPE_OPENOMCIEVENTTYPE = _descriptor.EnumDescriptor(
  name='OpenOmciEventType',
  full_name='omci.AlarmOpenOmciEventType.OpenOmciEventType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='state_change', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=809,
  serialized_end=846,
)
_sym_db.RegisterEnumDescriptor(_ALARMOPENOMCIEVENTTYPE_OPENOMCIEVENTTYPE)


_ALARMATTRIBUTEDATA = _descriptor.Descriptor(
  name='AlarmAttributeData',
  full_name='omci.AlarmAttributeData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='omci.AlarmAttributeData.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\366\315\035\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='omci.AlarmAttributeData.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=69,
  serialized_end=125,
)


_ALARMINSTANCEDATA = _descriptor.Descriptor(
  name='AlarmInstanceData',
  full_name='omci.AlarmInstanceData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance_id', full_name='omci.AlarmInstanceData.instance_id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\366\315\035\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created', full_name='omci.AlarmInstanceData.created', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='modified', full_name='omci.AlarmInstanceData.modified', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='attributes', full_name='omci.AlarmInstanceData.attributes', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\342\366\315\035\006\n\004name', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=128,
  serialized_end=269,
)


_ALARMCLASSDATA = _descriptor.Descriptor(
  name='AlarmClassData',
  full_name='omci.AlarmClassData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='class_id', full_name='omci.AlarmClassData.class_id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\366\315\035\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='instances', full_name='omci.AlarmClassData.instances', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\342\366\315\035\r\n\013instance_id', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=271,
  serialized_end=376,
)


_ALARMMANAGEDENTITY = _descriptor.Descriptor(
  name='AlarmManagedEntity',
  full_name='omci.AlarmManagedEntity',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='class_id', full_name='omci.AlarmManagedEntity.class_id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\366\315\035\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='omci.AlarmManagedEntity.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\366\315\035\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=378,
  serialized_end=444,
)


_ALARMMESSAGETYPE = _descriptor.Descriptor(
  name='AlarmMessageType',
  full_name='omci.AlarmMessageType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message_type', full_name='omci.AlarmMessageType.message_type', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\366\315\035\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=446,
  serialized_end=493,
)


_ALARMDEVICEDATA = _descriptor.Descriptor(
  name='AlarmDeviceData',
  full_name='omci.AlarmDeviceData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='device_id', full_name='omci.AlarmDeviceData.device_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\350\366\315\035\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created', full_name='omci.AlarmDeviceData.created', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_alarm_sequence', full_name='omci.AlarmDeviceData.last_alarm_sequence', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_sync_time', full_name='omci.AlarmDeviceData.last_sync_time', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='omci.AlarmDeviceData.version', index=4,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='classes', full_name='omci.AlarmDeviceData.classes', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\342\366\315\035\n\n\010class_id', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='managed_entities', full_name='omci.AlarmDeviceData.managed_entities', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='message_types', full_name='omci.AlarmDeviceData.message_types', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=496,
  serialized_end=781,
)


_ALARMOPENOMCIEVENTTYPE = _descriptor.Descriptor(
  name='AlarmOpenOmciEventType',
  full_name='omci.AlarmOpenOmciEventType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ALARMOPENOMCIEVENTTYPE_OPENOMCIEVENTTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=783,
  serialized_end=846,
)


_ALARMOPENOMCIEVENT = _descriptor.Descriptor(
  name='AlarmOpenOmciEvent',
  full_name='omci.AlarmOpenOmciEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='omci.AlarmOpenOmciEvent.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='omci.AlarmOpenOmciEvent.data', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=848,
  serialized_end=944,
)

_ALARMINSTANCEDATA.fields_by_name['attributes'].message_type = _ALARMATTRIBUTEDATA
_ALARMCLASSDATA.fields_by_name['instances'].message_type = _ALARMINSTANCEDATA
_ALARMDEVICEDATA.fields_by_name['classes'].message_type = _ALARMCLASSDATA
_ALARMDEVICEDATA.fields_by_name['managed_entities'].message_type = _ALARMMANAGEDENTITY
_ALARMDEVICEDATA.fields_by_name['message_types'].message_type = _ALARMMESSAGETYPE
_ALARMOPENOMCIEVENTTYPE_OPENOMCIEVENTTYPE.containing_type = _ALARMOPENOMCIEVENTTYPE
_ALARMOPENOMCIEVENT.fields_by_name['type'].enum_type = _ALARMOPENOMCIEVENTTYPE_OPENOMCIEVENTTYPE
DESCRIPTOR.message_types_by_name['AlarmAttributeData'] = _ALARMATTRIBUTEDATA
DESCRIPTOR.message_types_by_name['AlarmInstanceData'] = _ALARMINSTANCEDATA
DESCRIPTOR.message_types_by_name['AlarmClassData'] = _ALARMCLASSDATA
DESCRIPTOR.message_types_by_name['AlarmManagedEntity'] = _ALARMMANAGEDENTITY
DESCRIPTOR.message_types_by_name['AlarmMessageType'] = _ALARMMESSAGETYPE
DESCRIPTOR.message_types_by_name['AlarmDeviceData'] = _ALARMDEVICEDATA
DESCRIPTOR.message_types_by_name['AlarmOpenOmciEventType'] = _ALARMOPENOMCIEVENTTYPE
DESCRIPTOR.message_types_by_name['AlarmOpenOmciEvent'] = _ALARMOPENOMCIEVENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AlarmAttributeData = _reflection.GeneratedProtocolMessageType('AlarmAttributeData', (_message.Message,), {
  'DESCRIPTOR' : _ALARMATTRIBUTEDATA,
  '__module__' : 'voltha_protos.omci_alarm_db_pb2'
  # @@protoc_insertion_point(class_scope:omci.AlarmAttributeData)
  })
_sym_db.RegisterMessage(AlarmAttributeData)

AlarmInstanceData = _reflection.GeneratedProtocolMessageType('AlarmInstanceData', (_message.Message,), {
  'DESCRIPTOR' : _ALARMINSTANCEDATA,
  '__module__' : 'voltha_protos.omci_alarm_db_pb2'
  # @@protoc_insertion_point(class_scope:omci.AlarmInstanceData)
  })
_sym_db.RegisterMessage(AlarmInstanceData)

AlarmClassData = _reflection.GeneratedProtocolMessageType('AlarmClassData', (_message.Message,), {
  'DESCRIPTOR' : _ALARMCLASSDATA,
  '__module__' : 'voltha_protos.omci_alarm_db_pb2'
  # @@protoc_insertion_point(class_scope:omci.AlarmClassData)
  })
_sym_db.RegisterMessage(AlarmClassData)

AlarmManagedEntity = _reflection.GeneratedProtocolMessageType('AlarmManagedEntity', (_message.Message,), {
  'DESCRIPTOR' : _ALARMMANAGEDENTITY,
  '__module__' : 'voltha_protos.omci_alarm_db_pb2'
  # @@protoc_insertion_point(class_scope:omci.AlarmManagedEntity)
  })
_sym_db.RegisterMessage(AlarmManagedEntity)

AlarmMessageType = _reflection.GeneratedProtocolMessageType('AlarmMessageType', (_message.Message,), {
  'DESCRIPTOR' : _ALARMMESSAGETYPE,
  '__module__' : 'voltha_protos.omci_alarm_db_pb2'
  # @@protoc_insertion_point(class_scope:omci.AlarmMessageType)
  })
_sym_db.RegisterMessage(AlarmMessageType)

AlarmDeviceData = _reflection.GeneratedProtocolMessageType('AlarmDeviceData', (_message.Message,), {
  'DESCRIPTOR' : _ALARMDEVICEDATA,
  '__module__' : 'voltha_protos.omci_alarm_db_pb2'
  # @@protoc_insertion_point(class_scope:omci.AlarmDeviceData)
  })
_sym_db.RegisterMessage(AlarmDeviceData)

AlarmOpenOmciEventType = _reflection.GeneratedProtocolMessageType('AlarmOpenOmciEventType', (_message.Message,), {
  'DESCRIPTOR' : _ALARMOPENOMCIEVENTTYPE,
  '__module__' : 'voltha_protos.omci_alarm_db_pb2'
  # @@protoc_insertion_point(class_scope:omci.AlarmOpenOmciEventType)
  })
_sym_db.RegisterMessage(AlarmOpenOmciEventType)

AlarmOpenOmciEvent = _reflection.GeneratedProtocolMessageType('AlarmOpenOmciEvent', (_message.Message,), {
  'DESCRIPTOR' : _ALARMOPENOMCIEVENT,
  '__module__' : 'voltha_protos.omci_alarm_db_pb2'
  # @@protoc_insertion_point(class_scope:omci.AlarmOpenOmciEvent)
  })
_sym_db.RegisterMessage(AlarmOpenOmciEvent)


DESCRIPTOR._options = None
_ALARMATTRIBUTEDATA.fields_by_name['name']._options = None
_ALARMINSTANCEDATA.fields_by_name['instance_id']._options = None
_ALARMINSTANCEDATA.fields_by_name['attributes']._options = None
_ALARMCLASSDATA.fields_by_name['class_id']._options = None
_ALARMCLASSDATA.fields_by_name['instances']._options = None
_ALARMMANAGEDENTITY.fields_by_name['class_id']._options = None
_ALARMMANAGEDENTITY.fields_by_name['name']._options = None
_ALARMMESSAGETYPE.fields_by_name['message_type']._options = None
_ALARMDEVICEDATA.fields_by_name['device_id']._options = None
_ALARMDEVICEDATA.fields_by_name['classes']._options = None
# @@protoc_insertion_point(module_scope)
