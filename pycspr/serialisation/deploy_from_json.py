from pycspr.factory import create_public_key_from_account_key
from pycspr.serialisation.cl_value_from_json import decode as cl_value_from_json
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


def decode(typedef: object, obj: dict) -> object:
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
        approvals=[decode(DeployApproval, i) for i in obj["approvals"]],
        hash=bytes.fromhex(obj["hash"]),
        header=decode(DeployHeader, obj["header"]),
        payment=decode(DeployExecutableItem, obj["payment"]),
        session=decode(DeployExecutableItem, obj["session"])
    )


def _decode_deploy_approval(obj: dict) -> DeployApproval:
    return DeployApproval(
        signer=create_public_key_from_account_key(bytes.fromhex(obj["signer"])),
        signature=bytes.fromhex(obj["signature"]),
    )


def _decode_deploy_argument(obj: dict) -> DeployArgument:
    return DeployArgument(
        name=obj[0],
        value=cl_value_from_json(obj[1])
        )


def _decode_deploy_executable_item(obj: dict) -> DeployExecutableItem:
    if "ModuleBytes" in obj:
        return decode(ModuleBytes, obj)
    elif "StoredContractByHash" in obj:
        return decode(StoredContractByHash, obj)
    elif "StoredVersionedContractByHash" in obj:
        return decode(StoredContractByHashVersioned, obj)
    elif "StoredContractByName" in obj:
        return decode(StoredContractByName, obj)
    elif "StoredVersionedContractByName" in obj:
        return decode(StoredContractByNameVersioned, obj)
    elif "Transfer" in obj:
        return decode(Transfer, obj)
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
        args=[decode(DeployArgument, i) for i in obj["args"]],
        module_bytes=bytes.fromhex(obj["module_bytes"])
        )


def _decode_stored_contract_by_hash(obj: dict) -> StoredContractByHash:
    return StoredContractByHash(
        args=[decode(DeployArgument, i) for i in obj["args"]],
        entry_point=obj["entry_point"],
        hash=bytes.fromhex(obj["hash"])
    )


def _decode_stored_contract_by_hash_versioned(obj: dict) -> StoredContractByHashVersioned:
    return StoredContractByHashVersioned(
        args=[decode(DeployArgument, i) for i in obj["args"]],
        entry_point=obj["entry_point"],
        hash=bytes.fromhex(obj["hash"]),
        version=obj["version"]
    )


def _decode_stored_contract_by_name(obj: dict) -> StoredContractByName:
    return StoredContractByName(
        args=[decode(DeployArgument, i) for i in obj["args"]],
        entry_point=obj["entry_point"],
        name=obj["name"],
    )


def _decode_stored_contract_by_name_versioned(obj: dict) -> StoredContractByNameVersioned:
    return StoredContractByNameVersioned(
        args=[decode(DeployArgument, i) for i in obj["args"]],
        entry_point=obj["entry_point"],
        name=obj["name"],
        version=obj["version"]
    )


def _decode_transfer(obj: dict) -> Transfer:
    return Transfer(
        args=[decode(DeployArgument, i) for i in obj["args"]],
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