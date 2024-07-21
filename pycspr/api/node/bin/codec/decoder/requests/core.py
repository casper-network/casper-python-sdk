import typing

from pycspr.api.node.bin.codec.decoder.domain import \
    decode_protocol_version
from pycspr.api.node.bin.codec.decoder.primitives import \
    decode_u8, \
    decode_u16
from pycspr.api.node.bin.types.requests.core import \
    Request, \
    RequestHeader, \
    Endpoint


def decode_request(bstream: bytes) -> typing.Tuple[bytes, Request]:
    bstream, header = decode_request_header(bstream)
    bstream, body = decode_request_body(bstream)

    return b'', Request(body, header)


def decode_request_body(bstream: bytes) -> typing.Tuple[bytes, object]:
    # TODO
    return bstream, bstream


def decode_request_header(bstream: bytes) -> typing.Tuple[bytes, RequestHeader]:
    bstream, binary_request_version = decode_u16(bstream)
    bstream, chain_protocol_version = decode_protocol_version(bstream)
    bstream, request_type_raw = decode_u8(bstream)
    bstream, request_id = decode_u16(bstream)

    return bstream, RequestHeader(
        binary_request_version=binary_request_version,
        chain_protocol_version=chain_protocol_version,
        type_tag=Endpoint(request_type_raw),
        id=request_id
    )


DECODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: decode_request,
    RequestHeader: decode_request_header
}
