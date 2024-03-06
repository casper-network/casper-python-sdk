from __future__ import annotations

import typing

from pycspr.api.rpc.types import AccountID
from pycspr.api.rpc.types import AccountInfo
from pycspr.api.rpc.types import ActionThresholds
from pycspr.api.rpc.types import Address
from pycspr.api.rpc.types import AssociatedKey
from pycspr.api.rpc.types import AuctionBidByDelegator
from pycspr.api.rpc.types import AuctionBidByValidator
from pycspr.api.rpc.types import AuctionBidByValidatorInfo
from pycspr.api.rpc.types import AuctionState
from pycspr.api.rpc.types import Block
from pycspr.api.rpc.types import BlockBody
from pycspr.api.rpc.types import BlockHeader
from pycspr.api.rpc.types import BlockHeight
from pycspr.api.rpc.types import BlockSignature
from pycspr.api.rpc.types import BlockTransfers
from pycspr.api.rpc.types import ContractID
from pycspr.api.rpc.types import ContractVersion
from pycspr.api.rpc.types import Deploy
from pycspr.api.rpc.types import DeployApproval
from pycspr.api.rpc.types import DeployArgument
from pycspr.api.rpc.types import DeployExecutionInfo
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
from pycspr.api.rpc.types import EraID
from pycspr.api.rpc.types import EraInfo
from pycspr.api.rpc.types import EraSummary
from pycspr.api.rpc.types import EraValidators
from pycspr.api.rpc.types import EraValidatorWeight
from pycspr.api.rpc.types import Gas
from pycspr.api.rpc.types import GasPrice
from pycspr.api.rpc.types import MerkleProof
from pycspr.api.rpc.types import Motes
from pycspr.api.rpc.types import NamedKey
from pycspr.api.rpc.types import ProtocolVersion
from pycspr.api.rpc.types import PublicKey
from pycspr.api.rpc.types import SeigniorageAllocation
from pycspr.api.rpc.types import SeigniorageAllocationForDelegator
from pycspr.api.rpc.types import SeigniorageAllocationForValidator
from pycspr.api.rpc.types import Signature
from pycspr.api.rpc.types import DeployOfStoredContract
from pycspr.api.rpc.types import Transfer
from pycspr.api.rpc.types import Timestamp
from pycspr.api.rpc.types import URef
from pycspr.api.rpc.types import URefAccessRights
from pycspr.api.rpc.types import ValidatorChanges
from pycspr.api.rpc.types import ValidatorStatusChange
from pycspr.api.rpc.types import ValidatorStatusChangeType
from pycspr.api.rpc.types import WasmModule
from pycspr.api.rpc.types import Weight
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


def _decode_account_id(encoded: str) -> AccountID:
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
        deployment=decode(encoded["deployment"], Weight),
        key_management=decode(encoded["key_management"], Weight),
    )


def _decode_address(encoded: str) -> Address:
    return bytes.fromhex(encoded)


def _decode_associated_key(encoded: dict) -> AssociatedKey:
    return AssociatedKey(
        account_hash=decode(encoded["account_hash"], AccountID),
        weight=decode(encoded["weight"], Weight),
        )


def _decode_auction_bid_by_delegator(encoded: dict) -> AuctionBidByDelegator:
    return AuctionBidByDelegator(
        bonding_purse=decode(encoded["bonding_purse"], URef),
        delegatee=decode(encoded["delegatee"], PublicKey),
        public_key=decode(encoded["public_key"], PublicKey),
        staked_amount=decode(encoded["staked_amount"], Motes),
    )


def _decode_auction_bid_by_validator(encoded: dict) -> AuctionBidByValidator:
    return AuctionBidByValidator(
        public_key=decode(encoded["public_key"], PublicKey),
        bid=decode(encoded["bid"], AuctionBidByValidatorInfo),
    )


def _decode_auction_bid_by_validator_info(encoded: dict) -> AuctionBidByValidatorInfo:
    return AuctionBidByValidatorInfo(
        bonding_purse=decode(encoded["bonding_purse"], URef),
        # TODO: verify
        delegation_rate=decode(encoded["delegation_rate"], int),
        delegators=[decode(i, AuctionBidByDelegator) for i in encoded["delegators"]],
        inactive=decode(encoded["inactive"], bool),
        staked_amount=decode(encoded["staked_amount"], Motes),
    )


