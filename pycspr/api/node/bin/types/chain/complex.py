from __future__ import annotations

import dataclasses
import typing

from pycspr.api.node.bin.types.chain.simple import \
    BlockHash, \
    BlockHeight, \
    EraID, \
    Motes, \
    GasPrice, \
    Weight
from pycspr.api.node.bin.types.crypto import \
    DigestBytes, \
    PublicKey, \
    PublicKeyBytes
from pycspr.api.node.bin.types.primitives.time import Timestamp


@dataclasses.dataclass
class ActivationPoint():
    """Point in time at which next chain upgrade activiation will occur.

    """
    pass


@dataclasses.dataclass
class ActivationPoint_Era(ActivationPoint):
    """Era at which upgrade activiation will occur.

    """
    # ID of era at which chain upgrade will occur.
    era_id: EraID


@dataclasses.dataclass
class ActivationPoint_Genesis(ActivationPoint):
    """Genesis timestamp at which upgrade activiation will occur.

    """
    # Timestamp upon which genesis started.
    timestamp: Timestamp


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
    # Body of block.
    # body: typing.Union["BlockBody_V1", "BlockBody_V2"]

    # Digest over block.
    hash: "BlockHash"

    # Header of block.
    header: typing.Union["BlockHeader_V1", "BlockHeader_V2"]


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


@dataclasses.dataclass
class ChainspecRawBytes():
    """Raw byte view over a chainspec.

    """
    # Raw bytes of the current chainspec.toml file.
    chainspec_bytes: bytes

    # Raw bytes of the current genesis accounts.toml file.
    maybe_genesis_accounts_bytes: typing.Optional[bytes]

    # Raw bytes of the current global_state.toml file.
    maybe_global_state_bytes: typing.Optional[bytes]


@dataclasses.dataclass
class ConsensusStatus():
    """Current state of consensus.

    """
    # Consensus round leader.
    validator_public_key: int

    # Consensus round length (in time).
    round_length: typing.Optional[int]

# pub struct ConsensusStatus {
#     validator_public_key: PublicKey,
#     round_length: Option<TimeDiff>,
# }

@dataclasses.dataclass
class EraEnd():
    """End of era information.

    """
    pass


@dataclasses.dataclass
class EraEnd_V1(EraEnd):
    """End of era information scoped by block header version 1.

    """
    pass


@dataclasses.dataclass
class EraEnd_V2(EraEnd):
    """End of era information scoped by block header version 2.

    """
    # Set of equivocators to be punished.
    equivocators: typing.List[ValidatorID]

    # Validators that haven't produced any unit during era.
    inactive_validators: typing.List[ValidatorID]

    # Next era gas price computed from a moving average.
    next_era_gas_price: GasPrice

    # Next era validator set & their respective weights.
    next_era_validator_weights: typing.List[EraValidatorWeight]

    # Rewards distributed to validators.
    rewards: typing.List[EraValidatorReward]


@dataclasses.dataclass
class EraValidatorReward():
    """Reward distributed to a validator in respect of protocol participation scoped by era.

    """
    # Reward amounts in motes.
    rewards: typing.List[Motes]

    # Identifier of a validator (i.e. public key).
    validator: ValidatorID


@dataclasses.dataclass
class EraValidatorWeight():
    """Weight of a validator in respect of protocol participation scoped by era.

    """
    # Identifier of a validator (i.e. public key).
    validator_id: ValidatorID

    # Consensus weight scoped by era.
    weight: Weight

    def __str__(self) -> str:
        return f"ValidatorWeight({self.validator_id}::{self.weight})"


@dataclasses.dataclass
class NextUpgrade():
    """Future point in chain time when an upgrade will be applied.

    """
    # Activation point of the next upgrade.
    activation_point: ActivationPoint

    # Network protocol version at point when block was created.
    protocol_version: ProtocolVersion


@dataclasses.dataclass
class ProtocolVersion():
    """Version of protocol.

    """
    # Major semantic version.
    major: int

    # Minor semantic version.
    minor: int

    # Patch semantic version.
    patch: int

    @staticmethod
    def from_semvar(val: str):
        major, minor, patch = val.split(".")

        return ProtocolVersion(
            int(major),
            int(minor),
            int(patch)
        )

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


ValidatorID = typing.NewType(
    "Validator identifier.", PublicKey
    )
