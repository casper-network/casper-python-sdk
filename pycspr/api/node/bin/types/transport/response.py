from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.api.node.bin.types.chain import \
    AvailableBlockRange, \
    BlockID, \
    BlockHeader, \
    BlockSynchronizerStatus, \
    ChainspecRawBytes, \
    ConsensusReward, \
    ConsensusStatus, \
    EraID, \
    NextUpgrade, \
    ProtocolVersion
from pycspr.api.node.bin.types.node import \
    NodeLastProgress, \
    NodePeerEntry, \
    NodeUptime
from pycspr.api.node.bin.types.transport.core import Endpoint, ErrorCode
from pycspr.api.node.bin.types.transport.request import Request


@dataclasses.dataclass
class Response():
    """Response wrapper over raw bytes returned from server.

    """
    # Inner payload bytes.
    bytes_payload: bytes

    # Raw bytes.
    bytes_raw: bytes

    # Decoded header.
    header: ResponseHeader

    # Original request.
    request: Request

    # Inner payload.
    payload: typing.Union[object, typing.List[object]] = None

    def __str__(self) -> str:
        return f"Response: {self.header}"


@dataclasses.dataclass
class ResponseHeader():
    """Decoded response header.

    """
    # Chain protocol version.
    protocol_version: ProtocolVersion

    # Server error code.
    error_code: ErrorCode

    # Server data type.
    returned_data_type_tag: typing.Optional[int]

    def __str__(self) -> str:
        return "{} | Err={} | Data Type={}".format(
            self.protocol_version,
            self.error_code,
            self.returned_data_type_tag
        )

# Map: Endpoint <-> (type, is_sequence)
RESPONSE_PAYLOAD_TYPE_INFO: typing.Dict[Endpoint, typing.Tuple[type, bool]] = {
    Endpoint.Get_Information_AvailableBlockRange: (AvailableBlockRange, False),
    Endpoint.Get_Information_BlockHeader: (BlockHeader, False),
    Endpoint.Get_Information_BlockSynchronizerStatus: (BlockSynchronizerStatus, False),
    Endpoint.Get_Information_ChainspecRawBytes: (ChainspecRawBytes, False),
    Endpoint.Get_Information_ConsensusStatus: (ConsensusStatus, False),
    Endpoint.Get_Information_LatestSwitchBlockHeader: (BlockHeader, False),
    Endpoint.Get_Information_LastProgress: (NodeLastProgress, False),
    Endpoint.Get_Information_NetworkName: (str, False),
    Endpoint.Get_Information_NextUpgrade: (NextUpgrade, False),
    Endpoint.Get_Information_Peers: (NodePeerEntry, True),
    Endpoint.Get_Information_ReactorState: (str, False),
    Endpoint.Get_Information_Reward: (ConsensusReward, False),
    Endpoint.Get_Information_Uptime: (NodeUptime, False),
}
