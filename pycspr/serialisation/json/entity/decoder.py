import typing

from pycspr.factory import create_public_key_from_account_key
from pycspr.serialisation.json.cl_value import decode as decode_cl_value
from pycspr.types.node.rpc import Deploy
from pycspr.types.node.rpc import DeployHeader
from pycspr.types.node.rpc import DeployTimeToLive
from pycspr.types.node.rpc import DeployApproval
from pycspr.types.node.rpc import DeployArgument
from pycspr.types.node.rpc import DeployExecutableItem
from pycspr.types.node.rpc import DeployOfModuleBytes
from pycspr.types.node.rpc import DeployOfStoredContractByHash
from pycspr.types.node.rpc import DeployOfStoredContractByHashVersioned
from pycspr.types.node.rpc import DeployOfStoredContractByName
from pycspr.types.node.rpc import DeployOfStoredContractByNameVersioned
from pycspr.types.node.rpc import DeployOfTransfer
from pycspr.types.node.rpc import Timestamp
from pycspr.utils import constants
from pycspr.utils import conversion as convertor


def decode(encoded: dict, typedef: object) -> object:
    """Decoder: Domain entity <- JSON blob.

    :param encoded: A JSON compatible dictionary.
    :param typedef: Deploy related type definition.
    :returns: A deploy related type.

    """
    try:
        decoder = _DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json")
    else:
        return decoder(_get_parsed_json(typedef, encoded))


def _decode_deploy(encoded: dict) -> Deploy:
    return Deploy(
        approvals=[decode(i, DeployApproval) for i in encoded["approvals"]],
        hash=bytes.fromhex(encoded["hash"]),
        header=decode(encoded["header"], DeployHeader),
        payment=decode(encoded["payment"], DeployExecutableItem),
        session=decode(encoded["session"], DeployExecutableItem)
    )


def _decode_deploy_approval(encoded: dict) -> DeployApproval:
    return DeployApproval(
        signer=create_public_key_from_account_key(bytes.fromhex(encoded["signer"])),
        signature=bytes.fromhex(encoded["signature"]),
    )


def _decode_deploy_argument(encoded: dict) -> DeployArgument:
    return DeployArgument(name=encoded[0], value=decode_cl_value(encoded[1]))


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
    decode(encoded["ttl"], DeployTimeToLive)

    return DeployHeader(
        account=create_public_key_from_account_key(bytes.fromhex(encoded["account"])),
        body_hash=bytes.fromhex(encoded["body_hash"]),
        chain_name=encoded["chain_name"],
        dependencies=[],
        gas_price=encoded["gas_price"],
        timestamp=decode(encoded["timestamp"], Timestamp),
        ttl=decode(encoded["ttl"], DeployTimeToLive)
    )


def _decode_deploy_time_to_live(encoded: str) -> DeployTimeToLive:
    as_ms = convertor.humanized_time_interval_to_ms(encoded)
    if as_ms > constants.DEPLOY_TTL_MS_MAX:
        raise ValueError(f"Invalid deploy ttl. Maximum (ms)={constants.DEPLOY_TTL_MS_MAX}")

    return DeployTimeToLive(as_ms, encoded)


def _decode_module_bytes(encoded: dict) -> DeployOfModuleBytes:
    return DeployOfModuleBytes(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        module_bytes=bytes.fromhex(encoded["module_bytes"])
        )


def _decode_stored_contract_by_hash(encoded: dict) -> DeployOfStoredContractByHash:
    return DeployOfStoredContractByHash(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        entry_point=encoded["entry_point"],
        hash=bytes.fromhex(encoded["hash"])
    )


def _decode_stored_contract_by_hash_versioned(
    encoded: dict
) -> DeployOfStoredContractByHashVersioned:
    return DeployOfStoredContractByHashVersioned(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        entry_point=encoded["entry_point"],
        hash=bytes.fromhex(encoded["hash"]),
        version=encoded["version"]
    )


def _decode_stored_contract_by_name(encoded: dict) -> DeployOfStoredContractByName:
    return DeployOfStoredContractByName(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        entry_point=encoded["entry_point"],
        name=encoded["name"],
    )


def _decode_stored_contract_by_name_versioned(
    encoded: dict
) -> DeployOfStoredContractByNameVersioned:
    return DeployOfStoredContractByNameVersioned(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        entry_point=encoded["entry_point"],
        name=encoded["name"],
        version=encoded["version"]
    )


def _decode_timestamp(encoded: str) -> Timestamp:
    return Timestamp(convertor.iso_to_timestamp(encoded))


def _decode_transfer(encoded: dict) -> DeployOfTransfer:
    return DeployOfTransfer(
        args=[decode(i, DeployArgument) for i in encoded["args"]],
        )


def _get_parsed_json(typedef: object, encoded: typing.Union[dict, str]) -> dict:
    if typedef is DeployArgument:
        if isinstance(encoded[1]["bytes"], str):
            encoded[1]["bytes"] = bytes.fromhex(encoded[1]["bytes"])
    elif typedef is DeployOfModuleBytes:
        return encoded["ModuleBytes"]
    elif typedef is DeployOfStoredContractByHash:
        return encoded["StoredContractByHash"]
    elif typedef is DeployOfStoredContractByHashVersioned:
        return encoded["StoredContractByHashVersioned"]
    elif typedef is DeployOfStoredContractByName:
        return encoded["StoredContractByName"]
    elif typedef is DeployOfStoredContractByNameVersioned:
        return encoded["StoredContractByNameVersioned"]
    elif typedef is DeployOfTransfer:
        return encoded["Transfer"]
    return encoded


_DECODERS = {
    Deploy: _decode_deploy,
    DeployApproval: _decode_deploy_approval,
    DeployArgument: _decode_deploy_argument,
    DeployExecutableItem: _decode_deploy_executable_item,
    DeployHeader: _decode_deploy_header,
    DeployOfModuleBytes: _decode_module_bytes,
    DeployOfStoredContractByHash: _decode_stored_contract_by_hash,
    DeployOfStoredContractByHashVersioned: _decode_stored_contract_by_hash_versioned,
    DeployOfStoredContractByName: _decode_stored_contract_by_name,
    DeployOfStoredContractByNameVersioned: _decode_stored_contract_by_name_versioned,
    DeployOfTransfer: _decode_transfer,
    DeployTimeToLive: _decode_deploy_time_to_live,
    Timestamp: _decode_timestamp,
}
