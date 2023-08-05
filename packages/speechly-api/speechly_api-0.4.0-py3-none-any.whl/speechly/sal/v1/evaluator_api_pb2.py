# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: speechly/sal/v1/evaluator_api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='speechly/sal/v1/evaluator_api.proto',
  package='speechly.sal.v1',
  syntax='proto3',
  serialized_options=b'\n\023com.speechly.sal.v1B\021EvaluatorApiProtoP\001Z\025speechly/sal/v1;salv1\242\002\003SSX\252\002\017Speechly.Sal.V1\312\002\017Speechly\\Sal\\V1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n#speechly/sal/v1/evaluator_api.proto\x12\x0fspeechly.sal.v1\"D\n\x0cTextsRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x15\n\rlanguage_code\x18\x02 \x01(\t\x12\r\n\x05texts\x18\x03 \x03(\t\"(\n\rTextsResponse\x12\x17\n\x0f\x61nnotated_texts\x18\x02 \x03(\t\"\xb5\x01\n\x10\x45valTextsRequest\x12\x0e\n\x06\x61pp_id\x18\x01 \x01(\t\x12\x15\n\rlanguage_code\x18\x02 \x01(\t\x12?\n\x05pairs\x18\x03 \x03(\x0b\x32\x30.speechly.sal.v1.EvalTextsRequest.EvaluationPair\x1a\x39\n\x0e\x45valuationPair\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x19\n\x11ground_truth_text\x18\x02 \x01(\t\"#\n\x11\x45valTextsResponse\x12\x0e\n\x06report\x18\x01 \x01(\t2\xaa\x01\n\x0c\x45valuatorAPI\x12\x46\n\x05Texts\x12\x1d.speechly.sal.v1.TextsRequest\x1a\x1e.speechly.sal.v1.TextsResponse\x12R\n\tEvalTexts\x12!.speechly.sal.v1.EvalTextsRequest\x1a\".speechly.sal.v1.EvalTextsResponseBk\n\x13\x63om.speechly.sal.v1B\x11\x45valuatorApiProtoP\x01Z\x15speechly/sal/v1;salv1\xa2\x02\x03SSX\xaa\x02\x0fSpeechly.Sal.V1\xca\x02\x0fSpeechly\\Sal\\V1b\x06proto3'
)




_TEXTSREQUEST = _descriptor.Descriptor(
  name='TextsRequest',
  full_name='speechly.sal.v1.TextsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='speechly.sal.v1.TextsRequest.app_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='language_code', full_name='speechly.sal.v1.TextsRequest.language_code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='texts', full_name='speechly.sal.v1.TextsRequest.texts', index=2,
      number=3, type=9, cpp_type=9, label=3,
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
  serialized_start=56,
  serialized_end=124,
)


_TEXTSRESPONSE = _descriptor.Descriptor(
  name='TextsResponse',
  full_name='speechly.sal.v1.TextsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='annotated_texts', full_name='speechly.sal.v1.TextsResponse.annotated_texts', index=0,
      number=2, type=9, cpp_type=9, label=3,
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
  serialized_start=126,
  serialized_end=166,
)


_EVALTEXTSREQUEST_EVALUATIONPAIR = _descriptor.Descriptor(
  name='EvaluationPair',
  full_name='speechly.sal.v1.EvalTextsRequest.EvaluationPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='speechly.sal.v1.EvalTextsRequest.EvaluationPair.text', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ground_truth_text', full_name='speechly.sal.v1.EvalTextsRequest.EvaluationPair.ground_truth_text', index=1,
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
  serialized_start=293,
  serialized_end=350,
)

_EVALTEXTSREQUEST = _descriptor.Descriptor(
  name='EvalTextsRequest',
  full_name='speechly.sal.v1.EvalTextsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='app_id', full_name='speechly.sal.v1.EvalTextsRequest.app_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='language_code', full_name='speechly.sal.v1.EvalTextsRequest.language_code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pairs', full_name='speechly.sal.v1.EvalTextsRequest.pairs', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_EVALTEXTSREQUEST_EVALUATIONPAIR, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=169,
  serialized_end=350,
)


