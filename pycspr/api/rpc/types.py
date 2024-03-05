from __future__ import annotations

import dataclasses
import enum
import typing


# Identifiers.
Address = AccountID = bytes
Digest = bytes
EraID = int
PublicKey = bytes
Signature = bytes


@dataclasses.dataclass
class AccountInfo():
    account_hash: AccountID
    action_thresholds: ActionThresholds
    associated_keys: typing.List[AssociatedKey]
    main_purse: URef
    named_keys: typing.List[NamedKey]


@dataclasses.dataclass
class ActionThresholds():
    deployment: int
    key_management: int


@dataclasses.dataclass
class AssociatedKey():
    account_hash: AccountID
    weight: int


@dataclasses.dataclass
class AuctionBidByDelegator():
    bonding_purse: URef
    public_key: PublicKey
    delegatee: AccountID
    staked_amount: int


@dataclasses.dataclass
class AuctionState():
    bids: typing.List[AuctionBidByValidator]
    block_height: int
    era_validators: EraValidators
    state_root: Digest


@dataclasses.dataclass
class AuctionBidByValidator():
    public_key: PublicKey
    bid: AuctionBidByValidatorInfo


@dataclasses.dataclass
class AuctionBidByValidatorInfo():
    bonding_purse: URef
    delegation_rate: int
    delegators: typing.List[AuctionBidByDelegator]
    inactive: bool
    staked_amount: int


@dataclasses.dataclass
class Block():
    body: BlockBody
    hash: Digest
    header: BlockHeader
    proofs: typing.List[BlockSignature]


@dataclasses.dataclass
class BlockBody():
    proposer: AccountID
    deploy_hashes: typing.List[Digest]
    transfer_hashes: typing.List[Digest]


@dataclasses.dataclass
class BlockHeader():
    accumulated_seed: bytes
    body_hash: Digest
    era_id: EraID
    height: int
    parent_hash: Digest
    protocol_version: str
    random_bit: bool
    state_root: Digest


@dataclasses.dataclass
class BlockSignature():
    public_key: PublicKey
    signature: Signature


@dataclasses.dataclass
class BlockTransfers():
    block_hash: Digest
    transfers: typing.List[Transfer]


@dataclasses.dataclass
class Deploy():
    approvals: typing.List[DeployApproval]
    hash: Digest
    header: DeployHeader
    payment: dict
    session: dict


@dataclasses.dataclass
class DeployApproval():
    signer: PublicKey
    signature: Signature


@dataclasses.dataclass
class DeployHeader():
    account: bytes
    body_hash: Digest
    chain_name: str
    dependencies: typing.List[Digest]
    gas_price: int
    timestamp: Timestamp
    ttl: DeployTimeToLive


@dataclasses.dataclass
class DeployTimeToLive():
    as_milliseconds: int
    humanized: str


@dataclasses.dataclass
class EraValidators():
    era_id: EraID
    validator_weights: typing.List[EraValidatorWeight]


@dataclasses.dataclass
class EraValidatorWeight():
    public_key: PublicKey
    weight: int


@dataclasses.dataclass
class EraInfo():
    seigniorage_allocations: typing.List[SeigniorageAllocation]


@dataclasses.dataclass
class EraSummary():
    block_hash: Digest
    era_id: EraID
    era_info: EraInfo
    merkle_proof: str
    state_root: Digest


@dataclasses.dataclass
class NamedKey():
    key: str
    name: str


@dataclasses.dataclass
class ProtocolVersion():
    major: int
    minor: int
    revision: int


@dataclasses.dataclass
class SeigniorageAllocation():
    amount: int


@dataclasses.dataclass
class SeigniorageAllocationForDelegator(SeigniorageAllocation):
    delegator_public_key: PublicKey
    validator_public_key: PublicKey


@dataclasses.dataclass
class SeigniorageAllocationForValidator(SeigniorageAllocation):
    validator_public_key: PublicKey


@dataclasses.dataclass
class Transfer():
    amount: int
    deploy_hash: Digest
    from_: PublicKey
    gas: int
    source: URef
    target: URef
    correlation_id: int = None
    to_: PublicKey = None


@dataclasses.dataclass
class Timestamp():
    value: float


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
    address: Address


@dataclasses.dataclass
class ValidatorChanges():
    public_key: PublicKey
    status_changes: typing.List[ValidatorStatusChange]


@dataclasses.dataclass
class ValidatorStatusChange():
    era_id: EraID
    status_change: ValidatorStatusChangeType


class ValidatorStatusChangeType(enum.Enum):
    Added = 0
    Removed = 1
    Banned = 2
    CannotPropose = 4
    SeenAsFaulty = 3
