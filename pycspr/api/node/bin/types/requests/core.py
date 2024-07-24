from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.api.node.bin.types.domain import ProtocolVersion


@dataclasses.dataclass
class Request():
    """Encapsulates information required to dispatch an API request.

    """
    # Request endpoint.
    endpoint: Endpoint

    # Request header encapsulating API metadata.
    header: "RequestHeader"

    # Request payload, i.e. endpoint params.
    payload: object = None


@dataclasses.dataclass
class RequestHeader():
    """Encapsulates API request header information.

    """
    # Version of binary server API.
    binary_request_version: int

    # Version of chain protocol.
    chain_protocol_version: ProtocolVersion

    # Request correlation identifier.
    id: "RequestID"


RequestID = typing.NewType(
    "Request identifier specified by end user typically used to correlate responses.", int
)
