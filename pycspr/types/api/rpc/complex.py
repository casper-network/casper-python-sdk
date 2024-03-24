from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.crypto import get_signature_for_deploy_approval
from pycspr.crypto import verify_deploy_approval_signature
from pycspr.crypto.types import Digest
from pycspr.crypto.types import MerkleProofBytes
from pycspr.crypto.types import PublicKey
from pycspr.crypto.types import PublicKeyBytes
from pycspr.crypto.types import PrivateKey
from pycspr.crypto.types import SignatureBytes
from pycspr.types.cl.values import CLV_Value
from pycspr.types.api.rpc.simple import AccountID
from pycspr.types.api.rpc.simple import Address
from pycspr.types.api.rpc.simple import BlockHash
from pycspr.types.api.rpc.simple import BlockHeight
from pycspr.types.api.rpc.simple import ContractID
from pycspr.types.api.rpc.simple import ContractVersion
from pycspr.types.api.rpc.simple import DeployHash
from pycspr.types.api.rpc.simple import EraID
from pycspr.types.api.rpc.simple import Gas
from pycspr.types.api.rpc.simple import GasPrice
from pycspr.types.api.rpc.simple import Motes
from pycspr.types.api.rpc.simple import StateRootHash
from pycspr.types.api.rpc.simple import WasmModule
from pycspr.types.api.rpc.simple import Weight
from pycspr.utils import conversion
from pycspr.utils import constants


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
    public_key: PublicKeyBytes
    delegatee: AccountID
    staked_amount: Motes


@dataclasses.dataclass
class AuctionBidByValidator():
    public_key: PublicKeyBytes
    bid: AuctionBidByValidatorInfo


@dataclasses.dataclass
class AuctionBidByValidatorInfo():
    bonding_purse: URef
    delegation_rate: int
    delegators: typing.List[AuctionBidByDelegator]
    inactive: bool
    staked_amount: Motes


@dataclasses.dataclass
class AuctionState():
    bids: typing.List[AuctionBidByValidator]
    block_height: BlockHeight
    era_validators: EraValidators
    state_root: StateRootHash


@dataclasses.dataclass
class Block():
    body: BlockBody
    hash: BlockHash
    header: BlockHeader
    proofs: typing.List[BlockSignature]


@dataclasses.dataclass
class BlockBody():
    proposer: AccountID
    deploy_hashes: typing.List[DeployHash]
    transfer_hashes: typing.List[DeployHash]


@dataclasses.dataclass
class BlockHeader():
    accumulated_seed: bytes
    body_hash: Digest
    era_id: EraID
    height: BlockHeight
    parent_hash: BlockHash
    protocol_version: ProtocolVersion
    random_bit: bool
    state_root: StateRootHash


@dataclasses.dataclass
class BlockSignature():
    public_key: PublicKeyBytes
    signature: SignatureBytes


@dataclasses.dataclass
class BlockTransfers():
    block_hash: BlockHash
    transfers: typing.List[Transfer]


@dataclasses.dataclass
class Deploy():
    approvals: typing.List[DeployApproval]
    hash: DeployHash
    header: DeployHeader
    payment: DeployExecutableItem
    session: DeployExecutableItem
    execution_info: DeployExecutionInfo = None

    def __eq__(self, other: Deploy) -> bool:
        return self.approvals == other.approvals and \
               self.hash == other.hash and \
               self.header == other.header and \
               self.payment == other.payment and \
               self.session == other.session and \
               self.execution_info == other.execution_info

    def get_body(self) -> DeployBody:
        return DeployBody(
            payment=self.payment,
            session=self.session,
            hash=self.header.body_hash
        )

    def approve(self, approver: PrivateKey):
        """Creates a deploy approval & appends it to associated set.

        :params approver: Private key of entity approving the deploy.

        """
        sig = get_signature_for_deploy_approval(
            self.hash, approver.private_key, approver.key_algo
            )
        approval = DeployApproval(approver.to_public_key(), sig)
        self._append_approval(approval)

    def set_approval(self, approval: DeployApproval):
        """Appends an approval to associated set.

        :params approval: An approval to be associated with the deploy.

        """
        if not verify_deploy_approval_signature(
            self.hash,
            approval.signature,
            approval.signer.to_account_key()
        ):
            raise ValueError("Invalid signature - please review your processes.")

        self._append_approval(approval)

    def _append_approval(self, approval: DeployApproval):
        """Appends an approval to managed set - implicitly deduplicating.

        """
        self.approvals.append(approval)
        uniques = set()
        self.approvals = [
            uniques.add(a.signer) or a for a in self.approvals if a.signer not in uniques
            ]


@dataclasses.dataclass
class DeployApproval():
    signer: PublicKeyBytes
    signature: SignatureBytes

    def __eq__(self, other) -> bool:
        return self.signer == other.signer and self.signature == other.signature

    @property
    def sig(self) -> bytes:
        """Returns signature denuded of leading byte (representing ECC algo)."""
        return self.signature[1:]


@dataclasses.dataclass
class DeployArgument():
    name: str
    value: CLV_Value

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.value == other.value


@dataclasses.dataclass
class DeployBody():
    payment: DeployExecutableItem
    session: DeployExecutableItem
    hash: bytes

    def __eq__(self, other) -> bool:
        return self.payment == other.payment and \
               self.session == other.session and \
               self.hash == other.hash


@dataclasses.dataclass
class DeployExecutionInfo():
    block_hash: BlockHash
    results: dict


