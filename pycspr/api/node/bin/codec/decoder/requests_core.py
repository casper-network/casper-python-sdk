import typing

from pycspr.api.node.bin.codec.decoder.domain import \
    decode_protocol_version
from pycspr.api.node.bin.codec.primitives import \
    decode_u8, \
    decode_u16, \
    encode_u8
from pycspr.api.node.bin.types.core import \
    Endpoint, \
    Request, \
    RequestHeader
from pycspr.api.node.bin.codec.constants import \
    TAG_ENDPOINT, \
    TAGS_TO_ENDPOINTS, \
    TAG_GET, \
    TAG_GET_INFORMATION, \
    TAG_GET_RECORD, \
    TAG_GET_STATE, \
    TAG_TRY_ACCEPT_TRANSACTION, \
    TAG_TRY_SPECULATIVE_TRANSACTION


def decode_request(bstream: bytes) -> typing.Tuple[bytes, Request]:
    bstream, binary_request_version = decode_u16(bstream)
    bstream, chain_protocol_version = decode_protocol_version(bstream)
    bstream, header_type_tag = decode_u8(bstream)
    bstream, request_id = decode_u16(bstream)

    # Endpoint can be identified from header type plus leading bits of payload stream.
    bstream, endpoint = _decode_endpoint(bstream, header_type_tag)
    bstream, payload = _decode_request_payload(bstream, endpoint)

    return b'', Request(
        endpoint=endpoint,
        header=RequestHeader(
            binary_request_version=binary_request_version,
            chain_protocol_version=chain_protocol_version,
            id=request_id
        ),
        payload=payload,
    )


def _decode_request_payload(bstream: bytes, endpoint: Endpoint) -> typing.Tuple[bytes, object]:
    # TODO map endpoint to domain type.
    # TODO invoke decoder
    print(107, bstream)
    return bstream, bstream


def _decode_endpoint(bstream: bytes, header_tag: int) -> typing.Tuple[bytes, Endpoint]:
    if header_tag == TAG_TRY_ACCEPT_TRANSACTION:
        return bstream, Endpoint.Try_AcceptTransaction
    elif header_tag == TAG_TRY_SPECULATIVE_TRANSACTION:
        return bstream, Endpoint.Try_AcceptTransaction
    elif header_tag == TAG_GET:
        bstream, query_type = decode_u8(bstream)
        bstream, query_subtype = decode_u8(bstream)
        try:
            endpoint = TAGS_TO_ENDPOINTS[(header_tag, query_type, query_subtype)]
        except KeyError:
            raise ValueError("Invalid query endpoint encoding")
        else:
            return bstream, endpoint
    else:
        raise ValueError("Invalid endpoint header tag")


DECODERS: typing.Dict[typing.Type, typing.Callable] = {
    Request: decode_request,
}
