import typing

from pycspr.api.rpc.types import AccountID
from pycspr.api.rpc.types import AccountInfo
from pycspr.api.rpc.types import ActionThresholds
from pycspr.api.rpc.types import AssociatedKey
from pycspr.api.rpc.types import AuctionBidByDelegator
from pycspr.api.rpc.types import AuctionBidByValidator
from pycspr.api.rpc.types import AuctionBidByValidatorInfo
from pycspr.api.rpc.types import AuctionState
from pycspr.api.rpc.types import Block
from pycspr.api.rpc.types import BlockBody
from pycspr.api.rpc.types import BlockHeader
from pycspr.api.rpc.types import BlockSignature
from pycspr.api.rpc.types import BlockTransfers
from pycspr.api.rpc.types import Deploy
from pycspr.api.rpc.types import DeployApproval
from pycspr.api.rpc.types import DeployExecutableItem
from pycspr.api.rpc.types import DeployHeader
from pycspr.api.rpc.types import DeployOfModuleBytes
from pycspr.api.rpc.types import DeployOfStoredContractByHash
from pycspr.api.rpc.types import DeployOfStoredContractByHashVersioned
from pycspr.api.rpc.types import DeployOfStoredContractByName
from pycspr.api.rpc.types import DeployOfStoredContractByNameVersioned
from pycspr.api.rpc.types import DeployOfTransfer
from pycspr.api.rpc.types import DeployTimeToLive
from pycspr.api.rpc.types import Digest
from pycspr.api.rpc.types import EraInfo
from pycspr.api.rpc.types import EraSummary
from pycspr.api.rpc.types import EraValidators
from pycspr.api.rpc.types import EraValidatorWeight
from pycspr.api.rpc.types import NamedKey
from pycspr.api.rpc.types import ProtocolVersion
from pycspr.api.rpc.types import PublicKey
from pycspr.api.rpc.types import SeigniorageAllocation
from pycspr.api.rpc.types import SeigniorageAllocationForDelegator
from pycspr.api.rpc.types import SeigniorageAllocationForValidator
from pycspr.api.rpc.types import StoredContractDeploy
from pycspr.api.rpc.types import Transfer
from pycspr.api.rpc.types import Timestamp
from pycspr.api.rpc.types import URef
from pycspr.api.rpc.types import URefAccessRights
from pycspr.api.rpc.types import ValidatorChanges
from pycspr.api.rpc.types import ValidatorStatusChange
from pycspr.api.rpc.types import ValidatorStatusChangeType
from pycspr.utils import conversion


def decode(encoded: dict, typedef: type) -> object:
    """Decodes a domain entity from a JSON object.

    :param obj: A JSON compatible dictionary.
    :param typedef: Domain entity type definition.
    :returns: A domain entity.

    """
    try:
        decoder = _DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json object")
    else:
        return decoder(encoded)


def _decode_account_id(encoded: str) -> bytes:
    # E.G. account-hash-2c4a11c062a8a337bfc97e27fd66291caeb2c65865dcb5d3ef3759c4c97efecb
    return bytes.fromhex(encoded[13:])


def _decode_account_info(encoded: dict) -> AccountInfo:
    return AccountInfo(
        account_hash=decode(encoded["account_hash"], AccountID),
        action_thresholds=decode(encoded["action_thresholds"], ActionThresholds),
        associated_keys=[decode(i, AssociatedKey) for i in encoded["associated_keys"]],
        main_purse=decode(encoded["main_purse"], URef),
        named_keys=[decode(i, NamedKey) for i in encoded["named_keys"]],
    )


def _decode_action_thresholds(encoded: dict) -> ActionThresholds:
    return ActionThresholds(
        deployment=decode(encoded["deployment"], int),
        key_management=decode(encoded["key_management"], int),
    )


def _decode_associated_key(encoded: dict) -> AssociatedKey:
    return AssociatedKey(
        account_hash=decode(encoded["account_hash"], AccountID),
        weight=decode(encoded["weight"], int),
        )


def _decode_auction_bid_by_delegator(encoded: dict) -> AuctionBidByDelegator:
    return AuctionBidByDelegator(
        bonding_purse=decode(encoded["bonding_purse"], URef),
        delegatee=decode(encoded["delegatee"], bytes),
        public_key=decode(encoded["public_key"], bytes),
        staked_amount=decode(encoded["staked_amount"], int),
    )


