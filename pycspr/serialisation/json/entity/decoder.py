from pycspr.factory import create_public_key_from_account_key
from pycspr.serialisation.json.cl_value import decode as decode_cl_value
from pycspr.types.api.rpc import Deploy
from pycspr.types.api.rpc import DeployHeader
from pycspr.types.api.rpc import DeployTimeToLive
from pycspr.types.api.rpc import DeployApproval
from pycspr.types.api.rpc import DeployArgument
from pycspr.types.api.rpc import DeployExecutableItem
from pycspr.types.api.rpc import DeployOfModuleBytes
from pycspr.types.api.rpc import DeployOfStoredContractByHash
from pycspr.types.api.rpc import DeployOfStoredContractByHashVersioned
from pycspr.types.api.rpc import DeployOfStoredContractByName
from pycspr.types.api.rpc import DeployOfStoredContractByNameVersioned
from pycspr.types.api.rpc import DeployOfTransfer
from pycspr.types.api.rpc import Timestamp
from pycspr.utils import conversion as convertor


def decode(obj: dict, typedef: object) -> object:
    """Decoder: Domain entity <- JSON blob.

    :param obj: A JSON compatible dictionary.
    :param typedef: Deploy related type definition.
    :returns: A deploy related type.

    """
    try:
        decoder = _DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json")
    else:
        return decoder(_get_parsed_json(typedef, obj))


def _decode_deploy(obj: dict) -> Deploy:
    return Deploy(
        approvals=[decode(i, DeployApproval) for i in obj["approvals"]],
        hash=bytes.fromhex(obj["hash"]),
        header=decode(obj["header"], DeployHeader),
        payment=decode(obj["payment"], DeployExecutableItem),
        session=decode(obj["session"], DeployExecutableItem)
    )


def _decode_deploy_approval(obj: dict) -> DeployApproval:
    return DeployApproval(
        signer=create_public_key_from_account_key(bytes.fromhex(obj["signer"])),
        signature=bytes.fromhex(obj["signature"]),
    )


def _decode_deploy_argument(obj: dict) -> DeployArgument:
    return DeployArgument(name=obj[0], value=decode_cl_value(obj[1]))


def _decode_deploy_executable_item(obj: dict) -> DeployExecutableItem:
    if "ModuleBytes" in obj:
        return decode(obj, DeployOfModuleBytes)
    elif "StoredContractByHash" in obj:
        return decode(obj, DeployOfStoredContractByHash)
    elif "StoredVersionedContractByHash" in obj:
        return decode(obj, DeployOfStoredContractByHashVersioned)
    elif "StoredContractByName" in obj:
        return decode(obj, DeployOfStoredContractByName)
    elif "StoredVersionedContractByName" in obj:
        return decode(obj, DeployOfStoredContractByNameVersioned)
    elif "Transfer" in obj:
        return decode(obj, DeployOfTransfer)
    else:
        raise NotImplementedError("Unsupported DeployExecutableItem variant")


def _decode_deploy_header(obj: dict) -> DeployHeader:
    return DeployHeader(
        account=create_public_key_from_account_key(bytes.fromhex(obj["account"])),
        body_hash=bytes.fromhex(obj["body_hash"]),
        chain_name=obj["chain_name"],
        dependencies=[],
        gas_price=obj["gas_price"],
        timestamp=Timestamp(convertor.iso_to_timestamp(obj["timestamp"])),
        ttl=DeployTimeToLive.from_string(obj["ttl"])
    )


def _decode_module_bytes(obj: dict) -> DeployOfModuleBytes:
    return DeployOfModuleBytes(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        module_bytes=bytes.fromhex(obj["module_bytes"])
        )


def _decode_stored_contract_by_hash(obj: dict) -> DeployOfStoredContractByHash:
    return DeployOfStoredContractByHash(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        entry_point=obj["entry_point"],
        hash=bytes.fromhex(obj["hash"])
    )


def _decode_stored_contract_by_hash_versioned(
    obj: dict
) -> DeployOfStoredContractByHashVersioned:
    return DeployOfStoredContractByHashVersioned(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        entry_point=obj["entry_point"],
        hash=bytes.fromhex(obj["hash"]),
        version=obj["version"]
    )


def _decode_stored_contract_by_name(obj: dict) -> DeployOfStoredContractByName:
    return DeployOfStoredContractByName(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        entry_point=obj["entry_point"],
        name=obj["name"],
    )


def _decode_stored_contract_by_name_versioned(
    obj: dict
) -> DeployOfStoredContractByNameVersioned:
    return DeployOfStoredContractByNameVersioned(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        entry_point=obj["entry_point"],
        name=obj["name"],
        version=obj["version"]
    )


def _decode_transfer(obj: dict) -> DeployOfTransfer:
    return DeployOfTransfer(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        )


def _get_parsed_json(typedef: object, obj: dict) -> dict:
    if typedef is DeployArgument:
        if isinstance(obj[1]["bytes"], str):
            obj[1]["bytes"] = bytes.fromhex(obj[1]["bytes"])
    elif typedef is DeployOfModuleBytes:
        return obj["ModuleBytes"]
    elif typedef is DeployOfStoredContractByHash:
        return obj["StoredContractByHash"]
    elif typedef is DeployOfStoredContractByHashVersioned:
        return obj["StoredContractByHashVersioned"]
    elif typedef is DeployOfStoredContractByName:
        return obj["StoredContractByName"]
    elif typedef is DeployOfStoredContractByNameVersioned:
        return obj["StoredContractByNameVersioned"]
    elif typedef is DeployOfTransfer:
        return obj["Transfer"]
    return obj


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
    DeployOfTransfer: _decode_transfer
}
