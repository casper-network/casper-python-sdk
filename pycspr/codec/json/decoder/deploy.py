from pycspr import crypto
from pycspr.codec.json.decoder.cl import decode_cl_value
from pycspr.codec.json.decoder.misc import decode_digest
from pycspr.codec.json.decoder.misc import decode_public_key
from pycspr.codec.json.decoder.misc import decode_signature
from pycspr.codec.json.decoder.misc import decode_timestamp
from pycspr.types import Deploy
from pycspr.types import DeployApproval
from pycspr.types import DeployHeader
from pycspr.types import DeployTimeToLive
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutionInfo
from pycspr.types import ExecutionInfo_ModuleBytes
from pycspr.types import ExecutionInfo_StoredContractByHash
from pycspr.types import ExecutionInfo_StoredContractByHashVersioned
from pycspr.types import ExecutionInfo_StoredContractByName
from pycspr.types import ExecutionInfo_StoredContractByNameVersioned
from pycspr.types import ExecutionInfo_Transfer
from pycspr.types import PublicKey



def decode_deploy(obj: dict) -> Deploy:
    """Maps a dictionary to a deploy.
    
    """
    return Deploy(
        approvals=[decode_deploy_approval(i) for i in obj["approvals"]],
        hash=decode_digest(obj["hash"]),
        header = decode_deploy_header(obj["header"]),
        payment = decode_execution_info(obj["payment"]),
        session = decode_execution_info(obj["session"])
    )


def decode_deploy_approval(obj: dict) -> DeployApproval:    
    """Maps a dictionary to a deploy approval.
    
    """
    return DeployApproval(
        signer=decode_public_key(obj["signer"]),
        signature=decode_signature(obj["signature"]),
    )


def decode_deploy_header(obj: dict) -> DeployHeader:
    """Maps a dictionary to a deploy header.
    
    """
    return DeployHeader(
        accountPublicKey=decode_public_key(obj["account"]),
        body_hash=decode_digest(obj["body_hash"]),
        chain_name=obj["chain_name"],
        dependencies=[],
        gas_price=obj["chain_name"],
        timestamp=decode_timestamp(obj["timestamp"]),
        ttl=decode_deploy_ttl(obj["ttl"])
    )


def decode_deploy_ttl(obj: str) -> DeployTimeToLive:
    """Maps a dictionary to a deploy ttl wrapper object.
    
    """
    return DeployTimeToLive(
        as_milliseconds=1 * 24 * 60 * 60 * 1000,
        humanized=obj
    )


def decode_execution_argument(obj) -> ExecutionArgument:
    """Maps a dictionary to an execution argument.
    
    """
    return ExecutionArgument(
        name=obj[0], 
        value=decode_cl_value(obj[1])
        )


def decode_execution_info(obj) -> ExecutionInfo:
    """Maps a dictionary to execution information.
    
    """
    def _decode_module_bytes():
        return ExecutionInfo_ModuleBytes(
            args=[decode_execution_argument(i) for i in obj["ModuleBytes"]["args"]],
            module_bytes=bytes.fromhex(obj["ModuleBytes"]["module_bytes"])
            )        

    def _decode_stored_contract_by_hash() -> dict:
        raise NotImplementedError()

    def _decode_stored_contract_by_hash_versioned() -> dict:
        raise NotImplementedError()

    def _decode_stored_contract_by_name() -> dict:
        raise NotImplementedError()

    def _decode_stored_contract_by_name_versioned() -> dict:
        raise NotImplementedError()

    def _decode_session_for_transfer():
        return ExecutionInfo_Transfer(
            args=[decode_execution_argument(i) for i in obj["Transfer"]["args"]],
            )  

    if "ModuleBytes" in obj:
        return _decode_module_bytes()
    elif "StoredContractByHash" in obj:
        return _decode_stored_contract_by_hash()
    elif "StoredVersionedContractByHash" in obj:
        return _decode_stored_contract_by_hash_versioned()
    elif "StoredContractByName" in obj:
        return _decode_stored_contract_by_name()
    elif "StoredVersionedContractByName" in obj:
        return _decode_stored_contract_by_name_versioned()
    elif "Transfer" in obj:
        return _decode_session_for_transfer()
    else:
        raise NotImplementError("Unsupported execution information variant")
