import typing

from pycspr.api.node.bin import types
from pycspr.api.node.bin.types.response.core import Response
from pycspr.api.node.bin.types.response.core import ResponseHeader
from pycspr.api.node.bin.types.domain import ProtocolVersion


def decode(bstream: bytes, typedef: type) -> typing.Tuple[bytes, object]:
    try:
        decoder = DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Non-decodeable type: {typedef}")
    else:
        return decoder(bstream)


def decode_entity(bstream: bytes, typedef: type) -> typing.Tuple[bytes, object]:
    try:
        decoder = DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Non-decodeable type: {typedef}")
    else:
        return decoder(bstream)


def decode_u8(bstream: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bstream, 1)


def decode_u16(bstream: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bstream, 2)


def decode_u32(bstream: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bstream, 4)


def decode_u64(bstream: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bstream, 8)


def decode_uint(bstream: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    return \
        bstream[encoded_length:], \
        int.from_bytes(bstream[:encoded_length], "little", signed=False)


def decode_protocol_version(bstream: bytes) -> typing.Tuple[bytes, ProtocolVersion]:

    raise NotImplementedError()


def decode_response(bstream: bytes) -> typing.Tuple[bytes, Response]:
    bstream, header = decode(bstream, ResponseHeader)
    payload: bytes = bstream

    return bstream, Response(header, payload)


def decode_response_header(bstream: bytes) -> typing.Tuple[bytes, ResponseHeader]:
    bstream, protocol_version = decode(bstream, ProtocolVersion)
    bstream, error = decode(bstream, int)
    bstream, returned_data_type_tag = decode_optional(bstream, int)

    return ResponseHeader(
        protocol_version = protocol_version,
        error = error,
        returned_data_type_tag = returned_data_type_tag
    )


DECODERS: typing.Dict[typing.Type, typing.Callable] = {
    Response: decode_response,
    ResponseHeader: decode_response_header,
    ProtocolVersion: decode_protocol_version,
}
