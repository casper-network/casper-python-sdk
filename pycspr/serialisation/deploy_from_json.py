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
    print(typedef)
    obj = _get_parsed_json(typedef, obj)

    if typedef is Deploy:
        return Deploy(
            approvals=[decode(DeployApproval, i) for i in obj["approvals"]],
            hash=bytes.fromhex(obj["hash"]),
            header=decode(DeployHeader, obj["header"]),
            payment=decode(DeployExecutableItem, obj["payment"]),
            session=decode(DeployExecutableItem, obj["session"])
        )

    elif typedef is DeployApproval:
        return DeployApproval(
            signer=create_public_key_from_account_key(bytes.fromhex(obj["signer"])),
            signature=bytes.fromhex(obj["signature"]),
        )

    elif typedef is DeployArgument:
        return DeployArgument(
            name=obj[0],
            value=cl_value_from_json(obj[1])
            )

    elif typedef is DeployExecutableItem:
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

    elif typedef is DeployHeader:
        return DeployHeader(
            account_public_key=create_public_key_from_account_key(bytes.fromhex(obj["account"])),
            body_hash=bytes.fromhex(obj["body_hash"]),
            chain_name=obj["chain_name"],
            dependencies=[],
            gas_price=obj["gas_price"],
            timestamp=Timestamp.from_string(obj["timestamp"]),
            ttl=DeployTimeToLive.from_string(obj["ttl"])
        )

    elif typedef is ModuleBytes:
        return ModuleBytes(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            module_bytes=bytes.fromhex(obj["module_bytes"])
            )

    elif typedef is StoredContractByHash:
        return StoredContractByHash(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            hash=bytes.fromhex(obj["hash"])
        )

    elif typedef is StoredContractByHashVersioned:
        return StoredContractByHashVersioned(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            hash=bytes.fromhex(obj["hash"]),
            version=obj["version"]
        )

    elif typedef is StoredContractByName:
        return StoredContractByName(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            name=obj["name"],
        )

    elif typedef is StoredContractByNameVersioned:
        return StoredContractByNameVersioned(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            name=obj["name"],
            version=obj["version"]
        )

    elif typedef is Transfer:
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
