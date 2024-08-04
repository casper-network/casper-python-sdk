import random
import typing

from pycspr.api.node.bin.types import \
    ConnectionInfo, \
    Endpoint, \
    Request, \
    RequestHeader, \
    RequestID
from pycspr.api.node.bin.types.domain import \
    ProtocolVersion


def get_request(
    endpoint: Endpoint,
    connection_info: ConnectionInfo,
    request_id: typing.Optional[RequestID] = None
) -> Request:
    """Returns a remote binary server request header.

    """
    def get_header() -> RequestHeader:
        return RequestHeader(
            binary_request_version=connection_info.binary_request_version,
            chain_protocol_version= \
                ProtocolVersion.from_semvar(connection_info.chain_protocol_version),
            id=(request_id or random.randint(0, int(1e4))),
        )


    return Request(
        endpoint=endpoint,
        header=get_header()
    )
