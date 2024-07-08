import typing

from pycspr.api.node.bin.codec.decoder.primitives import \
    decode_u8
from pycspr.api.node.bin.types.domain import \
    BlockID, \
    BlockHash, \
    BlockHeight, \
    EraID, \
    PublicKey, \
    TransactionHash
from pycspr.api.node.bin.types.domain import \
    BlockHeader, \
    NodeUptime, \
    ProtocolVersion


def decode_block_header(bstream: bytes) -> typing.Tuple[bytes, BlockHeader]:
    raise NotImplementedError()


def decode_node_uptime(bstream: bytes) -> typing.Tuple[bytes, NodeUptime]:
    raise NotImplementedError()


def decode_protocol_version(bstream: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    bstream, major = decode_u8(bstream)
    bstream, minor = decode_u8(bstream)
    bstream, patch = decode_u8(bstream)

    return bstream, ProtocolVersion(major, minor, patch)


DECODERS: typing.Dict[typing.Type, typing.Callable] = {
    BlockHeader: decode_block_header,
    NodeUptime: decode_node_uptime,
    ProtocolVersion: decode_protocol_version,
}



# /// A type of the payload being returned in a binary response.
# #[derive(Debug, Copy, Clone, PartialEq, Eq)]
# #[repr(u8)]
# #[cfg_attr(feature = "json-schema", derive(JsonSchema))]
# pub enum PayloadType {
#     /// Legacy version of the block header.
#     BlockHeaderV1,
#     /// Block header.
#     BlockHeader,
#     /// Legacy version of the block body.
#     BlockBodyV1,
#     /// Block body.
#     BlockBody,
#     /// Legacy version of the approvals hashes.
#     ApprovalsHashesV1,
#     /// Approvals hashes
#     ApprovalsHashes,
#     /// Legacy version of the block signatures.
#     BlockSignaturesV1,
#     /// Block signatures.
#     BlockSignatures,
#     /// Deploy.
#     Deploy,
#     /// Transaction.
#     Transaction,
#     /// Legacy version of the execution result.
#     ExecutionResultV1,
#     /// Execution result.
#     ExecutionResult,
#     /// Wasm V1 execution result.
#     WasmV1Result,
#     /// Transfers.
#     Transfers,
#     /// Finalized deploy approvals.
#     FinalizedDeployApprovals,
#     /// Finalized approvals.
#     FinalizedApprovals,
#     /// Block with signatures.
#     SignedBlock,
#     /// Transaction with approvals and execution info.
#     TransactionWithExecutionInfo,
#     /// Peers.
#     Peers,
#     /// Last progress.
#     LastProgress,
#     /// State of the reactor.
#     ReactorState,
#     /// Network name.
#     NetworkName,
#     /// Consensus validator changes.
#     ConsensusValidatorChanges, // return type in `effects.rs` will be turned into dedicated type.
#     /// Status of the block synchronizer.
#     BlockSynchronizerStatus,
#     /// Available block range.
#     AvailableBlockRange,
#     /// Information about the next network upgrade.
#     NextUpgrade,
#     /// Consensus status.
#     ConsensusStatus, // return type in `effects.rs` will be turned into dedicated type.
#     /// Chainspec represented as raw bytes.
#     ChainspecRawBytes,
#     /// Uptime.
#     Uptime,
#     /// Result of checking if given block is in the highest available block range.
#     HighestBlockSequenceCheckResult,
#     /// Result of the speculative execution,
#     SpeculativeExecutionResult,
#     /// Result of querying global state,
#     GlobalStateQueryResult,
#     /// Result of querying global state for all values under a specified key.
#     StoredValues,
#     /// Result of querying global state for a full trie.
#     GetTrieFullResult,
#     /// Node status.
#     NodeStatus,
#     /// Result of querying for a dictionary item.
#     DictionaryQueryResult,
#     /// Balance query response.
#     BalanceResponse,
#     /// Reward response.
#     Reward,
# }
