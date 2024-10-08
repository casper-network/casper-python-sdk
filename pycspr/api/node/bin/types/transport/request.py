from __future__ import annotations

import dataclasses
import typing

from pycspr.api.node.bin.types.chain import ProtocolVersion


@dataclasses.dataclass
class Request():
    """Encapsulates information required to dispatch an API request.

    """
    # Request header encapsulating API metadata.
    header: RequestHeader

    # Request payload, i.e. endpoint params.
    payload: bytes = bytes([])

    def __eq__(self, other: Request) -> bool:
        return self.header == other.header and self.payload == self.payload

    def __str__(self) -> str:
        return f"Request: {self.header} :: Payload Length={len(self.payload)}"


@dataclasses.dataclass
class RequestHeader():
    """Encapsulates API request header information.

    """
    # Version of binary server API.
    binary_request_version: int

    # Version of chain protocol.
    chain_protocol_version: ProtocolVersion

    # Request endpoint.
    endpoint: Endpoint

    # Request correlation identifier.
    id: int

    def __eq__(self, other: RequestHeader) -> bool:
        return \
            self.binary_request_version == other.binary_request_version and \
            self.chain_protocol_version == self.chain_protocol_version and \
            self.endpoint == other.endpoint and \
            self.id == other.id

    def __str__(self) -> str:
        return f"EndPoint={self.endpoint.name} | ID={self.id}"


RequestID = typing.NewType(
    "Request identifier specified by end user typically used to correlate responses.", int
)
