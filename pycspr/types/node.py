from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr import crypto
from pycspr.type_defs.cl_values import CLV_Value
from pycspr.type_defs.crypto import \
    DigestBytes, \
    MerkleProofBytes, \
    PublicKey, \
    PublicKeyBytes, \
    PrivateKey, \
    Signature


AccountKey = typing.NewType(
    "On-chain account public key prefixed with ecc algo type.", bytes
    )

Address = typing.NewType(
    "Identifier of an on-chain account address.", bytes
    )

BlockHash = typing.NewType(
    "Digest over a block.", DigestBytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", int
)

BlockID = typing.Union[BlockHash, BlockHeight]

ContractID = typing.NewType(
    "Identifier of an on-chain smart contract.", bytes
    )

ContractVersion = typing.NewType(
    "Version of an on-chain smart contract.", int
    )

DeployHash = typing.NewType(
    "Identifier of a transaction.", DigestBytes
    )

EraID = typing.NewType(
    "Identifier of an era in chain time.", int
    )

Gas = typing.NewType(
    "Atomic unit of constraint over node compute.", int
    )

GasPrice = typing.NewType(
    "Price of gas within an era in chain time.", int
    )

Motes = typing.NewType(
    "Basic unit of crypto economic system.", int
    )

URefIdentifier = typing.NewType(
    "String encoded UREF identifier.", str
    )

WasmModule = typing.NewType(
    "WASM module payload.", bytes
    )

Weight = typing.NewType(
    "Some form of relative relevance measure.", int
    )

StateRootHash = typing.NewType(
    "Root digest of a node's global state.", DigestBytes
    )


class GlobalStateIDType(enum.Enum):
    BLOCK_HASH = "BlockHash"
    BLOCK_HEIGHT = "BlockHeight"
    STATE_ROOT_HASH = "StateRootHash"


class NodeEventChannel(enum.Enum):
    """Enumeration over set of exposed node SEE event types.

    """
    deploys = enum.auto()
    main = enum.auto()
    sigs = enum.auto()


