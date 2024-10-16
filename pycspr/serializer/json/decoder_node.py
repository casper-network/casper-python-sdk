import typing

from pycspr.serializer.json.decoder_clv import decode as decode_clv
from pycspr.serializer.json.decoder_crypto import DECODERS as CRYPTO_DECODERS
from pycspr.serializer.json.decoder_primitives import DECODERS as PRIMITIVES_DECODERS
from pycspr.type_defs.crypto import DigestHex
from pycspr.type_defs.crypto import MerkleProofHex
from pycspr.type_defs.crypto import PublicKey
from pycspr.type_defs.crypto import PublicKeyHex
from pycspr.type_defs.crypto import SignatureHex
from pycspr.types.node import Address
from pycspr.types.node import AccountInfo
from pycspr.types.node import AccountKey
from pycspr.types.node import ActionThresholds
from pycspr.types.node import AssociatedKey
from pycspr.types.node import AuctionBidByDelegator
from pycspr.types.node import AuctionBidByValidator
from pycspr.types.node import AuctionBidByValidatorInfo
from pycspr.types.node import AuctionState
from pycspr.types.node import AuctionStateEraValidators
from pycspr.types.node import Block
from pycspr.types.node import BlockHash
from pycspr.types.node import BlockBody
from pycspr.types.node import BlockHeader
from pycspr.types.node import BlockHeight
from pycspr.types.node import BlockSignature
from pycspr.types.node import BlockTransfers
from pycspr.types.node import ContractID
from pycspr.types.node import ContractVersion
from pycspr.types.node import Deploy
from pycspr.types.node import DeployApproval
from pycspr.types.node import DeployArgument
from pycspr.types.node import DeployExecutionInfo
from pycspr.types.node import DeployExecutableItem
from pycspr.types.node import DeployHash
from pycspr.types.node import DeployHeader
from pycspr.types.node import DeployOfModuleBytes
from pycspr.types.node import DeployOfStoredContractByHash
from pycspr.types.node import DeployOfStoredContractByHashVersioned
from pycspr.types.node import DeployOfStoredContractByName
from pycspr.types.node import DeployOfStoredContractByNameVersioned
from pycspr.types.node import DeployOfTransfer
from pycspr.types.node import DeployTimeToLive
from pycspr.types.node import DictionaryItem
from pycspr.types.node import EraID
from pycspr.types.node import EraEnd
from pycspr.types.node import EraEndReport
from pycspr.types.node import EraSummary
from pycspr.types.node import EraSummaryInfo
from pycspr.types.node import Gas
from pycspr.types.node import GasPrice
from pycspr.types.node import MinimalBlockInfo
from pycspr.types.node import Motes
from pycspr.types.node import NamedKey
from pycspr.types.node import NodePeer
from pycspr.types.node import NodeStatus
from pycspr.types.node import NextUpgradeInfo
from pycspr.types.node import ProtocolVersion
from pycspr.types.node import ReactorState
from pycspr.types.node import SeigniorageAllocation
from pycspr.types.node import SeigniorageAllocationForDelegator
from pycspr.types.node import SeigniorageAllocationForValidator
from pycspr.types.node import StateRootHash
from pycspr.types.node import Transfer
from pycspr.types.node import Timestamp
from pycspr.types.node import URef
from pycspr.types.node import URefAccessRights
from pycspr.types.node import ValidatorChanges
from pycspr.types.node import ValidatorReward
from pycspr.types.node import ValidatorStatusChange
from pycspr.types.node import ValidatorStatusChangeType
from pycspr.types.node import ValidatorWeight
from pycspr.types.node import WasmModule
from pycspr.types.node import Weight
from pycspr.utils import constants
from pycspr.utils import convertor


def decode(typedef: object, encoded: dict) -> object:
    """Decodes a domain entity instance from JSON encoded data.

    :param typedef: Domain type to be instantiated.
    :param encoded: JSON encoded data.
    :returns: A node related type instance.

    """
    try:
        decoder = DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json")
    else:
        return decoder(encoded)