def _decode_auction_state(encoded: dict) -> AuctionState:
    return AuctionState(
        bids=[decode(i, AuctionBidByValidator) for i in encoded["bids"]],
        block_height=decode(encoded["block_height"], BlockHeight),
        era_validators=[decode(i, EraValidators) for i in encoded["era_validators"]],
        state_root=decode(encoded["state_root_hash"], Digest),
    )


def _decode_bool(encoded: str) -> bool:
    return bool(encoded)


def _decode_block(encoded: dict) -> Block:
    return Block(
        body=decode(encoded["body"], BlockBody),
        hash=decode(encoded["hash"], Digest),
        header=decode(encoded["header"], BlockHeader),
        proofs=[decode(i, BlockSignature) for i in encoded["proofs"]],
    )


def _decode_block_body(encoded: dict) -> BlockBody:
    return BlockBody(
        proposer=decode(encoded["proposer"], PublicKey),
        deploy_hashes=[decode(i, Digest) for i in encoded["deploy_hashes"]],
        transfer_hashes=[decode(i, Digest) for i in encoded["transfer_hashes"]],
    )


def _decode_block_header(encoded: dict) -> BlockHeader:
    return BlockHeader(
        accumulated_seed=decode(encoded["accumulated_seed"], bytes),
        body_hash=decode(encoded["body_hash"], Digest),
        era_id=decode(encoded["era_id"], EraID),
        height=decode(encoded["height"], BlockHeight),
        parent_hash=decode(encoded["parent_hash"], Digest),
        protocol_version=decode(encoded["protocol_version"], ProtocolVersion),
        random_bit=decode(encoded["random_bit"], bool),
        state_root=decode(encoded["state_root_hash"], Digest),
        )


def _decode_block_height(encoded: str) -> BlockHeight:
    return decode(encoded, int)


def _decode_block_signature(encoded: dict) -> BlockSignature:
    return BlockSignature(
        public_key=decode(encoded["public_key"], PublicKey),
        signature=decode(encoded["signature"], Signature)
    )


def _decode_block_transfers(encoded: dict) -> BlockTransfers:
    return BlockTransfers(
        block_hash=decode(encoded["block_hash"], Digest),
        transfers=decode(encoded["transfers"], Transfer)
    )


def _decode_bytes(encoded: str) -> bytes:
    return bytes.fromhex(encoded)


def _decode_deploy(encoded: dict) -> Deploy:
    return Deploy(
        approvals=[decode(i, DeployApproval) for i in encoded["approvals"]],
        hash=decode(encoded["hash"], Digest),
        header=decode(encoded["header"], DeployHeader),
        payment=decode(encoded["payment"], DeployExecutableItem),
        session=decode(encoded["session"], DeployExecutableItem),
        execution_info=decode(encoded["execution_info"], DeployExecutionInfo),
    )


def _decode_deploy_approval(encoded: dict) -> DeployApproval:
    return DeployApproval(
        signer=decode(encoded["signer"], PublicKey),
        signature=decode(encoded["signature"], Signature)
    )


def _decode_deploy_argument(encoded: list) -> DeployArgument:
    name, value = encoded
    print(encoded)
    return DeployArgument(
        name=decode(name, str),
        value=value,
    )


def _decode_deploy_execution_info(encoded: list) -> DeployExecutionInfo:
    print("TODO: _decode_deploy_execution_info")
    return encoded


def _decode_deploy_executable_item(encoded: dict) -> DeployExecutableItem:
    if "ModuleBytes" in encoded:
        return decode(encoded["ModuleBytes"], DeployOfModuleBytes)
    elif "StoredContractByHash" in encoded:
        return decode(encoded["StoredContractByHash"], DeployOfStoredContractByHash)
    elif "StoredVersionedContractByHash" in encoded:
        return decode(encoded["StoredVersionedContractByHash"], DeployOfStoredContractByHashVersioned)
    elif "StoredContractByName" in encoded:
        return decode(encoded["StoredContractByName"], DeployOfStoredContractByName)
    elif "StoredVersionedContractByName" in encoded:
        return decode(encoded["StoredVersionedContractByName"], DeployOfStoredContractByNameVersioned)
    elif "Transfer" in encoded:
        return decode(encoded["Transfer"], DeployOfTransfer)
    else:
        raise NotImplementedError("Unsupported DeployExecutableItem variant")


