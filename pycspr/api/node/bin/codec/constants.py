import typing

from pycspr.api.node.bin.types.core import Endpoint


TYPE_TAG_ENDPOINT: typing.Dict[Endpoint, int] = {
    Endpoint.Get_Information_AvailableBlockRange: 10,
    Endpoint.Get_Information_BlockHeader: 0,
    Endpoint.Get_Information_BlockSynchronizerStatus: 9,
    Endpoint.Get_Information_ChainspecRawBytes: 13,
    Endpoint.Get_Information_ConsensusStatus: 12,
    Endpoint.Get_Information_ConsensusValidatorChanges: 8,
    Endpoint.Get_Information_LastProgress: 5,
    Endpoint.Get_Information_LatestSwitchBlockHeader: 15,
    Endpoint.Get_Information_NetworkName: 7,
    Endpoint.Get_Information_NextUpgrade: 11,
    Endpoint.Get_Information_NodeStatus: 14,
    Endpoint.Get_Information_Peers: 3,
    Endpoint.Get_Information_ReactorState: 6,
    Endpoint.Get_Information_Reward: 16,
    Endpoint.Get_Information_SignedBlock: 1,
    Endpoint.Get_Information_Transaction: 2,
    Endpoint.Get_Information_Uptime: 4,
    Endpoint.Try_AcceptTransaction: 1,
    Endpoint.Try_SpeculativeExec: 2,
}

TYPE_TAG_DOMAIN_BLOCK_HASH: int = 0
TYPE_TAG_DOMAIN_BLOCK_HEIGHT: int = 1
TYPE_TAG_OPTIONAL_NONE: int = 0
TYPE_TAG_OPTIONAL_VALUE: int = 1
TYPE_TAG_REQUEST_GET: int = 0
TYPE_TAG_REQUEST_GET_INFORMATION: int = 0
TYPE_TAG_REQUEST_GET_RECORD: int = 0
TYPE_TAG_REQUEST_GET_STATE: int = 0
TYPE_TAG_REQUEST_TRY_ACCEPT_TRANSACTION: int = 1
TYPE_TAG_REQUEST_TRY_SPECULATIVE_TRANSACTION: int = 2
