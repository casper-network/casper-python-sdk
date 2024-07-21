import dataclasses
import typing

from pycspr.api.node.bin.types.domain import \
    BlockID, \
    EraID, \
    PublicKey, \
    TransactionHash
from pycspr.api.node.bin.types.requests.core import \
    RequestPayload, \
    Endpoint


@dataclasses.dataclass
class GetAvailableBlockRangeRequest():
    """Request payload: Get.Information.AvailableBlockRange endpoint.

    """
    typeof: Endpoint = Endpoint.Get_Information_AvailableBlockRange


@dataclasses.dataclass
class GetBlockHeaderRequestPayload():
    """Request payload: Get.Information.BlockHeader endpoint.

    """
    block_id: typing.Optional[BlockID]
    typeof: Endpoint = Endpoint.Get_Information_BlockHeader


@dataclasses.dataclass
class GetBlockSynchronizerStatusRequest():
    """Request payload: Get.Information.BlockSynchronizerStatus endpoint.

    """
    typeof: Endpoint = Endpoint.Get_Information_BlockSynchronizerStatus


@dataclasses.dataclass
class GetChainspecRawBytesRequest():
    """Request payload: Get.Information.ChainspecRawBytes endpoint.

    """
    pass


@dataclasses.dataclass
class GetConsensusStatusRequest():
    """Request payload: Get.Information.ConsensusStatus endpoint.

    """
    pass


@dataclasses.dataclass
class GetConsensusValidatorChangesRequest():
    """Request payload: Get.Information.ConsensusValidatorChanges endpoint.

    """
    pass


@dataclasses.dataclass
class GetLastProgressRequest():
    """Request payload: Get.Information.LastProgress endpoint.

    """
    pass


@dataclasses.dataclass
class GetLatestSwitchBlockHeaderRequest():
    """Request payload: Get.Information.LatestSwitchBlockHeader endpoint.

    """
    pass


@dataclasses.dataclass
class GetNetworkNameRequest():
    """Request payload: Get.Information.NetworkName endpoint.

    """
    pass


@dataclasses.dataclass
class GetNextUpgradeRequest():
    """Request payload: Get.Information.NextUpgrade endpoint.

    """
    pass


@dataclasses.dataclass
class GetNodeStatusRequest():
    """Request payload: Get.Information.NodeStatus endpoint.

    """
    pass


@dataclasses.dataclass
class GetPeersRequest():
    """Request payload: Get.Information.Peers endpoint.

    """
    pass


@dataclasses.dataclass
class GetReactorStateRequest():
    """Request payload: Get.Information.ReactorState endpoint.

    """
    pass


@dataclasses.dataclass
class GetRewardRequest():
    """Request payload: Get.Information.Reward endpoint.

    """
    delegator: typing.Optional[PublicKey]
    era_id: typing.Optional[EraID]
    validator: PublicKey


@dataclasses.dataclass
class GetSignedBlockRequest():
    """Request payload: Get.Information.SignedBlock endpoint.

    """
    block_id: typing.Optional[BlockID]


@dataclasses.dataclass
class GetTransactionRequest():
    """Request payload: Get.Information.Transaction endpoint.

    """
    # Hash of the transaction to retrieve.
    hash: TransactionHash

    # Whether to return the deploy with the finalized approvals substituted.
    with_finalized_approvals: bool


@dataclasses.dataclass
class GetUptimeRequest():
    """Request payload: Get.Information.Uptime endpoint.

    """
    typeof: Endpoint = Endpoint.Get_Information_Uptime


@dataclasses.dataclass
class GetUptimeRequest1():
    """Request payload: Get.Information.Uptime endpoint.

    """
    typeof: Endpoint = Endpoint.Get_Information_Uptime


PAYLOAD_TYPESET: typing.Set[object] = {
    GetUptimeRequest1,
}
