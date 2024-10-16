import typing

from pycspr.api.node.bin.type_defs import Endpoint

# Codec tags: chain.
TAG_ACTIVATION_POINT_ERA: int = 0
TAG_ACTIVATION_POINT_GENESIS: int = 1
TAG_BLOCK_HASH: int = 0
TAG_BLOCK_HEIGHT: int = 1
TAG_BLOCK_TYPE_V1: int = 0
TAG_BLOCK_TYPE_V2: int = 1

# Codec tags: transport.
TAG_GET: int = 0
TAG_GET_INFORMATION: int = 1
TAG_GET_INFORMATION_AVAILABLE_BLOCK_RANGE: int = 10
TAG_GET_INFORMATION_BLOCK_HEADER: int = 0
TAG_GET_INFORMATION_BLOCK_SYNCHRONIZER_STATUS: int = 9
TAG_GET_INFORMATION_CHAINSPEC_RAW_BYTES: int = 13
TAG_GET_INFORMATION_CONSENSUS_STATUS: int = 12
TAG_GET_INFORMATION_CONSENSUS_VALIDATOR_CHANGES: int = 8
TAG_GET_INFORMATION_LAST_PROGRESS: int = 5
TAG_GET_INFORMATION_LATEST_SWITCH_BLOCK_HEADER: int = 15
TAG_GET_INFORMATION_NETWORK_NAME: int = 7
TAG_GET_INFORMATION_NEXT_UPGRADE: int = 11
TAG_GET_INFORMATION_NODE_STATUS: int = 14
TAG_GET_INFORMATION_PEERS: int = 3
TAG_GET_INFORMATION_REACTOR_STATE: int = 6
TAG_GET_INFORMATION_REWARD: int = 16
TAG_GET_INFORMATION_SIGNED_BLOCK: int = 1
TAG_GET_INFORMATION_TRANSACTION: int = 2
TAG_GET_INFORMATION_UPTIME: int = 4
TAG_GET_RECORD: int = 0
TAG_GET_STATE: int = 2
TAG_OPTIONAL_NONE: int = 0
TAG_OPTIONAL_VALUE: int = 1
TAG_TRY_ACCEPT_TRANSACTION: int = 1
TAG_TRY_SPECULATIVE_TRANSACTION: int = 2

# Codec tags: transport.
# Map of endpoint to a tuple of type tags.  This permits simplified encoding.
ENDPOINT_TO_TAGS: typing.Dict[
    Endpoint,
    typing.Tuple[int, typing.Optional[int], typing.Optional[int]]
] = {
    Endpoint.Get_Information_AvailableBlockRange:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_AVAILABLE_BLOCK_RANGE),
    Endpoint.Get_Information_BlockHeader:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_BLOCK_HEADER),
    Endpoint.Get_Information_BlockSynchronizerStatus:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_BLOCK_SYNCHRONIZER_STATUS),
    Endpoint.Get_Information_ChainspecRawBytes:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_CHAINSPEC_RAW_BYTES),
    Endpoint.Get_Information_ConsensusStatus:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_CONSENSUS_STATUS),
    Endpoint.Get_Information_ConsensusValidatorChanges:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_CONSENSUS_VALIDATOR_CHANGES),
    Endpoint.Get_Information_LastProgress:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_LAST_PROGRESS),
    Endpoint.Get_Information_LatestSwitchBlockHeader:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_LATEST_SWITCH_BLOCK_HEADER),
    Endpoint.Get_Information_NetworkName:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_NETWORK_NAME),
    Endpoint.Get_Information_NextUpgrade:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_NEXT_UPGRADE),
    Endpoint.Get_Information_NodeStatus:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_NODE_STATUS),
    Endpoint.Get_Information_Peers:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_PEERS),
    Endpoint.Get_Information_ReactorState:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_REACTOR_STATE),
    Endpoint.Get_Information_Reward:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_REWARD),
    Endpoint.Get_Information_SignedBlock:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_SIGNED_BLOCK),
    Endpoint.Get_Information_Transaction:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_TRANSACTION),
    Endpoint.Get_Information_Uptime:
        (TAG_GET, TAG_GET_INFORMATION, TAG_GET_INFORMATION_UPTIME),
    Endpoint.Try_AcceptTransaction:
        (TAG_TRY_ACCEPT_TRANSACTION, None, None),
    Endpoint.Try_SpeculativeExec:
        (TAG_TRY_SPECULATIVE_TRANSACTION, None, None),
}

# Codec tags: transport.
# Map of endpoint to a tuple of type tag as bytes.  This permits simplified decoding.
TAGS_TO_ENDPOINTS: typing.Dict[
    typing.Tuple[int, typing.Optional[int], typing.Optional[int]],
    Endpoint
] = {
    v: k for k, v in ENDPOINT_TO_TAGS.items()
}
