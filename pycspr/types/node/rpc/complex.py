from __future__ import annotations

import dataclasses
import typing

from pycspr import crypto
from pycspr.types.cl.values import CLV_Value
from pycspr.types.crypto import Digest
from pycspr.types.crypto import MerkleProofBytes
from pycspr.types.crypto import PublicKey
from pycspr.types.crypto import PublicKeyBytes
from pycspr.types.crypto import PrivateKey
from pycspr.types.crypto import SignatureBytes
from pycspr.types.node.rpc.simple import Address
from pycspr.types.node.rpc.simple import BlockHash
from pycspr.types.node.rpc.simple import BlockHeight
from pycspr.types.node.rpc.simple import ContractID
from pycspr.types.node.rpc.simple import ContractVersion
from pycspr.types.node.rpc.simple import DeployHash
from pycspr.types.node.rpc.simple import EraID
from pycspr.types.node.rpc.simple import Gas
from pycspr.types.node.rpc.simple import GasPrice
from pycspr.types.node.rpc.simple import Motes
from pycspr.types.node.rpc.simple import ReactorState
from pycspr.types.node.rpc.simple import StateRootHash
from pycspr.types.node.rpc.simple import URefAccessRights
from pycspr.types.node.rpc.simple import ValidatorStatusChangeType
from pycspr.types.node.rpc.simple import WasmModule
from pycspr.types.node.rpc.simple import Weight


@dataclasses.dataclass
class AccountInfo():
    address: Address
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
    address: Address
    weight: Weight


@dataclasses.dataclass
class AuctionBidByDelegator():
    bonding_purse: URef
    public_key: PublicKeyBytes
    delegatee: Address
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
    era_validators: AuctionStateEraValidators
    state_root: StateRootHash


@dataclasses.dataclass
class AuctionStateEraValidators():
    era_id: EraID
    validator_weights: typing.List[ValidatorWeight]


@dataclasses.dataclass
class Block():
    body: BlockBody
    hash: BlockHash
    header: BlockHeader
    proofs: typing.List[BlockSignature]


@dataclasses.dataclass
class BlockBody():
    proposer: Address
    deploy_hashes: typing.List[DeployHash]
    transfer_hashes: typing.List[DeployHash]


@dataclasses.dataclass
class BlockHeader():
    accumulated_seed: bytes
    body_hash: Digest
    era_end: typing.Optional[EraEnd]
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
        self._append_approval(
            DeployApproval(
                approver.to_public_key(),
                crypto.get_signature_for_deploy_approval(self.hash, approver)
            )
        )

    def set_approval(self, approval: DeployApproval):
        """Appends an approval to associated set.

        :params approval: An approval to be associated with the deploy.

        """
        if not crypto.verify_deploy_approval_signature(
            self.hash,
            approval.signature,
            approval.signer.account_key
        ):
            raise ValueError("Invalid signature - please review your processes.")

        self._append_approval(approval)

    def _append_approval(self, approval: DeployApproval):
        """Appends an approval to managed set - implicitly deduplicating.

        :params approval: An approval to be associated with the deploy.

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
class DictionaryItem():
    dictionary_key: str
    merkle_proof: MerkleProofBytes
    stored_value: dict


@dataclasses.dataclass
class EraEnd():
    era_report: EraEndReport
    next_era_validator_weights: typing.List[ValidatorWeight]


@dataclasses.dataclass
class EraEndReport():
    equivocators: typing.List[PublicKeyBytes]
    rewards: typing.List[ValidatorReward]
    inactive_validators: typing.List[PublicKeyBytes]


@dataclasses.dataclass
class EraSummary():
    block_hash: BlockHash
    era_id: EraID
    era_info: EraSummaryInfo
    merkle_proof: MerkleProofBytes
    state_root: Digest


@dataclasses.dataclass
class EraSummaryInfo():
    seigniorage_allocations: typing.List[SeigniorageAllocation]


@dataclasses.dataclass
class MinimalBlockInfo():
    creator: PublicKeyBytes
    era_id: EraID
    hash: BlockHash
    height: BlockHeight
    state_root: StateRootHash
    timestamp: Timestamp


@dataclasses.dataclass
class NamedKey():
    key: str
    name: str


@dataclasses.dataclass
class NextUpgradeInfo():
    activation_point: str
    protocol_version: str


@dataclasses.dataclass
class NodePeer():
    address: str
    node_id: str


@dataclasses.dataclass
class NodeStatus():
    api_version: str
    build_version: str
    chainspec_name: str
    last_added_block_info: MinimalBlockInfo
    next_upgrade: NextUpgradeInfo
    our_public_signing_key: PublicKey
    peers: typing.List[NodePeer]
    reactor_state: ReactorState
    round_length: str
    starting_state_root_hash: Digest
    uptime: str


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


@dataclasses.dataclass
class ValidatorChanges():
    public_key: PublicKeyBytes
    status_changes: typing.List[ValidatorStatusChange]


@dataclasses.dataclass
class ValidatorReward():
    amount: Motes
    validator: PublicKeyBytes


@dataclasses.dataclass
class ValidatorStatusChange():
    era_id: EraID
    status_change: ValidatorStatusChangeType


@dataclasses.dataclass
class ValidatorWeight():
    validator: PublicKeyBytes
    weight: Weight
