import typing

from pycspr.api.node.bin.types.core import \
    Endpoint
from pycspr.api.node.bin.types.requests import \
    Request
from pycspr.api.node.bin.codec.constants import \
    TYPE_TAG_REQUEST_GET, \
    TYPE_TAG_REQUEST_GET_INFORMATION, \
    TYPE_TAG_REQUEST_GET_RECORD, \
    TYPE_TAG_REQUEST_GET_STATE, \
    TYPE_TAG_REQUEST_TRY_ACCEPT_TRANSACTION, \
    TYPE_TAG_REQUEST_TRY_SPECULATIVE_TRANSACTION
from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_u8, \
    encode_u16
from pycspr.api.node.bin.codec.encoder.domain import \
    encode_protocol_version


def encode_request(entity: Request) -> bytes:
    def encode_header() -> bytes:
        def encode_endpoint() -> bytes:
            if entity.endpoint.name.startswith("Get_"):
                return encode_u8(TYPE_TAG_REQUEST_GET)
            elif entity.endpoint == Endpoint.Try_AcceptTransaction:
                return encode_u8(TYPE_TAG_REQUEST_TRY_ACCEPT_TRANSACTION)
            elif entity.endpoint == Endpoint.Try_SpeculativeExec:
                return encode_u8(TYPE_TAG_REQUEST_TRY_SPECULATIVE_TRANSACTION)
            else:
                raise ValueError("Invalid request type")

        return \
            encode_u16(entity.header.binary_request_version) + \
            encode_protocol_version(entity.header.chain_protocol_version) + \
            encode_endpoint() + \
            encode_u16(entity.header.id)

    def encode_payload() -> bytes:
        if entity.payload is None:
            return b''

        print("TODO: _encode_request_payload")
        return b''

    def encode_payload_tag() -> bytes:
        if entity.endpoint.name.startswith("Get_"):
            if entity.endpoint.name.startswith("Get_Information"):
                return encode_u8(TYPE_TAG_REQUEST_GET_INFORMATION) + encode_u8(entity.endpoint.value)
            elif entity.endpoint.name.startswith("Get_Record"):
                return encode_u8(TYPE_TAG_REQUEST_GET_RECORD) + encode_u8(entity.endpoint.value)
            elif entity.endpoint.name.startswith("Get_State"):
                return encode_u8(TYPE_TAG_REQUEST_GET_STATE) + encode_u8(entity.endpoint.value)
            else:
                raise ValueError("Invalid endpoint")
        else:
            return b''

    return encode_header() + encode_payload_tag() + encode_payload()


ENCODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: encode_request,
}