def _decode_deploy_header(encoded: dict) -> DeployHeader:
    return DeployHeader(
        account=decode(encoded["account"], PublicKey),
        body_hash=decode(encoded["body_hash"], Digest),
        chain_name=decode(encoded["chain_name"], str),
        dependencies=[decode(i, Digest) for i in encoded["dependencies"]],
        gas_price=decode(encoded["gas_price"], GasPrice),
        timestamp=decode(encoded["timestamp"], Timestamp),
        ttl=decode(encoded["ttl"], DeployTimeToLive)
    )


def _decode_deploy_of_module_bytes(encoded: dict) -> DeployOfModuleBytes:
    return DeployOfModuleBytes(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        module_bytes=decode(encoded["module_bytes"], WasmModule)
    )


def _decode_deploy_of_stored_contract_by_hash(encoded: dict) -> DeployOfStoredContractByHash:
    return DeployOfStoredContractByHash(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        hash=decode(encoded["hash"], Digest),
    )


def _decode_deploy_of_stored_contract_by_hash_versioned(
    encoded: dict
) -> DeployOfStoredContractByHashVersioned:
    return DeployOfStoredContractByNameVersioned(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        hash=decode(encoded["hash"], Digest),
        version=decode(encoded["version"], ContractVersion),
    )

def _decode_deploy_of_stored_contract_by_name(encoded: dict) -> DeployOfStoredContractByName:
    return DeployOfStoredContractByName(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        name=decode(encoded["name"], str),
    )


def _decode_deploy_of_stored_contract_by_name_versioned(
    encoded: dict
) -> DeployOfStoredContractByNameVersioned:
    return DeployOfStoredContractByNameVersioned(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        name=decode(encoded["name"], str),
        version=decode(encoded["version"], ContractVersion),
    )


def _decode_deploy_of_transfer(encoded: dict) -> DeployOfTransfer:
    return DeployOfTransfer(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
    )


def _decode_deploy_time_to_live(encoded: str) -> DeployTimeToLive:
    return DeployTimeToLive(
        as_milliseconds=conversion.humanized_time_interval_to_milliseconds(encoded),
        humanized=encoded
    )


def _decode_digest(encoded: str) -> bytes:
    return decode(encoded, bytes)


def _decode_era_id(encoded: str) -> EraID:
    return decode(encoded, int)


def _decode_era_info(encoded: dict) -> EraInfo:
    return EraInfo(
        seigniorage_allocations=[
            decode(i, SeigniorageAllocation) for i in encoded["seigniorage_allocations"]
            ]
    )


def _decode_era_validators(encoded: dict) -> EraValidators:
    return EraValidators(
        era_id=decode(encoded["era_id"], EraID),
        validator_weights=[decode(i, EraValidatorWeight) for i in encoded["validator_weights"]]
    )


def _decode_era_validator_weight(encoded: dict) -> EraValidatorWeight:
    return EraValidatorWeight(
        public_key=decode(encoded["public_key"], PublicKey),
        weight=decode(encoded["weight"], Weight)
    )


def _decode_era_summary(encoded: dict) -> EraSummary:
    return EraSummary(
        block_hash=decode(encoded["block_hash"], Digest),
        era_id=decode(encoded["era_id"], EraID),
        era_info=decode(encoded["stored_value"]["EraInfo"], EraInfo),
        merkle_proof=decode(encoded["merkle_proof"], MerkleProof),
        state_root=decode(encoded["state_root_hash"], Digest),
    )


def _decode_gas(encoded: str) -> Gas:
    return decode(encoded, int)


def _decode_gas_price(encoded: str) -> GasPrice:
    return decode(encoded, int)


def _decode_int(encoded: str) -> int:
    return int(encoded)


def _decode_merkle_proof(encoded: str) -> MerkleProof:
    return decode(encoded, bytes)


def _decode_motes(encoded: str) -> Motes:
    return int(encoded)


def _decode_named_key(encoded: dict) -> NamedKey:
    return NamedKey(
        key=decode(encoded["key"], str),
        name=decode(encoded["name"], str),
    )


def _decode_protocol_version(encoded: str) -> ProtocolVersion:
    major, minor, revision = encoded.split(".")

    return ProtocolVersion(
        major=int(major),
        minor=int(minor),
        revision=int(revision)
        )


def _decode_public_key(encoded: str) -> PublicKey:
    return decode(encoded, bytes)