def _decode_auction_bid_by_validator(encoded: dict) -> AuctionBidByValidator:
    return AuctionBidByValidator(
        public_key=decode(encoded["public_key"], bytes),
        bid=decode(encoded["bid"], AuctionBidByValidatorInfo),
    )


def _decode_auction_bid_by_validator_info(encoded: dict) -> AuctionBidByValidatorInfo:
    return AuctionBidByValidatorInfo(
        bonding_purse=decode(encoded["bonding_purse"], URef),
        delegation_rate=decode(encoded["delegation_rate"], int),
        delegators=[decode(i, AuctionBidByDelegator) for i in encoded["delegators"]],
        inactive=encoded["inactive"],
        staked_amount=decode(encoded["staked_amount"], int),
    )


def _decode_auction_state(encoded: dict) -> AuctionState:
    return AuctionState(
        bids=[decode(i, AuctionBidByValidator) for i in encoded["bids"]],
        block_height=encoded["block_height"],
        era_validators=[decode(i, EraValidators) for i in encoded["era_validators"]],
        state_root=decode(encoded["state_root_hash"], bytes),
    )


def _decode_block(encoded: dict) -> Block:
    return Block(
        body=decode(encoded["body"], BlockBody),
        hash=decode(encoded["hash"], bytes),
        header=decode(encoded["header"], BlockHeader),
        proofs=[decode(i, BlockSignature) for i in encoded["proofs"]],
    )


def _decode_block_body(encoded: dict) -> BlockBody:
    return BlockBody(
        proposer=decode(encoded["proposer"], bytes),
        deploy_hashes=[decode(i, bytes) for i in encoded["deploy_hashes"]],
        transfer_hashes=[decode(i, bytes) for i in encoded["transfer_hashes"]],
    )


def _decode_block_header(encoded: dict) -> BlockHeader:
    return BlockHeader(
        accumulated_seed=decode(encoded["accumulated_seed"], bytes),
        body_hash=decode(encoded["body_hash"], bytes),
        era_id=decode(encoded["era_id"], int),
        height=decode(encoded["height"], int),
        parent_hash=decode(encoded["parent_hash"], bytes),
        protocol_version=decode(encoded["protocol_version"], ProtocolVersion),
        random_bit=decode(encoded["random_bit"], bool),
        state_root=decode(encoded["state_root_hash"], bytes),
        )


def _decode_block_signature(encoded: dict) -> BlockSignature:
    return BlockSignature(
        public_key=decode(encoded["public_key"], PublicKey),
        signature=decode(encoded["signature"], bytes)
    )


def _decode_block_transfers(encoded: dict) -> BlockTransfers:
    return BlockTransfers(
        block_hash=encoded["block_hash"].encode("utf-8"),
        transfers=decode(encoded["transfers"], Transfer)
    )


def _decode_deploy(encoded: dict) -> Deploy:
    return Deploy(
        approvals=[decode(i, DeployApproval) for i in encoded["approvals"]],
        hash=decode(encoded["hash"], bytes),
        header=decode(encoded["header"], DeployHeader),
        payment=decode(encoded["payment"], DeployExecutableItem),
        session=decode(encoded["session"], DeployExecutableItem),
    )


def _decode_deploy_approval(encoded: dict) -> DeployApproval:
    return DeployApproval(
        signer=decode(encoded["signer"], PublicKey),
        signature=decode(encoded["signature"], bytes)
    )


def _decode_deploy_executable_item(encoded: dict) -> DeployExecutableItem:
    if "ModuleBytes" in encoded:
        return decode(encoded, DeployOfModuleBytes)
    elif "StoredContractByHash" in encoded:
        return decode(encoded, DeployOfStoredContractByHash)
    elif "StoredVersionedContractByHash" in encoded:
        return decode(encoded, DeployOfStoredContractByHashVersioned)
    elif "StoredContractByName" in encoded:
        return decode(encoded, DeployOfStoredContractByName)
    elif "StoredVersionedContractByName" in encoded:
        return decode(encoded, DeployOfStoredContractByNameVersioned)
    elif "Transfer" in encoded:
        return decode(encoded, DeployOfTransfer)
    else:
        raise NotImplementedError("Unsupported DeployExecutableItem variant")


