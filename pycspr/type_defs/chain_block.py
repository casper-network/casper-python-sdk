from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.type_defs.crypto import \
    DigestBytes, \
    PublicKey, \
    PublicKeyBytes, \
    Signature
from pycspr.type_defs.primitives import \
    U64, \
    TimeDifference, \
    Timestamp


BlockBodyHash = typing.NewType(
    "Digest over a block's body.", DigestBytes
    )

BlockHash = typing.NewType(
    "Digest over a block.", DigestBytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", U64
)

BlockID = typing.Union[BlockHash, BlockHeight]

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many eras precede it.", int
)

@dataclasses.dataclass
class AvailableBlockRange():
    """A range of block heights that a node may be aware of.

    """
    # End lower bound.
    low: int

    # End upper bound.
    high: int


@dataclasses.dataclass
class Block():
    """A block after execution, with the resulting global state root hash.

    """
    pass


@dataclasses.dataclass
class Block_V1(Block):
    """A version one block after execution, with the resulting global state root hash.

    """
    # Body of block.
    body: BlockBody_V1

    # Digest over block.
    hash: BlockHash

    # Header of block.
    header: BlockHeader_V1


@dataclasses.dataclass
class Block_V2(Block):
    """A version two block after execution, with the resulting global state root hash.

    """
    # Body of block.
    body: BlockBody_V2

    # Digest over block.
    hash: BlockHash

    # Header of block.
    header: BlockHeader_V2


@dataclasses.dataclass
class BlockBody():
    """A block after execution, with the resulting global state root hash.

    """
    pass


@dataclasses.dataclass
class BlockBody_V1(BlockBody):
    """A version one block body.

    """
    pass


@dataclasses.dataclass
class BlockBody_V2(BlockBody):
    """A version two block body.

    """
    # Digest over block body.
    hash: BlockBodyHash

    # List of identifiers for finality signatures for a particular past block.
    rewarded_signatures: RewardedSignatures

    # Map of transactions mapping categories to a list of transaction hashes.
    transactions: typing.Dict[int, TransactionHash]


@dataclasses.dataclass
class BlockHeader():
    """Block header encpasulating versioned header portion of a block.

    """
    pass


@dataclasses.dataclass
class BlockHeader_V1(BlockHeader):
    """Block header encpasulating version 1 header portion of a block.

    """
    # Future era initializion seed.
    accumulated_seed: DigestBytes

    # Digest over block body.
    body_hash: DigestBytes

    # Digest over block body.
    era_end: typing.Optional[EraEnd_V1]

    # Height of era, i.e. number of ancestors.
    era_id: EraID

    # Height of block, i.e. number of ancestors.
    height: BlockHeight

    # Digest over parent block.
    parent_hash: BlockHash

    # Future era initializion random bit.
    random_bit: bool

    # Network protocol version at point when block was created.
    protocol_version: ProtocolVersion

    # Digest over post block execution state root.
    state_root_hash: DigestBytes

    # Timestamp from when the block was proposed.
    timestamp: bytes


@dataclasses.dataclass
class BlockHeader_V2(BlockHeader):
    """Block header encpasulating version 2 header portion of a block.

    """
    # A seed needed for initializing a future era.
    accumulated_seed: DigestBytes

    # The hash of the block's body.
    body_hash: DigestBytes

    # The gas price of the era
    current_gas_price: GasPrice

    # The `EraEnd` of a block if it is a switch block.
    era_end: typing.Optional[EraEnd_V2]

    # The era ID in which this block was created.
    era_id: EraID

    # The height of this block, i.e. the number of ancestors.
    height: BlockHeight

    # The most recent switch block hash.
    last_switch_block_hash: typing.Optional[BlockHash]

    # The parent block's hash.
    parent_hash: BlockHash

    # The public key of the validator which proposed the block.
    proposer: PublicKeyBytes

    # The protocol version of the network from when this block was created.
    protocol_version: ProtocolVersion

    # A random bit needed for initializing a future era.
    random_bit: bool

    # The root hash of global state after the deploys in this block have been executed.
    state_root_hash: DigestBytes

    # The timestamp from when the block was proposed.
    timestamp: Timestamp


@dataclasses.dataclass
class BlockSignatures():
    """A collection of signatures for a single block, along
       with the associated block's hash & era id.

    """
    pass


@dataclasses.dataclass
class BlockSignatures_V1(BlockSignatures):
    """Block signatures pertaining to version 1 blocks.

    """
    # Computed digest over block contents.
    block_hash: BlockHash

    # Era ID in which this block was created.
    era_id: EraID

    # Set of proofs over block, i.e. collection of validators' signatures over block hash.
    proofs: typing.Dict[PublicKey, Signature]


@dataclasses.dataclass
class BlockSignatures_V2(BlockSignatures):
    """Block signatures pertaining to version 2 blocks.

    """
    # Computed digest over block contents.
    block_hash: BlockHash

    # Height of block within linear block chain.
    block_height: BlockHeight

    # Era ID in which this block was created.
    era_id: EraID

    # Digest over block's associated chain name.
    chain_name_hash: ChainNameDigest

    # Set of proofs over block, i.e. collection of validators' signatures over block hash.
    proofs: typing.Dict[PublicKey, Signature]


@dataclasses.dataclass
class BlockSynchronizerStatus():
    """Status of the block synchronizer.

    """
    # The status of syncing a historical block, if any.
    historical: typing.Optional[BlockSynchronizerStatusInfo]

    # The status of syncing a forward block, if any.
    forward: typing.Optional[BlockSynchronizerStatusInfo]


@dataclasses.dataclass
class BlockSynchronizerStatusInfo():
    """Status of the block synchronizer.

    """
    # The block hash.
    block_hash: BlockHash

    # The height of the block, if known.
    block_height: typing.Optional[int]

    # The state of acquisition of the data associated with the block.
    acquisition_state: str


RewardedSignatures = typing.NewType(
    "Finality signatures to be rewarded within a block.", typing.List["SingleBlockRewardedSignatures"]
    )


SingleBlockRewardedSignatures = typing.NewType(
    "Finality signature identifiers for a recent block.", bytes
    )


@dataclasses.dataclass
class SignedBlock():
    """A block plus associated signatures over that block.

    """
    # A block encapsulating a set of transactions.
    block: Block

    # Set of signatures over block.
    signatures: BlockSignatures
