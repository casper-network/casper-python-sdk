import dataclasses
import typing

from pycspr.api.node.bin.types.domain import \
    BlockID, \
    EraID, \
    PublicKey, \
    TransactionHash


@dataclasses.dataclass
class GetAvailableBlockRangeRequest():
    """Request payload: Get.Information.AvailableBlockRange endpoint.

    """
    pass


@dataclasses.dataclass
class GetBlockHeaderRequest():
    """Request payload: Get.Information.BlockHeader endpoint.

    """
    block_id: typing.Optional[BlockID]


@dataclasses.dataclass
class GetBlockSynchronizerStatusRequest():
    """Request payload: Get.Information.BlockSynchronizerStatus endpoint.

    """
    pass


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
    pass


# /// Request for information from the node.
# #[derive(Clone, Debug, PartialEq)]
# pub enum InformationRequest {
#     /// Returns the block header by an identifier, no identifier indicates the latest block.
#     BlockHeader(Option<BlockIdentifier>),
#     /// Returns the signed block by an identifier, no identifier indicates the latest block.
#     SignedBlock(Option<BlockIdentifier>),
#     /// Returns a transaction with approvals and execution info for a given hash.
#     Transaction {
#         /// Hash of the transaction to retrieve.
#         hash: TransactionHash,
#         /// Whether to return the deploy with the finalized approvals substituted.
#         with_finalized_approvals: bool,
#     },
#     /// Returns connected peers.
#     Peers,
#     /// Returns node uptime.
#     Uptime,
#     /// Returns last progress of the sync process.
#     LastProgress,
#     /// Returns current state of the main reactor.
#     ReactorState,
#     /// Returns network name.
#     NetworkName,
#     /// Returns consensus validator changes.
#     ConsensusValidatorChanges,
#     /// Returns status of the BlockSynchronizer.
#     BlockSynchronizerStatus,
#     /// Returns the available block range.
#     AvailableBlockRange,
#     /// Returns info about next upgrade.
#     NextUpgrade,
#     /// Returns consensus status.
#     ConsensusStatus,
#     /// Returns chainspec raw bytes.
#     ChainspecRawBytes,
#     /// Returns the status information of the node.
#     NodeStatus,
#     /// Returns the latest switch block header.
#     LatestSwitchBlockHeader,
#     /// Returns the reward for a validator or a delegator in a specific era.
#     Reward {
#         /// Identifier of the era to get the reward for. Must point to either a switch block or
#         /// a valid `EraId`. If `None`, the reward for the latest switch block is returned.
#         era_identifier: Option<EraIdentifier>,
#         /// Public key of the validator to get the reward for.
#         validator: Box<PublicKey>,
#         /// Public key of the delegator to get the reward for.
#         /// If `None`, the reward for the validator is returned.
#         delegator: Option<Box<PublicKey>>,
#     },
# }
