from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.type_defs.chain_


from pycspr.type_defs.crypto import PublicKey
from pycspr.type_defs.primitives import \
    U64, \
    TimeDifference, \
    Timestamp


DelegationRate = typing.NewType(
    "Delegation rate of tokens. Range from 0..=100.", int
    )

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many eras precede it.", int
)

Weight = typing.NewType(
    "Some form of relative relevance measure.", int
    )


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