def _decode_account_info(encoded: dict) -> AccountInfo:
    return AccountInfo(
        address=decode(Address, encoded["account_hash"]),
        action_thresholds=decode(ActionThresholds, encoded["action_thresholds"]),
        associated_keys=[decode(AssociatedKey, i) for i in encoded["associated_keys"]],
        main_purse=decode(URef, encoded["main_purse"]),
        named_keys=[decode(NamedKey, i) for i in encoded["named_keys"]],
    )


def _decode_action_thresholds(encoded: dict) -> ActionThresholds:
    return ActionThresholds(
        deployment=decode(Weight, encoded["deployment"]),
        key_management=decode(Weight, encoded["key_management"]),
    )


def _decode_address(encoded: str) -> Address:
    if encoded.startswith("account-hash-"):
        return decode(bytes, encoded[13:])
    else:
        return decode(bytes, encoded)


def _decode_associated_key(encoded: dict) -> AssociatedKey:
    return AssociatedKey(
        address=decode(Address, encoded["account_hash"]),
        weight=decode(Weight, encoded["weight"]),
        )


def _decode_auction_bid_by_delegator(encoded: dict) -> AuctionBidByDelegator:
    return AuctionBidByDelegator(
        bonding_purse=decode(URef, encoded["bonding_purse"]),
        delegatee=decode(PublicKeyHex, encoded["delegatee"]),
        public_key=decode(PublicKeyHex, encoded["public_key"]),
        staked_amount=decode(Motes, encoded["staked_amount"]),
    )


def _decode_auction_bid_by_validator(encoded: dict) -> AuctionBidByValidator:
    return AuctionBidByValidator(
        public_key=decode(PublicKeyHex, encoded["public_key"]),
        bid=decode(AuctionBidByValidatorInfo, encoded["bid"]),
    )


def _decode_auction_bid_by_validator_info(encoded: dict) -> AuctionBidByValidatorInfo:
    return AuctionBidByValidatorInfo(
        bonding_purse=decode(URef, encoded["bonding_purse"]),
        # TODO: verify
        delegation_rate=decode(int, encoded["delegation_rate"]),
        delegators=[decode(AuctionBidByDelegator, i) for i in encoded["delegators"]],
        inactive=decode(bool, encoded["inactive"]),
        staked_amount=decode(Motes, encoded["staked_amount"]),
    )


def _decode_auction_state(encoded: dict) -> AuctionState:
    return AuctionState(
        bids=[decode(AuctionBidByValidator, i) for i in encoded["bids"]],
        block_height=decode(BlockHeight, encoded["block_height"]),
        era_validators=[decode(AuctionStateEraValidators, i) for i in encoded["era_validators"]],
        state_root=decode(StateRootHash, encoded["state_root_hash"]),
    )


def _decode_auction_state_era_validators(encoded: dict) -> AuctionStateEraValidators:
    return AuctionStateEraValidators(
        era_id=decode(EraID, encoded["era_id"]),
        validator_weights=[decode(ValidatorWeight, i) for i in encoded["validator_weights"]]
    )


def _decode_block(encoded: dict) -> Block:
    return Block(
        body=decode(BlockBody, encoded["body"]),
        hash=decode(BlockHash, encoded["hash"]),
        header=decode(BlockHeader, encoded["header"]),
        proofs=[decode(BlockSignature, i) for i in encoded["proofs"]],
    )


def _decode_block_body(encoded: dict) -> BlockBody:
    return BlockBody(
        proposer=decode(PublicKeyHex, encoded["proposer"]),
        deploy_hashes=[decode(DeployHash, i) for i in encoded["deploy_hashes"]],
        transfer_hashes=[decode(DeployHash, i) for i in encoded["transfer_hashes"]],
    )


def _decode_block_header(encoded: dict) -> BlockHeader:
    return BlockHeader(
        accumulated_seed=decode(bytes, encoded["accumulated_seed"]),
        body_hash=decode(DigestHex, encoded["body_hash"]),
        era_end=decode(EraEnd, encoded["era_end"]),
        era_id=decode(EraID, encoded["era_id"]),
        height=decode(BlockHeight, encoded["height"]),
        parent_hash=decode(BlockHash, encoded["parent_hash"]),
        protocol_version=decode(ProtocolVersion, encoded["protocol_version"]),
        random_bit=decode(bool, encoded["random_bit"]),
        state_root=decode(StateRootHash, encoded["state_root_hash"]),
        timestamp=decode(Timestamp, encoded["timestamp"]),
        )