@dataclasses.dataclass
class DeployExecutableItem():
    args: typing.Union[typing.List[DeployArgument], typing.Dict[str, CLV_Value]]

    def __eq__(self, other) -> bool:
        return self.arguments == other.arguments

    @property
    def arguments(self) -> typing.List[DeployArgument]:
        if isinstance(self.args, list):
            return self.args
        elif isinstance(self.args, dict):
            return [DeployArgument(k, v) for (k, v) in self.args.items()]
        else:
            raise ValueError("Deploy arguments can be passed as either a list or dictionary")


@dataclasses.dataclass
class DeployHeader():
    account: PublicKey
    body_hash: Digest
    chain_name: str
    dependencies: typing.List[DeployHash]
    gas_price: GasPrice
    timestamp: Timestamp
    ttl: DeployTimeToLive

    def __eq__(self, other) -> bool:
        return self.account == other.account and \
               self.body_hash == other.body_hash and \
               self.chain_name == other.chain_name and \
               self.dependencies == other.dependencies and \
               self.gas_price == other.gas_price and \
               self.timestamp == other.timestamp and \
               self.ttl == other.ttl


@dataclasses.dataclass
class DeployOfModuleBytes(DeployExecutableItem):
    module_bytes: WasmModule

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.module_bytes == other.module_bytes


@dataclasses.dataclass
class DeployOfStoredContract(DeployExecutableItem):
    entry_point: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.entry_point == other.entry_point


@dataclasses.dataclass
class DeployOfStoredContractByHash(DeployOfStoredContract):
    hash: ContractID

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.hash == other.hash


@dataclasses.dataclass
class DeployOfStoredContractByHashVersioned(DeployOfStoredContractByHash):
    version: ContractVersion

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.version == other.version


@dataclasses.dataclass
class DeployOfStoredContractByName(DeployOfStoredContract):
    name: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.name == other.name


@dataclasses.dataclass
class DeployOfStoredContractByNameVersioned(DeployOfStoredContractByName):
    version: ContractVersion

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.version == other.version


@dataclasses.dataclass
class DeployOfTransfer(DeployExecutableItem):
    def __eq__(self, other) -> bool:
        return super().__eq__(other)


@dataclasses.dataclass
class DeployParameters():
    account: PublicKey
    chain_name: str
    dependencies: typing.List[bytes]
    gas_price: int
    timestamp: Timestamp
    ttl: "DeployTimeToLive"

    def __eq__(self, other) -> bool:
        return self.account == other.account and \
               self.chain_name == other.chain_name and \
               self.dependencies == other.dependencies and \
               self.gas_price == other.gas_price and \
               self.timestamp == other.timestamp and \
               self.ttl == other.ttl


@dataclasses.dataclass
class DeployTimeToLive():
    as_milliseconds: int
    humanized: str

    def __eq__(self, other) -> bool:
        return self.as_milliseconds == other.as_milliseconds and \
               self.humanized == other.humanized

    @staticmethod
    def from_string(as_string: str) -> "DeployTimeToLive":
        as_milliseconds = conversion.humanized_time_interval_to_milliseconds(as_string)
        if as_milliseconds > constants.DEPLOY_TTL_MS_MAX:
            raise ValueError(f"Invalid deploy ttl. Maximum (ms)={constants.DEPLOY_TTL_MS_MAX}")

        return DeployTimeToLive(
            as_milliseconds=as_milliseconds,
            humanized=as_string
        )

    @staticmethod
    def from_milliseconds(as_milliseconds: int) -> "DeployTimeToLive":
        return DeployTimeToLive(
            as_milliseconds,
            conversion.milliseconds_to_humanized_time_interval(as_milliseconds)
            )

    def to_string(self) -> str:
        return self.humanized


@dataclasses.dataclass
class DictionaryID():
    pass


@dataclasses.dataclass
class DictionaryID_AccountNamedKey(DictionaryID):
    account_key: str
    dictionary_item_key: str
    dictionary_name: str


@dataclasses.dataclass
class DictionaryID_ContractNamedKey(DictionaryID):
    contract_key: str
    dictionary_item_key: str
    dictionary_name: str


@dataclasses.dataclass
class DictionaryID_SeedURef(DictionaryID):
    dictionary_item_key: str
    seed_uref: object


@dataclasses.dataclass
class DictionaryID_UniqueKey(DictionaryID):
    key: str


@dataclasses.dataclass
class EraInfo():
    seigniorage_allocations: typing.List[SeigniorageAllocation]


@dataclasses.dataclass
class EraSummary():
    block_hash: BlockHash
    era_id: EraID
    era_info: EraInfo
    merkle_proof: MerkleProofBytes
    state_root: Digest


@dataclasses.dataclass
class EraValidators():
    era_id: EraID
    validator_weights: typing.List[EraValidatorWeight]


@dataclasses.dataclass
class EraValidatorWeight():
    public_key: PublicKeyBytes
    weight: Weight


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
    delegator_public_key: PublicKeyBytes
    validator_public_key: PublicKeyBytes


@dataclasses.dataclass
class SeigniorageAllocationForValidator(SeigniorageAllocation):
    validator_public_key: PublicKeyBytes


@dataclasses.dataclass
class Timestamp():
    value: float


@dataclasses.dataclass
class Transfer():
    amount: Motes
    deploy_hash: DeployHash
    from_: PublicKeyBytes
    gas: Gas
    source: URef
    target: URef
    correlation_id: int = None
    to_: PublicKeyBytes = None


@dataclasses.dataclass
class URef():
    access_rights: URefAccessRights
    address: Address


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
class ValidatorChanges():
    public_key: PublicKeyBytes
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
