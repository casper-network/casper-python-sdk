import typing

from pycspr.api.node.bin.codec.constants import \
    TAG_GET, \
    TAG_TRY_ACCEPT_TRANSACTION, \
    TAG_TRY_SPECULATIVE_TRANSACTION, \
    TAGS_TO_ENDPOINTS
from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.type_defs.chain import ProtocolVersion
from pycspr.type_defs.primitives import U8, U16
from pycspr.api.node.bin.type_defs import \
    Endpoint, \
    ErrorCode, \
    Request, \
    RequestHeader, \
    Response, \
    ResponseHeader, \
    ResponseAndRequest, \
    RESPONSE_PAYLOAD_TYPE_INFO


def _decode_request(bytes_in: bytes) -> typing.Tuple[bytes, Request]:
    def _decode_endpoint(bytes_in: bytes, request_tag: int) -> typing.Tuple[bytes, Endpoint]:
        if request_tag == TAG_TRY_ACCEPT_TRANSACTION:
            return bytes_in, Endpoint.Try_AcceptTransaction
        elif request_tag == TAG_TRY_SPECULATIVE_TRANSACTION:
            return bytes_in, Endpoint.Try_SpeculativeExec
        elif request_tag == TAG_GET:
            rem, get_type = decode(U8, bytes_in)
            rem, get_type_inner = decode(U8, rem)
            return rem, TAGS_TO_ENDPOINTS[(request_tag, get_type, get_type_inner)]
        else:
            raise ValueError(f"Invalid request header tag: {request_tag}")

    def _decode_header(bytes_in: bytes) -> typing.Tuple[bytes, RequestHeader]:
        rem, request_version = decode(U16, bytes_in)
        rem, protocol_version = decode(ProtocolVersion, rem)
        rem, request_tag = decode(U8, rem)
        rem, request_id = decode(U16, rem)
        rem, endpoint = _decode_endpoint(rem, request_tag)

        return rem, RequestHeader(request_version, protocol_version, endpoint, request_id)

    def _decode_payload(bytes_in: bytes, header: RequestHeader) -> typing.Tuple[bytes, object]:
        # TODO invoke request payload decoder
        return b'', bytes_in

    rem, header = _decode_header(bytes_in)
    rem, payload = _decode_payload(rem, header)

    return rem, Request(header, payload)


def _decode_response(bytes_in: bytes) -> typing.Tuple[bytes, Response]:
    rem, protocol_version = decode(ProtocolVersion, bytes_in)
    rem, error_code = decode(U16, rem)
    rem, returned_data_type_tag = decode(U8, rem, True)
    rem, payload_bytes = decode(bytes, rem)

    return rem,  Response(
        header=ResponseHeader(
            protocol_version=protocol_version,
            error_code=ErrorCode(error_code),
            returned_data_type_tag=returned_data_type_tag
        ),
        payload_bytes=payload_bytes
    )


def _decode_response_and_request(bytes_in: bytes) -> ResponseAndRequest:
    def _decode_original_request_context(bytes_in: bytes) -> typing.Tuple[bytes, typing.Tuple[int, Request]]:
        rem, request_id = decode(U16, bytes_in)
        rem, bytes_req = decode(bytes, rem)
        rem_bytes_req, request = decode(Request, bytes_req)

        assert len(rem_bytes_req) == 0
        assert request.header.id == request_id

        return rem, (request_id, request)

    def _decode_response_payload(request: Request, response: Response) -> typing.Union[object, typing.List[object]]:
        try:
            typedef, is_sequence = RESPONSE_PAYLOAD_TYPE_INFO[request.header.endpoint]
        except KeyError:
            raise ValueError(f"Invalid endpoint response payload type ({request.header.endpoint})")

        if len(response.payload_bytes) == 0:
            return [] if is_sequence is True else None

        rem, entity = decode(typedef, response.payload_bytes, is_sequence=is_sequence)
        assert len(rem) == 0, "Unconsumed response payload bytes"
        return entity

    # Strip size.
    rem, bytes_inner = decode(bytes, bytes_in)
    assert len(rem) == 0

    # Inner request.
    rem, (_, request) = _decode_original_request_context(bytes_inner)

    # Inner response.
    rem, response = decode(Response, rem)
    assert len(rem) == 0

    # Inner response payload.
    response.payload = _decode_response_payload(request, response)

    return bytes([]), ResponseAndRequest(request, response)


def _decode_response_payload(
    endpoint: Endpoint,
    bytes_in: bytes
) -> typing.Union[object, typing.List[object]]:
    """Returns a decoded response payload.

    """
    # Set response payload metadata.
    try:
        typedef, is_sequence = RESPONSE_PAYLOAD_TYPE_INFO[endpoint]
    except KeyError:
        raise ValueError(f"Undefined endpoint response payload type ({endpoint})")

    if len(bytes_in) == 0:
        return [] if is_sequence is True else None
    else:
        rem, entity = decode(typedef, bytes_in, is_sequence=is_sequence)
        assert len(rem) == 0, "Unconsumed response payload bytes"
        return  entity


register_decoders({
    (Request, _decode_request),
    (Response, _decode_response),
    (ResponseAndRequest, _decode_response_and_request),
})
