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


AccountAddressBytes = typing.NewType(
    "Byte representation of an on chain address of an account mapped from an EOA public key.", bytes
    )


AccountKeyBytes = typing.NewType(
    "Byte representation of an account key.", bytes
    )


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

ChainNameDigest = typing.NewType(
    "Digest over a network's chain name.", DigestBytes
    )

DelegationRate = typing.NewType(
    "Delegation rate of tokens. Range from 0..=100.", int
    )

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many eras precede it.", int
)

GasPrice = typing.NewType(
    "Multiplier applied to estimation of computational costs (gas).", int
)

Motes = typing.NewType(
    "Basic unit of crypto economic system.", int
    )

StateRootHash = typing.NewType(
    "Root digest of a node's global state.", DigestBytes
    )

TransactionBodyHash = typing.NewType(
    "Digest over a transaction body.", DigestBytes
    )

TransactionHash = typing.NewType(
    "Digest over a transaction.", DigestBytes
    )

TransactionInitiatorAddress = typing.NewType(
    "Initiating address of a tx creator.", typing.Union[DigestBytes, PublicKey]
    )

Weight = typing.NewType(
    "Some form of relative relevance measure.", int
    )


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
class ConsensusReward():
    """Reward of a validator or a delegator during an era of consensus.

    """
    # Amount in motes of era reward.
    amount: Motes

    # Era within which reward was paid out.
    era_id: EraID

    # Rate of delegation to be paid from validaor to delegator.
    delegation_rate: DelegationRate

    # Identifier of switch block in which reward was distributed.
    switch_block_hash: BlockHash


@dataclasses.dataclass
class ConsensusStatus():
    """Current state of consensus.

    """
    # Consensus round leader.
    validator_public_key: int

    # Consensus round length (in time).
    round_length: typing.Optional[int]


@dataclasses.dataclass
class ConsensusValidatorChanges():
    """Set of validator changes within eras of consensus.

    """
    pass


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
class PricingMode():
    """Mode of tx execution pricing.

    """
    pass


@dataclasses.dataclass
class PricingMode_Classic(PricingMode):
    """Mode of tx execution pricing: tx creator specifies a gas limit & price.

    """
    # User-specified payment amount.
    payment_amount: int

    # User-specified gas_price tolerance (minimum 1).
    gas_price_tolerance: int

    # Flag indicating whether to utilise standard payment.
    standard_payment: bool = True


@dataclasses.dataclass
class PricingMode_Fixed(PricingMode):
    """Mode of tx execution pricing: determined by cost table as per tx category.

    """
    # User-specified gas_price tolerance (minimum 1).
    gas_price_tolerance: int


@dataclasses.dataclass
class PricingMode_Reserved(PricingMode):
    """Mode of tx execution pricing: tx payment was previously reserved.

    """
    # Pre-paid receipt.
    receipt: DigestBytes


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


@dataclasses.dataclass
class Transaction():
    """Transaction dispatched into and processed by network.

    """
    pass


@dataclasses.dataclass
class Transaction_V1():
    """Transaction version one.

    """
    pass


@dataclasses.dataclass
class Transaction_V2():
    """Transaction version two.

    """
    # Digest over tx contents.
    hash: TransactionHash

    # Header information.
    header: Transaction_V2_Header

    # body: TransactionV1Body,
    # approvals: BTreeSet<Approval>,


@dataclasses.dataclass
class Transaction_V2_Header():
    """Transaction version one header.

    """
    # Name of chain to which tx has been dispatched.
    chain_name: str

    # Instantiation timestamp.
    timestamp: Timestamp

    # Time period after which tx will no longer be processed.
    ttl: TimeDifference

    # Digest over tx body.
    body_hash: TransactionBodyHash

    # Mode of pricing to apply.
    pricing_mode: PricingMode

    # On-chain address of tx intiator.
    initiator_address: TransactionInitiatorAddress


class ValidatorChange(enum.Enum):
    """Enumeration over set of possible validator change reasons.

    """
    ADDED = enum.auto()
    REMOVED = enum.auto()
    BANNED = enum.auto()
    CANNOT_PROPOSE = enum.auto()
    SEEN_AS_FAULTY = enum.auto()


ValidatorID = typing.NewType(
    "Validator identifier.", PublicKey
    )
