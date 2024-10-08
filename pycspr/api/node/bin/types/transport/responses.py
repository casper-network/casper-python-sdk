import typing

from pycspr.api.node.bin.types.chain import \
    AvailableBlockRange, \
    BlockID, \
    BlockHeader, \
    BlockSynchronizerStatus, \
    ChainspecRawBytes, \
    ConsensusStatus, \
    EraID, \
    NextUpgrade
from pycspr.api.node.bin.types.node import \
    NodeLastProgress, \
    NodePeerEntry, \
    NodeUptime
from pycspr.api.node.bin.types.transport.core import Endpoint


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
    Endpoint.Get_Information_Reward: (bytes, False),
    Endpoint.Get_Information_Uptime: (NodeUptime, False),
}