def _decode_seigniorage_allocation(encoded: dict) -> SeigniorageAllocation:
    def decode_delegator_seigniorage_allocation(encoded: dict):
        return SeigniorageAllocationForDelegator(
            amount=decode(encoded["amount"], Motes),
            delegator_public_key=decode(encoded["delegator_public_key"], PublicKey),
            validator_public_key=decode(encoded["validator_public_key"], PublicKey),
        )

    def decode_validator_seigniorage_allocation(encoded: dict):
        return SeigniorageAllocationForValidator(
            amount=decode(encoded["amount"], Motes),
            validator_public_key=decode(encoded["validator_public_key"], PublicKey),
        )

    if "Delegator" in encoded:
        return decode_delegator_seigniorage_allocation(encoded["Delegator"])
    elif "Validator" in encoded:
        return decode_validator_seigniorage_allocation(encoded["Validator"])
    else:
        raise ValueError("decode_seigniorage_allocation")


def _decode_signature(encoded: str) -> Signature:
    return decode(encoded, bytes)


def _decode_stored_value(encoded: dict) -> typing.Union[EraInfo]:
    if "EraInfo" in encoded:
        _decode_era_info(encoded["EraInfo"])


def _decode_str(encoded: str) -> str:
    return encoded.strip()


def _decode_timestamp(encoded: str) -> Timestamp:
    return Timestamp(
        value=conversion.posix_timestamp_from_isoformat(encoded)
    )


def _decode_transfer(encoded: dict) -> Transfer:
    return Transfer(
        amount=decode(encoded["amount"], Motes),
        deploy_hash=decode(encoded["deploy_hash"], Digest),
        from_=decode(encoded["from"], AccountID),
        gas=decode(encoded["gas"], Gas),
        source=decode(encoded["source"], URef),
        target=decode(encoded["target"], URef),
        correlation_id=decode(encoded["id"], int),
        to_=decode(encoded["to"], AccountID),
    )


def _decode_uref(encoded: str) -> URef:
    # E.G. uref-bc4f1cd8cbb7a47464ea82e5dbd045c99f6c2fabedd54df1f50b08fbb9ed35ca-007.
    return URef(
        access_rights=decode(encoded[-3:], URefAccessRights),
        address=decode(encoded[5:-4], Address),
    )


def _decode_uref_access_rights(encoded: str) -> URefAccessRights:
    return URefAccessRights(int(encoded))


def _decode_validator_status_change(encoded: dict) -> ValidatorStatusChange:
    return ValidatorStatusChange(
        era_id=decode(encoded["era_id"], EraID),
        status_change=ValidatorStatusChangeType[encoded["validator_change"]]
    )


def _decode_validator_changes(encoded: list) -> ValidatorChanges:
    return ValidatorChanges(
        public_key=decode(encoded["public_key"], PublicKey),
        status_changes=[decode(i, ValidatorStatusChange) for i in encoded["status_changes"]],
    )


def _decode_wasm_module(encoded: str) -> WasmModule:
    return decode(encoded, bytes)


def _decode_weight(encoded: str):
    return _decode_int(encoded)


_DECODERS_OF_PRIMITIVE_TYPES = {
    bool: _decode_bool,
    bytes: _decode_bytes,
    int: _decode_int,
    str: _decode_str,
}

_DECODERS_OF_PRIMITIVE_TYPES_ALIASED = {
    AccountID: _decode_account_id,
    Address: _decode_address,
    BlockHeight: _decode_block_height,
    Digest: _decode_digest,
    EraID: _decode_era_id,
    Gas: _decode_gas,
    GasPrice: _decode_gas_price,
    PublicKey: _decode_public_key,
    MerkleProof: _decode_merkle_proof,
    Motes: _decode_motes,
    Signature: _decode_signature,
    Weight: _decode_weight,
    WasmModule: _decode_wasm_module
}

_DECODERS_OF_COMPLEX_TYPES = {
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
    DeployArgument: _decode_deploy_argument,
    DeployExecutionInfo: _decode_deploy_execution_info,
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
    SeigniorageAllocation: _decode_seigniorage_allocation,
    Timestamp: _decode_timestamp,
    Transfer: _decode_transfer,
    URef: _decode_uref,
    URefAccessRights: _decode_uref_access_rights,
    ValidatorChanges: _decode_validator_changes,
    ValidatorStatusChange: _decode_validator_status_change,
}

_DECODERS = \
    _DECODERS_OF_PRIMITIVE_TYPES | \
    _DECODERS_OF_PRIMITIVE_TYPES_ALIASED | \
    _DECODERS_OF_COMPLEX_TYPES