def _decode_deploy_header(encoded: dict) -> DeployHeader:
    return DeployHeader(
        account=decode(encoded["account"], PublicKey),
        body_hash=decode(encoded["body_hash"], bytes),
        chain_name=encoded["chain_name"],
        dependencies=[decode(i, Digest) for i in encoded["dependencies"]],
        gas_price=int(encoded["gas_price"]),
        timestamp=decode(encoded["timestamp"], Timestamp),
        ttl=decode(encoded["ttl"], DeployTimeToLive)
    )


def _decode_deploy_of_module_bytes(encoded: dict) -> DeployOfModuleBytes:
    return encoded


def _decode_deploy_of_stored_contract_by_hash(encoded: dict) -> DeployOfStoredContractByHash:
    return encoded


def _decode_deploy_of_stored_contract_by_hash_versioned(
    encoded: dict
) -> DeployOfStoredContractByHashVersioned:
    return encoded


def _decode_deploy_of_stored_contract_by_name(encoded: dict) -> DeployOfStoredContractByName:
    return encoded


def _decode_deploy_of_stored_contract_by_name_versioned(
    encoded: dict
) -> DeployOfStoredContractByNameVersioned:
    return encoded


def _decode_deploy_of_transfer(encoded: dict) -> DeployOfTransfer:
    return encoded


def _decode_deploy_time_to_live(encoded: str) -> DeployTimeToLive:
    return DeployTimeToLive(
        as_milliseconds=conversion.humanized_time_interval_to_milliseconds(encoded),
        humanized=encoded
    )


def _decode_digest(encoded: str) -> bytes:
    return decode(encoded, bytes)


def _decode_era_info(encoded: dict) -> EraInfo:
    return EraInfo(
        seigniorage_allocations=[
            _decode_seigniorage_allocation(i) for i in encoded["seigniorage_allocations"]
            ]
    )


def _decode_era_validators(encoded: dict) -> EraValidators:
    return EraValidators(
        era_id=encoded["era_id"],
        validator_weights=[decode(i, EraValidatorWeight) for i in encoded["validator_weights"]]
    )


def _decode_era_validator_weight(encoded: dict) -> EraValidatorWeight:
    return EraValidatorWeight(
        public_key=decode(encoded["public_key"], PublicKey),
        weight=int(encoded["weight"])
    )


def _decode_era_summary(encoded: dict) -> EraSummary:
    return EraSummary(
        block_hash=decode(encoded["block_hash"], bytes),
        era_id=encoded["era_id"],
        era_info=decode(encoded["stored_value"]["EraInfo"], EraInfo),
        merkle_proof=decode(encoded["merkle_proof"], bytes),
        state_root=decode(encoded["state_root_hash"], bytes),
    )


def _decode_merkle_proof(encoded: str) -> bytes:
    return decode(encoded, bytes)


def _decode_motes(encoded: str) -> int:
    return int(encoded)


def _decode_named_key(encoded: dict) -> NamedKey:
    return NamedKey(
        key=encoded["key"],
        name=encoded["name"],
    )


def _decode_protocol_version(encoded: str) -> ProtocolVersion:
    major, minor, revision = encoded.split(".")

    return ProtocolVersion(
        major=int(major),
        minor=int(minor),
        revision=int(revision)
        )


def _decode_public_key(encoded: str) -> bytes:
    return decode(encoded, bytes)


def _decode_primitive_bool(encoded: str) -> bool:
    return bool(encoded)


def _decode_primitive_bytes(encoded: str) -> bytes:
    return bytes.fromhex(encoded)


def _decode_primitive_int(encoded: str) -> int:
    return int(encoded)


def _decode_seigniorage_allocation(encoded: dict) -> SeigniorageAllocation:
    def decode_delegator_seigniorage_allocation(encoded: dict):
        return SeigniorageAllocationForDelegator(
            amount=decode(encoded["amount"], int),
            delegator_public_key=decode(encoded["delegator_public_key"], bytes),
            validator_public_key=decode(encoded["validator_public_key"], bytes),
        )

    def decode_validator_seigniorage_allocation(encoded: dict):
        return SeigniorageAllocationForValidator(
            amount=decode(encoded["amount"], int),
            validator_public_key=decode(encoded["validator_public_key"], bytes),
        )

    if "Delegator" in encoded:
        return decode_delegator_seigniorage_allocation(encoded["Delegator"])
    elif "Validator" in encoded:
        return decode_validator_seigniorage_allocation(encoded["Validator"])
    else:
        raise ValueError("decode_seigniorage_allocation")


