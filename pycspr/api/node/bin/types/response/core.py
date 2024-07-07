from __future__ import annotations

import dataclasses
import typing

from pycspr.api.node.bin.types.domain import ProtocolVersion


@dataclasses.dataclass
class Response():
    # Response header.
    header: "ResponseHeader"

    # Response inner payload.
    payload: bytes


@dataclasses.dataclass
class ResponseHeader():
    # Chain protocol version.
    protocol_version: ProtocolVersion

    # Server error code.
    error: int

    # Server data type.
    returned_data_type_tag: typing.Optional[int]
