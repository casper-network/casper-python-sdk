import dataclasses
import typing

from pycspr.api.node.bin.types.domain import BlockID


@dataclasses.dataclass
class GetBlockHeaderRequest():
    """Request payload: Get.Information.BlockHeader endpoint.

    """
    block_id: typing.Optional[BlockID]


@dataclasses.dataclass
class GetSignedBlockRequest():
    """Request payload: Get.Information.SignedBlock endpoint.

    """
    block_id: typing.Optional[BlockID]


@dataclasses.dataclass
class GetPeersRequest():
    """Request payload: Get.Information.Peers endpoint.

    """
    pass


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