def _decode_stored_value(encoded: dict) -> typing.Union[EraInfo]:
    if "EraInfo" in encoded:
        _decode_era_info(encoded["EraInfo"])


def _decode_timestamp(encoded: str) -> Timestamp:
    return Timestamp(
        value=conversion.posix_timestamp_from_isoformat(encoded)
    )


def _decode_transfer(encoded: dict) -> Transfer:
    return Transfer(
        amount=decode(encoded["amount"], int),
        deploy_hash=bytes.fromhex(encoded["deploy_hash"]),
        from_=decode(encoded["from"], AccountID),
        gas=int(encoded["gas"]),
        source=decode(encoded["source"], URef),
        target=decode(encoded["target"], URef),
        correlation_id=int(encoded["id"]),
        to_=decode(encoded["to"], AccountID),
    )


def _decode_uref(encoded: str) -> URef:
    # E.G. uref-bc4f1cd8cbb7a47464ea82e5dbd045c99f6c2fabedd54df1f50b08fbb9ed35ca-007.
    return URef(
        access_rights=URefAccessRights(int(encoded[-3:])),
        address=bytes.fromhex(encoded[5:-4])
    )


def _decode_validator_status_change(encoded: dict) -> ValidatorStatusChange:
    return ValidatorStatusChange(
        era_id=int(encoded["era_id"]),
        status_change=ValidatorStatusChangeType[encoded["validator_change"]]
    )


def _decode_validator_changes(encoded: list) -> ValidatorChanges:
    return ValidatorChanges(
        public_key=decode(encoded["public_key"], bytes),
        status_changes=[decode(i, ValidatorStatusChange) for i in encoded["status_changes"]],
    )


_DECODERS = {
    bool: _decode_primitive_bool,
    bytes: _decode_primitive_bytes,
    int: _decode_primitive_int,
} | {
    AccountID: _decode_account_id,
    Digest: _decode_digest,
    PublicKey: _decode_public_key,
} | {
    AccountInfo: _decode_account_info,
    ActionThresholds: _decode_action_thresholds,
    AssociatedKey: _decode_associated_key,
    AuctionBidByDelegator: _decode_auction_bid_by_delegator,
    AuctionBidByValidator: _decode_auction_bid_by_validator,
    AuctionBidByValidatorInfo: _decode_auction_bid_by_validator_info,
    AuctionState: _decode_auction_state,
    Block: _decode_block,
    BlockBody: _decode_block_body,
    BlockHeader: _decode_block_header,
    BlockSignature: _decode_block_signature,
    BlockTransfers: _decode_block_transfers,
    Deploy: _decode_deploy,
    DeployApproval: _decode_deploy_approval,
    DeployExecutableItem: _decode_deploy_executable_item,
    DeployHeader: _decode_deploy_header,
    DeployOfModuleBytes: _decode_deploy_of_module_bytes,
    DeployOfStoredContractByHash: _decode_deploy_of_stored_contract_by_hash,
    DeployOfStoredContractByHashVersioned: _decode_deploy_of_stored_contract_by_hash_versioned,
    DeployOfStoredContractByName: _decode_deploy_of_stored_contract_by_name,
    DeployOfStoredContractByNameVersioned: _decode_deploy_of_stored_contract_by_name_versioned,
    DeployOfTransfer: _decode_deploy_of_transfer,
    DeployTimeToLive: _decode_deploy_time_to_live,
    EraInfo: _decode_era_info,
    EraValidators: _decode_era_validators,
    EraValidatorWeight: _decode_era_validator_weight,
    EraSummary: _decode_era_summary,
    NamedKey: _decode_named_key,
    ProtocolVersion: _decode_protocol_version,
    Timestamp: _decode_timestamp,
    Transfer: _decode_transfer,
    URef: _decode_uref,
    ValidatorChanges: _decode_validator_changes,
    ValidatorStatusChange: _decode_validator_status_change,
}


def _map(func: typing.Callable, data: list) -> list:
    return [func(i) for i in data]