def _decode_block_signature(encoded: dict) -> BlockSignature:
    return BlockSignature(
        public_key=decode(PublicKeyHex, encoded["public_key"]),
        signature=decode(SignatureHex, encoded["signature"])
    )


def _decode_block_transfers(encoded: dict) -> BlockTransfers:
    return BlockTransfers(
        block_hash=decode(BlockHash, encoded["block_hash"]),
        transfers=[decode(Transfer, i) for i in encoded["transfers"]],
    )


def _decode_deploy(encoded: dict) -> Deploy:
    return Deploy(
        approvals=[decode(DeployApproval, i) for i in encoded["approvals"]],
        hash=decode(DeployHash, encoded["hash"]),
        header=decode(DeployHeader, encoded["header"]),
        payment=decode(DeployExecutableItem, encoded["payment"]),
        session=decode(DeployExecutableItem, encoded["session"])
    )


def _decode_deploy_approval(encoded: dict) -> DeployApproval:
    return DeployApproval(
        signer=PublicKey.from_bytes(
            decode(bytes, encoded["signer"])
            ),
        signature=decode(SignatureHex, encoded["signature"]),
    )


def _decode_deploy_argument(encoded: typing.Tuple[str, dict]) -> DeployArgument:
    return DeployArgument(
        name=decode(str, encoded[0]),
        value=decode_clv(encoded[1])
        )


def _decode_deploy_execution_info(encoded: list) -> DeployExecutionInfo:
    print("TODO: _decode_deploy_execution_info")
    return encoded


def _decode_deploy_executable_item(encoded: dict) -> DeployExecutableItem:
    def _decode_module_bytes(encoded: dict) -> DeployOfModuleBytes:
        if "ModuleBytes" in encoded:
            encoded = encoded["ModuleBytes"]

        return DeployOfModuleBytes(
            args=[decode(DeployArgument, i) for i in encoded["args"]],
            module_bytes=decode(bytes, encoded["module_bytes"]),
            )

    def _decode_stored_contract_by_hash(encoded: dict) -> DeployOfStoredContractByHash:
        if "StoredContractByHash" in encoded:
            encoded = encoded["StoredContractByHash"]

        return DeployOfStoredContractByHash(
            args=[decode(DeployArgument, i) for i in encoded["args"]],
            entry_point=decode(str, encoded["entry_point"]),
            hash=decode(ContractID, encoded["hash"]),
        )

    def _decode_stored_contract_by_hash_versioned(
        encoded: dict
    ) -> DeployOfStoredContractByHashVersioned:
        if "StoredVersionedContractByHash" in encoded:
            encoded = encoded["StoredVersionedContractByHash"]

        return DeployOfStoredContractByHashVersioned(
            args=[decode(DeployArgument, i) for i in encoded["args"]],
            entry_point=decode(str, encoded["entry_point"]),
            hash=decode(ContractID, encoded["hash"]),
            version=decode(ContractVersion, encoded["version"]),
        )

    def _decode_stored_contract_by_name(encoded: dict) -> DeployOfStoredContractByName:
        if "StoredContractByName" in encoded:
            encoded = encoded["StoredContractByName"]

        return DeployOfStoredContractByName(
            args=[decode(DeployArgument, i) for i in encoded["args"]],
            entry_point=decode(str, encoded["entry_point"]),
            name=decode(str, encoded["name"]),
        )

    def _decode_stored_contract_by_name_versioned(
        encoded: dict
    ) -> DeployOfStoredContractByNameVersioned:
        if "StoredVersionedContractByName" in encoded:
            encoded = encoded["StoredVersionedContractByName"]

        return DeployOfStoredContractByNameVersioned(
            args=[decode(DeployArgument, i) for i in encoded["args"]],
            entry_point=decode(str, encoded["entry_point"]),
            name=decode(str, encoded["name"]),
            version=decode(ContractVersion, encoded["version"]),
        )

    def _decode_transfer(encoded: dict) -> DeployOfTransfer:
        if "Transfer" in encoded:
            encoded = encoded["Transfer"]

        return DeployOfTransfer(
            args=[decode(DeployArgument, i) for i in encoded["args"]],
            )

    if "ModuleBytes" in encoded:
        decoder = _decode_module_bytes
    elif "StoredContractByHash" in encoded:
        decoder = _decode_stored_contract_by_hash
    elif "StoredVersionedContractByHash" in encoded:
        decoder = _decode_stored_contract_by_hash_versioned
    elif "StoredContractByName" in encoded:
        decoder = _decode_stored_contract_by_name
    elif "StoredVersionedContractByName" in encoded:
        decoder = _decode_stored_contract_by_name_versioned
    elif "Transfer" in encoded:
        decoder = _decode_transfer
    else:
        raise NotImplementedError(f"Unsupported DeployExecutableItem variant: {encoded}")

    return decoder(encoded)


