import dataclasses
import enum
import typing 


@dataclasses.dataclass
class AuctionBidByDelegator():
    bonding_purse: "URef"
    public_key: bytes
    delegatee: bytes
    staked_amount: int


@dataclasses.dataclass
class AuctionState():
    bids: typing.List["AuctionBidByValidator"]
    block_height: int
    era_validators: "EraValidators"
    state_root: bytes
    

@dataclasses.dataclass
class AuctionBidByValidator():
    public_key: bytes
    bid: "AuctionBidByValidatorInfo"


@dataclasses.dataclass
class AuctionBidByValidatorInfo():
    bonding_purse: "URef"
    delegation_rate: int
    delegators: typing.List["AuctionBidByDelegator"]
    inactive: bool
    staked_amount: int


@dataclasses.dataclass
class BlockTransfers():
    block_hash: bytes
    transfers: typing.List["Transfer"]


@dataclasses.dataclass
class EraValidators():
    era_id: int
    validator_weights: typing.List["EraValidatorWeight"]


@dataclasses.dataclass
class EraValidatorWeight():
    public_key: bytes
    weight: int


@dataclasses.dataclass
class EraInfo():
    seigniorage_allocations: typing.List["SeigniorageAllocation"]


@dataclasses.dataclass
class EraSummary():
    block_hash: bytes
    era_id: int
    era_info: EraInfo
    merkle_proof: str
    state_root: bytes


@dataclasses.dataclass
class SeigniorageAllocation():
    amount: int


@dataclasses.dataclass
class SeigniorageAllocationForDelegator(SeigniorageAllocation):
    delegator_public_key: bytes
    validator_public_key: bytes


@dataclasses.dataclass
class SeigniorageAllocationForValidator(SeigniorageAllocation):
    validator_public_key: bytes


@dataclasses.dataclass
class Transfer():
    amount: int
    deploy_hash: bytes
    from_: bytes
    gas: int
    source: "URef"
    target: "URef"
    correlation_id: int = None
    to_: bytes = None


class URefAccessRights(enum.Enum):
    NONE = 0
    READ = 1
    WRITE = 2
    ADD = 4
    READ_WRITE = 3
    READ_ADD = 5
    ADD_WRITE = 6
    READ_ADD_WRITE = 7


@dataclasses.dataclass
class URef():
    access_rights: URefAccessRights
    address: bytes


@dataclasses.dataclass
class ValidatorChanges():
    public_key: bytes
    status_changes: typing.List["ValidatorStatusChange"]


@dataclasses.dataclass
class ValidatorStatusChange():
    era_id: int
    status_change: "ValidatorStatusChangeType"


class ValidatorStatusChangeType(enum.Enum):
    Added = 0
    Removed = 1
    Banned = 2
    CannotPropose = 4
    SeenAsFaulty = 3
