from pycspr.factory import create_public_key_from_account_key
from pycspr.serialisation.json.cl_value import decode as decode_cl_value
from pycspr.types.deploys import Deploy
from pycspr.types.deploys import DeployApproval
from pycspr.types.deploys import DeployArgument
from pycspr.types.deploys import DeployExecutableItem
from pycspr.types.deploys import DeployHeader
from pycspr.types.deploys import DeployTimeToLive
from pycspr.types.deploys import ModuleBytes
from pycspr.types.deploys import StoredContractByHash
from pycspr.types.deploys import StoredContractByHashVersioned
from pycspr.types.deploys import StoredContractByName
from pycspr.types.deploys import StoredContractByNameVersioned
from pycspr.types.deploys import Transfer
from pycspr.types import Timestamp


def decode(obj: dict, typedef: object) -> object:
    """Decodes a deploy related type from a JSON object.

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
        return decode(obj, ModuleBytes)
    elif "StoredContractByHash" in obj:
        return decode(obj, StoredContractByHash)
    elif "StoredVersionedContractByHash" in obj:
        return decode(obj, StoredContractByHashVersioned)
    elif "StoredContractByName" in obj:
        return decode(obj, StoredContractByName)
    elif "StoredVersionedContractByName" in obj:
        return decode(obj, StoredContractByNameVersioned)
    elif "Transfer" in obj:
        return decode(obj, Transfer)
    else:
        raise NotImplementedError("Unsupported DeployExecutableItem variant")


def _decode_deploy_header(obj: dict) -> DeployHeader:
    return DeployHeader(
        account_public_key=create_public_key_from_account_key(bytes.fromhex(obj["account"])),
        body_hash=bytes.fromhex(obj["body_hash"]),
        chain_name=obj["chain_name"],
        dependencies=[],
        gas_price=obj["gas_price"],
        timestamp=Timestamp.from_string(obj["timestamp"]),
        ttl=DeployTimeToLive.from_string(obj["ttl"])
    )


def _decode_module_bytes(obj: dict) -> ModuleBytes:
    return ModuleBytes(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        module_bytes=bytes.fromhex(obj["module_bytes"])
        )


def _decode_stored_contract_by_hash(obj: dict) -> StoredContractByHash:
    return StoredContractByHash(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        entry_point=obj["entry_point"],
        hash=bytes.fromhex(obj["hash"])
    )


def _decode_stored_contract_by_hash_versioned(obj: dict) -> StoredContractByHashVersioned:
    return StoredContractByHashVersioned(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        entry_point=obj["entry_point"],
        hash=bytes.fromhex(obj["hash"]),
        version=obj["version"]
    )


def _decode_stored_contract_by_name(obj: dict) -> StoredContractByName:
    return StoredContractByName(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        entry_point=obj["entry_point"],
        name=obj["name"],
    )


def _decode_stored_contract_by_name_versioned(obj: dict) -> StoredContractByNameVersioned:
    return StoredContractByNameVersioned(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        entry_point=obj["entry_point"],
        name=obj["name"],
        version=obj["version"]
    )


def _decode_transfer(obj: dict) -> Transfer:
    return Transfer(
        args=[decode(i, DeployArgument) for i in obj["args"]],
        )


def _get_parsed_json(typedef: object, obj: dict) -> dict:
    if typedef is DeployArgument:
        if isinstance(obj[1]["bytes"], str):
            obj[1]["bytes"] = bytes.fromhex(obj[1]["bytes"])
    elif typedef is ModuleBytes:
        return obj["ModuleBytes"]
    elif typedef is StoredContractByHash:
        return obj["StoredContractByHash"]
    elif typedef is StoredContractByHashVersioned:
        return obj["StoredContractByHashVersioned"]
    elif typedef is StoredContractByName:
        return obj["StoredContractByName"]
    elif typedef is StoredContractByNameVersioned:
        return obj["StoredContractByNameVersioned"]
    elif typedef is Transfer:
        return obj["Transfer"]
    return obj


_DECODERS = {
    Deploy: _decode_deploy,
    DeployApproval: _decode_deploy_approval,
    DeployArgument: _decode_deploy_argument,
    DeployExecutableItem: _decode_deploy_executable_item,
    DeployHeader: _decode_deploy_header,
    ModuleBytes: _decode_module_bytes,
    StoredContractByHash: _decode_stored_contract_by_hash,
    StoredContractByHashVersioned: _decode_stored_contract_by_hash_versioned,
    StoredContractByName: _decode_stored_contract_by_name,
    StoredContractByNameVersioned: _decode_stored_contract_by_name_versioned,
    Transfer: _decode_transfer
}