def _decode_deploy_header(encoded: dict) -> DeployHeader:
    return DeployHeader(
        account=PublicKey.from_bytes(
            decode(bytes, encoded["account"])
        ),
        body_hash=decode(bytes, encoded["body_hash"]),
        chain_name=decode(str, encoded["chain_name"]),
        dependencies=[decode(DigestHex, i) for i in encoded["dependencies"]],
        gas_price=decode(GasPrice, encoded["gas_price"]),
        timestamp=decode(Timestamp, encoded["timestamp"]),
        ttl=decode(DeployTimeToLive, encoded["ttl"])
    )


def _decode_deploy_time_to_live(encoded: str) -> DeployTimeToLive:
    as_ms = convertor.ms_from_humanized_time_interval(encoded)
    if as_ms > constants.TX_MAX_TTL_MS:
        raise ValueError(f"Invalid deploy ttl. Maximum (ms)={constants.TX_MAX_TTL_MS}")

    return DeployTimeToLive(as_ms, encoded)


def _decode_dictionary_info(encoded: dict) -> DictionaryItem:
    return DictionaryItem(
        dictionary_key=decode(str, encoded["DictionaryInfo"]),
        merkle_proof=decode(MerkleProofHex, encoded["merkle_proof"]),
        stored_value=decode(dict, encoded["DictionaryInfo"]),
    )


def _decode_era_end(encoded: typing.Union[None, dict]) -> typing.Optional[EraEnd]:
    if encoded is not None:
        return EraEnd(
            era_report=decode(EraEndReport, encoded["era_report"]),
            next_era_validator_weights=[
                decode(ValidatorWeight, i) for i in encoded["next_era_validator_weights"]
            ]
        )


def _decode_era_end_report(encoded: dict) -> EraEndReport:
    return EraEndReport(
        equivocators=[decode(PublicKeyHex, i) for i in encoded["equivocators"]],
        rewards=[decode(ValidatorReward, i) for i in encoded["rewards"]],
        inactive_validators=[decode(PublicKeyHex, i) for i in encoded["inactive_validators"]],
    )


def _decode_era_summary(encoded: dict) -> EraSummary:
    return EraSummary(
        block_hash=decode(BlockHash, encoded["block_hash"]),
        era_id=decode(EraID, encoded["era_id"]),
        era_info=decode(EraSummaryInfo, encoded["stored_value"]["EraInfo"]),
        merkle_proof=decode(MerkleProofHex, encoded["merkle_proof"]),
        state_root=decode(StateRootHash, encoded["state_root_hash"]),
    )


def _decode_era_summary_info(encoded: dict) -> EraSummaryInfo:
    return EraSummaryInfo(
        seigniorage_allocations=[
            decode(SeigniorageAllocation, i) for i in encoded["seigniorage_allocations"]
            ]
    )


def _decode_minimal_block_info(encoded: dict) -> MinimalBlockInfo:
    return MinimalBlockInfo(
        creator=decode(PublicKeyHex, encoded["creator"]),
        era_id=decode(EraID, encoded["era_id"]),
        hash=decode(BlockHash, encoded["hash"]),
        height=decode(BlockHeight, encoded["height"]),
        state_root=decode(StateRootHash, encoded["state_root_hash"]),
        timestamp=decode(Timestamp, encoded["timestamp"]),
    )