class NodeEventType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.

    """
    ApiVersion = enum.auto()
    BlockAdded = enum.auto()
    DeployAccepted = enum.auto()
    DeployProcessed = enum.auto()
    DeployExpired = enum.auto()
    Fault = enum.auto()
    FinalitySignature = enum.auto()
    Shutdown = enum.auto()
    Step = enum.auto()


# Map: SSE channel <-> SSE event.
SSE_CHANNEL_TO_SSE_EVENT: typing.Dict[NodeEventChannel, typing.Set[NodeEventType]] = {
    NodeEventChannel.deploys: {
        NodeEventType.ApiVersion,
        NodeEventType.DeployAccepted
    },
    NodeEventChannel.main: {
        NodeEventType.ApiVersion,
        NodeEventType.BlockAdded,
        NodeEventType.DeployExpired,
        NodeEventType.DeployProcessed,
        NodeEventType.Fault,
        NodeEventType.Step
    },
    NodeEventChannel.sigs: {
        NodeEventType.ApiVersion,
        NodeEventType.FinalitySignature
    }
}


class PurseIDType(enum.Enum):
    PUBLIC_KEY = enum.auto()
    ACCOUNT_HASH = enum.auto()
    UREF = enum.auto()


class ReactorState(enum.Enum):
    INITIALIZE = "Initialize"
    CATCH_UP = "CatchUp"
    UPGRADING = "Upgrading"
    KEEP_UP = "KeepUp"
    VALIDATE = "Validate"
    SHUTDOWN_FOR_UPGRADE = "ShutdownForUpgrade"


class URefAccessRights(enum.Enum):
    NONE = 0
    READ = 1
    WRITE = 2
    ADD = 4
    READ_WRITE = 3
    READ_ADD = 5
    ADD_WRITE = 6
    READ_ADD_WRITE = 7


class ValidatorStatusChangeType(enum.Enum):
    ADDED = "Added"
    REMOVED = "Removed"
    BANNED = "Banned"
    CANNOT_PROPOSE = "CannotPropose"
    SEEN_AS_FAULTY = "SeenAsFaulty"


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
    public_key: PublicKey
    delegatee: Address
    staked_amount: Motes


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

    @property
    def era_id(self) -> EraID:
        """Helper attribute: era id."""
        return self.header.era_id

    @property
    def height(self) -> BlockHeight:
        """Helper attribute: block height."""
        return self.header.height

    @property
    def is_switch(self) -> bool:
        """Helper attribute: is a switch block."""
        return self.header.era_end is not None

    @property
    def signatories(self) -> typing.Set[PublicKey]:
        """Helper attribute: block signatories."""
        return set([i.public_key for i in self.proofs])

    @property
    def validator_weight_required_for_finality_in_next_era(self) -> int:
        return self.header.era_end.validator_weight_required_for_finality

    def get_finality_signature_weight(self, parent_switch_block: Block) -> int:
        return sum([
            i.weight for i in parent_switch_block.header.era_end.next_era_validator_weights \
            if i.validator in self.signatories
            ])


@dataclasses.dataclass
class BlockBody():
    proposer: Address
    deploy_hashes: typing.List[DeployHash]
    transfer_hashes: typing.List[DeployHash]

    def tx_hashes(self) -> typing.List[DeployHash]:
        return self.deploy_hashes + self.transfer_hashes


@dataclasses.dataclass
class BlockHeader():
    accumulated_seed: bytes
    body_hash: DigestBytes
    era_end: typing.Optional[EraEnd]
    era_id: EraID
    height: BlockHeight
    parent_hash: BlockHash
    protocol_version: ProtocolVersion
    random_bit: bool
    state_root: StateRootHash
    timestamp: Timestamp


@dataclasses.dataclass
class BlockSignature():
    public_key: PublicKey
    signature: Signature


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
            approval.signer
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
    signer: PublicKey
    signature: Signature

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
    body_hash: DigestBytes
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

    @property
    def next_era_signatories(self) -> typing.Set[PublicKey]:
        return set([i.validator for i in self.next_era_validator_weights])

    @property
    def validator_weight(self) -> int:
        return sum([i.weight for i in self.next_era_validator_weights])

    @property
    def validator_weight_required_for_finality(self) -> int:
        return int(self.validator_weight / 3) + 1


@dataclasses.dataclass
class EraEndReport():
    equivocators: typing.List[PublicKey]
    rewards: typing.List[ValidatorReward]
    inactive_validators: typing.List[PublicKey]


@dataclasses.dataclass
class EraSummary():
    block_hash: BlockHash
    era_id: EraID
    era_info: EraSummaryInfo
    merkle_proof: MerkleProofBytes
    state_root: StateRootHash


@dataclasses.dataclass
class EraSummaryInfo():
    seigniorage_allocations: typing.List[SeigniorageAllocation]


@dataclasses.dataclass
class GlobalStateID():
    identifier: typing.Union[BlockHash, BlockHeight, StateRootHash]
    id_type: "GlobalStateIDType"


@dataclasses.dataclass
class MinimalBlockInfo():
    creator: PublicKey
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
class NodeEventInfo():
    """Encapsulates emitted event information.

    """
    # Channel over which event emitted by a node.
    channel: NodeEventChannel

    # Type of event emitted by a node.
    typeof: NodeEventType

    # Event ordinal identifier - acts as an offset.
    idx: int

    # Event payload ... typically data but sometimes a simple string.
    payload: typing.Union[dict, str]


@dataclasses.dataclass
class NodePeer():
    address: str
    node_id: str


@dataclasses.dataclass
class NodeStatus():
    api_version: str
    available_block_range: typing.Tuple[int, int]
    build_version: str
    chainspec_name: str
    last_added_block_info: MinimalBlockInfo
    next_upgrade: NextUpgradeInfo
    our_public_signing_key: PublicKey
    peers: typing.List[NodePeer]
    reactor_state: ReactorState
    round_length: str
    starting_state_root_hash: StateRootHash
    uptime: str


@dataclasses.dataclass
class ProtocolVersion():
    major: int
    minor: int
    revision: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.revision}"


@dataclasses.dataclass
class PurseID():
    identifier: typing.Union[Address, PublicKeyBytes, URefIdentifier]
    id_type: "PurseIDType"


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
class Timestamp():
    value: float


@dataclasses.dataclass
class Transfer():
    amount: Motes
    deploy_hash: DeployHash
    from_: PublicKey
    gas: Gas
    source: URef
    target: URef
    correlation_id: int = None
    to_: PublicKey = None


@dataclasses.dataclass
class URef():
    access_rights: URefAccessRights
    address: Address


@dataclasses.dataclass
class ValidatorChanges():
    public_key: PublicKey
    status_changes: typing.List[ValidatorStatusChange]


@dataclasses.dataclass
class ValidatorReward():
    amount: Motes
    validator: PublicKey


@dataclasses.dataclass
class ValidatorStatusChange():
    era_id: EraID
    status_change: ValidatorStatusChangeType


@dataclasses.dataclass
class ValidatorWeight():
    validator: PublicKey
    weight: Weight


TYPESET: set = {
    AccountKey,
    Address,
    BlockHash,
    BlockHeight,
    BlockID,
    ContractID,
    ContractVersion,
    DeployHash,
    EraID,
    Gas,
    GasPrice,
    Motes,
    StateRootHash,
    WasmModule,
    Weight,
} | {
    GlobalStateID,
    GlobalStateIDType,
    NodeEventChannel,
    NodeEventType,
    PurseID,
    PurseIDType,
    ReactorState,
    URefAccessRights,
    ValidatorStatusChangeType,
} | {
    AccountInfo,
    ActionThresholds,
    AssociatedKey,
    AuctionBidByDelegator,
    AuctionBidByValidator,
    AuctionBidByValidatorInfo,
    AuctionState,
    AuctionStateEraValidators,
    Block,
    BlockBody,
    BlockHeader,
    BlockSignature,
    BlockTransfers,
    Deploy,
    DeployApproval,
    DeployArgument,
    DeployBody,
    DeployExecutionInfo,
    DeployExecutableItem,
    DeployHeader,
    DeployOfModuleBytes,
    DeployOfStoredContract,
    DeployOfStoredContractByHash,
    DeployOfStoredContractByHashVersioned,
    DeployOfStoredContractByName,
    DeployOfStoredContractByNameVersioned,
    DeployOfTransfer,
    DeployParameters,
    DeployTimeToLive,
    DictionaryID,
    DictionaryID_AccountNamedKey,
    DictionaryID_ContractNamedKey,
    DictionaryID_SeedURef,
    DictionaryID_UniqueKey,
    DictionaryItem,
    EraEnd,
    EraEndReport,
    EraSummary,
    EraSummaryInfo,
    MinimalBlockInfo,
    NamedKey,
    NextUpgradeInfo,
    NodeEventInfo,
    NodePeer,
    NodeStatus,
    ProtocolVersion,
    SeigniorageAllocation,
    SeigniorageAllocationForDelegator,
    SeigniorageAllocationForValidator,
    Timestamp,
    Transfer,
    URef,
    ValidatorChanges,
    ValidatorReward,
    ValidatorStatusChange,
    ValidatorWeight,
}