_EVALTEXTSRESPONSE = _descriptor.Descriptor(
  name='EvalTextsResponse',
  full_name='speechly.sal.v1.EvalTextsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='report', full_name='speechly.sal.v1.EvalTextsResponse.report', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=352,
  serialized_end=387,
)

_EVALTEXTSREQUEST_EVALUATIONPAIR.containing_type = _EVALTEXTSREQUEST
_EVALTEXTSREQUEST.fields_by_name['pairs'].message_type = _EVALTEXTSREQUEST_EVALUATIONPAIR
DESCRIPTOR.message_types_by_name['TextsRequest'] = _TEXTSREQUEST
DESCRIPTOR.message_types_by_name['TextsResponse'] = _TEXTSRESPONSE
DESCRIPTOR.message_types_by_name['EvalTextsRequest'] = _EVALTEXTSREQUEST
DESCRIPTOR.message_types_by_name['EvalTextsResponse'] = _EVALTEXTSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TextsRequest = _reflection.GeneratedProtocolMessageType('TextsRequest', (_message.Message,), {
  'DESCRIPTOR' : _TEXTSREQUEST,
  '__module__' : 'speechly.sal.v1.evaluator_api_pb2'
  # @@protoc_insertion_point(class_scope:speechly.sal.v1.TextsRequest)
  })
_sym_db.RegisterMessage(TextsRequest)

TextsResponse = _reflection.GeneratedProtocolMessageType('TextsResponse', (_message.Message,), {
  'DESCRIPTOR' : _TEXTSRESPONSE,
  '__module__' : 'speechly.sal.v1.evaluator_api_pb2'
  # @@protoc_insertion_point(class_scope:speechly.sal.v1.TextsResponse)
  })
_sym_db.RegisterMessage(TextsResponse)

EvalTextsRequest = _reflection.GeneratedProtocolMessageType('EvalTextsRequest', (_message.Message,), {

  'EvaluationPair' : _reflection.GeneratedProtocolMessageType('EvaluationPair', (_message.Message,), {
    'DESCRIPTOR' : _EVALTEXTSREQUEST_EVALUATIONPAIR,
    '__module__' : 'speechly.sal.v1.evaluator_api_pb2'
    # @@protoc_insertion_point(class_scope:speechly.sal.v1.EvalTextsRequest.EvaluationPair)
    })
  ,
  'DESCRIPTOR' : _EVALTEXTSREQUEST,
  '__module__' : 'speechly.sal.v1.evaluator_api_pb2'
  # @@protoc_insertion_point(class_scope:speechly.sal.v1.EvalTextsRequest)
  })
_sym_db.RegisterMessage(EvalTextsRequest)
_sym_db.RegisterMessage(EvalTextsRequest.EvaluationPair)

EvalTextsResponse = _reflection.GeneratedProtocolMessageType('EvalTextsResponse', (_message.Message,), {
  'DESCRIPTOR' : _EVALTEXTSRESPONSE,
  '__module__' : 'speechly.sal.v1.evaluator_api_pb2'
  # @@protoc_insertion_point(class_scope:speechly.sal.v1.EvalTextsResponse)
  })
_sym_db.RegisterMessage(EvalTextsResponse)


DESCRIPTOR._options = None

_EVALUATORAPI = _descriptor.ServiceDescriptor(
  name='EvaluatorAPI',
  full_name='speechly.sal.v1.EvaluatorAPI',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=390,
  serialized_end=560,
  methods=[
  _descriptor.MethodDescriptor(
    name='Texts',
    full_name='speechly.sal.v1.EvaluatorAPI.Texts',
    index=0,
    containing_service=None,
    input_type=_TEXTSREQUEST,
    output_type=_TEXTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='EvalTexts',
    full_name='speechly.sal.v1.EvaluatorAPI.EvalTexts',
    index=1,
    containing_service=None,
    input_type=_EVALTEXTSREQUEST,
    output_type=_EVALTEXTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_EVALUATORAPI)

DESCRIPTOR.services_by_name['EvaluatorAPI'] = _EVALUATORAPI

# @@protoc_insertion_point(module_scope)