def _decode_named_key(encoded: dict) -> NamedKey:
    return NamedKey(
        key=decode(str, encoded["key"]),
        name=decode(str, encoded["name"]),
    )


def _decode_next_upgrade_info(encoded: dict) -> NextUpgradeInfo:
    if encoded is not None:
        return NextUpgradeInfo(
            activation_point=decode(str, encoded["activation_point"]),
            protocol_version=decode(str, encoded["protocol_version"]),
        )


def _decode_node_peer(encoded: dict) -> NodePeer:
    return NodePeer(
        address=decode(str, encoded["address"]),
        node_id=decode(str, encoded["node_id"]),
    )


def _decode_node_status(encoded: dict) -> NodeStatus:
    # TODO: decode round length correctly
    return NodeStatus(
        api_version=decode(str, encoded["api_version"]),
        available_block_range=(
            encoded["available_block_range"]["low"],
            encoded["available_block_range"]["high"],
        ),
        build_version=decode(str, encoded["build_version"]),
        chainspec_name=decode(str, encoded["chainspec_name"]),
        last_added_block_info=decode(MinimalBlockInfo, encoded["last_added_block_info"]),
        next_upgrade=decode(NextUpgradeInfo, encoded["next_upgrade"]),
        our_public_signing_key=decode(PublicKeyHex, encoded["our_public_signing_key"]),
        peers=[decode(NodePeer, i) for i in encoded["peers"]],
        reactor_state=decode(ReactorState, encoded["reactor_state"]),
        round_length=decode(str, encoded["round_length"]),
        starting_state_root_hash=decode(StateRootHash, encoded["starting_state_root_hash"]),
        uptime=decode(str, encoded["uptime"]),
    )


def _decode_protocol_version(encoded: str) -> ProtocolVersion:
    major, minor, revision = [int(i) for i in encoded.split(".")]

    return ProtocolVersion(major, minor, revision)


def _decode_seigniorage_allocation(encoded: dict) -> SeigniorageAllocation:
    if "Delegator" in encoded:
        encoded = encoded["Delegator"]
        return SeigniorageAllocationForDelegator(
            amount=decode(Motes, encoded["amount"]),
            delegator_public_key=decode(PublicKeyHex, encoded["delegator_public_key"]),
            validator_public_key=decode(PublicKeyHex, encoded["validator_public_key"]),
        )

    if "Validator" in encoded:
        encoded = encoded["Validator"]
        return SeigniorageAllocationForValidator(
            amount=decode(Motes, encoded["amount"]),
            validator_public_key=decode(PublicKeyHex, encoded["validator_public_key"]),
        )

    raise ValueError("Invalid seigniorage allocation.")


def _decode_timestamp(encoded: str) -> Timestamp:
    return Timestamp(convertor.timestamp_from_iso_datetime(encoded))


def _decode_transfer(encoded: dict) -> Transfer:
    return Transfer(
        amount=decode(Motes, encoded["amount"]),
        deploy_hash=decode(DeployHash, encoded["deploy_hash"]),
        from_=decode(Address, encoded["from"]),
        gas=decode(Gas, encoded["gas"]),
        source=decode(URef, encoded["source"]),
        target=decode(URef, encoded["target"]),
        correlation_id=decode(int, encoded["id"]),
        to_=decode(Address, encoded["to"]),
    )


def _decode_uref(encoded: str) -> URef:
    # E.G. uref-bc4f1cd8cbb7a47464ea82e5dbd045c99f6c2fabedd54df1f50b08fbb9ed35ca-007.
    return URef(
        access_rights=decode(URefAccessRights, encoded[-3:]),
        address=decode(Address, encoded[5:-4]),
    )


def _decode_validator_changes(encoded: list) -> ValidatorChanges:
    return ValidatorChanges(
        public_key=decode(PublicKeyHex, encoded["public_key"]),
        status_changes=[decode(ValidatorStatusChange, i) for i in encoded["status_changes"]],
    )


