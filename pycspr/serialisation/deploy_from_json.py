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
from pycspr.types.other import Timestamp


def decode(typedef: object, obj: dict) -> object:
    obj = _parse_json(typedef, obj)

    if typedef is Deploy:
        return Deploy(
            approvals=[decode(DeployApproval, i) for i in obj["approvals"]],
            hash=bytes.fromhex(obj["hash"]),
            header=decode(DeployHeader, obj["header"]),
            payment=decode(DeployExecutableItem, obj["payment"]),
            session=decode(DeployExecutableItem, obj["session"])
        )

    if typedef is DeployApproval:
        return DeployApproval(
            signer=create_public_key_from_account_key(bytes.fromhex(obj["signer"])),
            signature=bytes.fromhex(obj["signature"]),
        )

    if typedef is DeployArgument:
        return DeployArgument(
            name=obj[0],
            value=cl_value_from_json(obj[1])
            )

    if typedef is DeployExecutableItem:
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

    if typedef is DeployHeader:
        return DeployHeader(
            account_public_key=create_public_key_from_account_key(bytes.fromhex(obj["account"])),
            body_hash=bytes.fromhex(obj["body_hash"]),
            chain_name=obj["chain_name"],
            dependencies=[],
            gas_price=obj["gas_price"],
            timestamp=Timestamp.from_string(obj["timestamp"]),
            ttl=DeployTimeToLive.from_string(obj["ttl"])
        )

    if typedef is ModuleBytes:
        return ModuleBytes(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            module_bytes=bytes.fromhex(obj["module_bytes"])
            )

    if typedef is StoredContractByHash:
        return StoredContractByHash(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            hash=bytes.fromhex(obj["hash"])
        )

    if typedef is StoredContractByHashVersioned:
        return StoredContractByHashVersioned(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            hash=bytes.fromhex(obj["hash"]),
            version=obj["version"]
        )

    if typedef is StoredContractByName:
        return StoredContractByName(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            name=obj["name"],
        )

    if typedef is StoredContractByNameVersioned:
        return StoredContractByNameVersioned(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            name=obj["name"],
            version=obj["version"]
        )

    if typedef is Transfer:
        return Transfer(
            args=[decode(DeployArgument, i) for i in obj["args"]],
            )


def _parse_json(typedef: object, obj: dict):
    if typedef is DeployArgument:
        if isinstance(obj[1]["bytes"], str):
            obj[1]["bytes"] = bytes.fromhex(obj[1]["bytes"])

    if typedef is ModuleBytes:
        return obj["ModuleBytes"]

    if typedef is StoredContractByHash:
        return obj["StoredContractByHash"]

    if typedef is StoredContractByHashVersioned:
        return obj["StoredContractByHashVersioned"]

    if typedef is StoredContractByName:
        return obj["StoredContractByName"]

    if typedef is StoredContractByNameVersioned:
        return obj["StoredContractByNameVersioned"]

    if typedef is Transfer:
        return obj["Transfer"]

    return obj
