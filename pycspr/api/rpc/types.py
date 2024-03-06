from __future__ import annotations

import dataclasses
import enum
import typing


Address = typing.NewType("Identifier of an on-chain account address.", bytes)

AccountID = typing.NewType("Identifier of an on-chain account.", bytes)

BlockHeight = typing.NewType("A specific location in a blockchain, measured by how many finalised blocks precede it.", int)

ContractID = typing.NewType("Identifier of an on-chain smart contract.", bytes)

ContractVersion = typing.NewType("Version of an on-chain smart contract.", int)

Digest = typing.NewType("Cryptographic fingerprint of data.", bytes)

EraID = typing.NewType("Identifier of an era in chain time.", int)

Gas = typing.NewType("Atomic unit of constraint over node compute.", int)

GasPrice = typing.NewType("Price of gas within an era in chain time.", int)

MerkleProof = typing.NewType("Cryptographic proof over a merkle trie.", bytes)

Motes = typing.NewType("Basic unit of crypto economic system.", int)

PublicKey = typing.NewType("Asymmetric public key associated with an account.", bytes)

Signature = typing.NewType("Cryptographic signature over data.", bytes)

WasmModule = typing.NewType("WASM payload module.", bytes)

Weight = typing.NewType("Some form of relative relevance measure.", int)


@dataclasses.dataclass
class AccountInfo():
    account_hash: AccountID
    action_thresholds: ActionThresholds
    associated_keys: typing.List[AssociatedKey]
    main_purse: URef
    named_keys: typing.List[NamedKey]


@dataclasses.dataclass
class ActionThresholds():
    deployment: Weight
    key_management: Weight


@dataclasses.dataclass
class AssociatedKey():
    account_hash: AccountID
    weight: Weight


@dataclasses.dataclass
class AuctionBidByDelegator():
    bonding_purse: URef
    public_key: PublicKey
    delegatee: AccountID
    staked_amount: Motes


@dataclasses.dataclass
class AuctionState():
    bids: typing.List[AuctionBidByValidator]
    block_height: BlockHeight
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
    staked_amount: Motes


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
    height: BlockHeight
    parent_hash: Digest
    protocol_version: ProtocolVersion
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
class CL_Value():
    pass


@dataclasses.dataclass
class Deploy():
    approvals: typing.List[DeployApproval]
    hash: Digest
    header: DeployHeader
    payment: dict
    session: dict
    execution_info: DeployExecutionInfo = None


@dataclasses.dataclass
class DeployApproval():
    signer: PublicKey
    signature: Signature


@dataclasses.dataclass
class DeployArgument():
    name: str
    value: CL_Value


@dataclasses.dataclass
class DeployExecutionInfo():
    block_hash: Digest
    results: dict


@dataclasses.dataclass
class DeployExecutableItem():
    args: typing.List[DeployArgument]


@dataclasses.dataclass
class DeployHeader():
    account: bytes
    body_hash: Digest
    chain_name: str
    dependencies: typing.List[Digest]
    gas_price: GasPrice
    timestamp: Timestamp
    ttl: DeployTimeToLive


@dataclasses.dataclass
class DeployOfModuleBytes(DeployExecutableItem):
    module_bytes: WasmModule


@dataclasses.dataclass
class DeployOfStoredContract(DeployExecutableItem):
    pass


@dataclasses.dataclass
class DeployOfStoredContractByHash(DeployOfStoredContract):
    hash: ContractID


@dataclasses.dataclass
class DeployOfStoredContractByHashVersioned(DeployOfStoredContractByHash):
    version: ContractVersion


@dataclasses.dataclass
class DeployOfStoredContractByName(DeployOfStoredContract):
    name: str


@dataclasses.dataclass
class DeployOfStoredContractByNameVersioned(DeployOfStoredContractByName):
    version: ContractVersion


@dataclasses.dataclass
class DeployOfTransfer(DeployExecutableItem):
    pass


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
    weight: Weight


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
    amount: Motes


@dataclasses.dataclass
class SeigniorageAllocationForDelegator(SeigniorageAllocation):
    delegator_public_key: PublicKey
    validator_public_key: PublicKey


@dataclasses.dataclass
class SeigniorageAllocationForValidator(SeigniorageAllocation):
    validator_public_key: PublicKey


@dataclasses.dataclass
class Transfer():
    amount: Motes
    deploy_hash: Digest
    from_: PublicKey
    gas: Gas
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