def _decode_validator_reward(encoded: dict) -> ValidatorReward:
    return ValidatorReward(
        amount=decode(Motes, encoded["amount"]),
        validator=decode(PublicKeyHex, encoded["validator"]),
    )


def _decode_validator_status_change(encoded: dict) -> ValidatorStatusChange:
    return ValidatorStatusChange(
        era_id=decode(EraID, encoded["era_id"]),
        status_change=ValidatorStatusChangeType(encoded["validator_change"])
    )


def _decode_validator_weight(encoded: dict) -> ValidatorWeight:
    # Validator weights appear in different JSON data structures with
    # differing field names.
    pbk: PublicKeyHex = encoded.get("public_key", encoded.get("validator"))

    return ValidatorWeight(
        validator=decode(PublicKeyHex, pbk),
        weight=decode(Weight, encoded["weight"])
    )


DECODERS = PRIMITIVES_DECODERS | CRYPTO_DECODERS | {
    AccountKey: lambda x: decode(bytes, x),
    Address: _decode_address,
    BlockHash: lambda x: decode(DigestHex, x),
    BlockHeight: lambda x: decode(int, x),
    ContractID: lambda x: decode(bytes, x),
    ContractVersion: lambda x: decode(int, x),
    DeployHash: lambda x: decode(DigestHex, x),
    EraID: lambda x: decode(int, x),
    Gas: lambda x: decode(int, x),
    GasPrice: lambda x: decode(int, x),
    Motes: lambda x: decode(int, x),
    ReactorState: lambda x: ReactorState(x),
    StateRootHash: lambda x: decode(DigestHex, x),
    URefAccessRights: lambda x: URefAccessRights(int(x)),
    Weight: lambda x: decode(int, x),
    WasmModule: lambda x: decode(bytes, x),
} | {
    AccountInfo: _decode_account_info,
    ActionThresholds: _decode_action_thresholds,
    AssociatedKey: _decode_associated_key,
    AuctionBidByDelegator: _decode_auction_bid_by_delegator,
    AuctionBidByValidator: _decode_auction_bid_by_validator,
    AuctionBidByValidatorInfo: _decode_auction_bid_by_validator_info,
    AuctionState: _decode_auction_state,
    AuctionStateEraValidators: _decode_auction_state_era_validators,
    Block: _decode_block,
    BlockBody: _decode_block_body,
    BlockHeader: _decode_block_header,
    BlockSignature: _decode_block_signature,
    BlockTransfers: _decode_block_transfers,
    Deploy: _decode_deploy,
    DeployApproval: _decode_deploy_approval,
    DeployArgument: _decode_deploy_argument,
    DeployExecutionInfo: _decode_deploy_execution_info,
    DeployExecutableItem: _decode_deploy_executable_item,
    DeployHeader: _decode_deploy_header,
    DeployOfModuleBytes: _decode_deploy_executable_item,
    DeployOfStoredContractByHash: _decode_deploy_executable_item,
    DeployOfStoredContractByHashVersioned: _decode_deploy_executable_item,
    DeployOfStoredContractByName: _decode_deploy_executable_item,
    DeployOfStoredContractByNameVersioned: _decode_deploy_executable_item,
    DeployOfTransfer: _decode_deploy_executable_item,
    DeployTimeToLive: _decode_deploy_time_to_live,
    DictionaryItem: _decode_dictionary_info,
    EraEnd: _decode_era_end,
    EraEndReport: _decode_era_end_report,
    EraSummary: _decode_era_summary,
    EraSummaryInfo: _decode_era_summary_info,
    MinimalBlockInfo: _decode_minimal_block_info,
    NamedKey: _decode_named_key,
    NodePeer: _decode_node_peer,
    NodeStatus: _decode_node_status,
    NextUpgradeInfo: _decode_next_upgrade_info,
    ProtocolVersion: _decode_protocol_version,
    SeigniorageAllocation: _decode_seigniorage_allocation,
    Timestamp: _decode_timestamp,
    Transfer: _decode_transfer,
    URef: _decode_uref,
    ValidatorChanges: _decode_validator_changes,
    ValidatorReward: _decode_validator_reward,
    ValidatorStatusChange: _decode_validator_status_change,
    ValidatorWeight: _decode_validator_weight,
}
