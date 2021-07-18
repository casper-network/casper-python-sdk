from pycspr import crypto
from pycspr.serialisation.dictionary.decoder.cl import decode_cl_value
from pycspr.serialisation.dictionary.decoder.misc import decode_digest
from pycspr.serialisation.dictionary.decoder.misc import decode_public_key
from pycspr.serialisation.dictionary.decoder.misc import decode_signature
from pycspr.serialisation.dictionary.decoder.misc import decode_timestamp
from pycspr.types import Deploy
from pycspr.types import DeployApproval
from pycspr.types import DeployHeader
from pycspr.types import DeployTimeToLive
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutableDeployItem
from pycspr.types import ExecutableDeployItem_ModuleBytes
from pycspr.types import ExecutableDeployItem_StoredContractByHash
from pycspr.types import ExecutableDeployItem_StoredContractByHashVersioned
from pycspr.types import ExecutableDeployItem_StoredContractByName
from pycspr.types import ExecutableDeployItem_StoredContractByNameVersioned
from pycspr.types import ExecutableDeployItem_Transfer
from pycspr.types import PublicKey
from pycspr.utils import constants
from pycspr.utils import conversion



def decode_deploy(obj: dict) -> Deploy:
    """Maps a dictionary to a deploy.
    
    """
    return Deploy(
        approvals=[decode_deploy_approval(i) for i in obj["approvals"]],
        hash=decode_digest(obj["hash"]),
        header = decode_deploy_header(obj["header"]),
        payment = decode_executable_deploy_item(obj["payment"]),
        session = decode_executable_deploy_item(obj["session"])
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
        gas_price=obj["gas_price"],
        timestamp=decode_timestamp(obj["timestamp"]),
        ttl=decode_deploy_ttl(obj["ttl"])
    )


def decode_deploy_ttl(obj: str) -> DeployTimeToLive:
    """Maps a dictionary to a deploy ttl wrapper object.
    
    """
    as_milliseconds = conversion.humanized_time_interval_to_milliseconds(obj)
    if as_milliseconds > constants.DEPLOY_TTL_MS_MAX:
        raise ValueError(f"Invalid deploy ttl {obj} = {as_milliseconds} ms.  Maximum (ms) = {constants.DEPLOY_TTL_MS_MAX}")

    return DeployTimeToLive(
        as_milliseconds=as_milliseconds,
        humanized=obj
    )


def decode_executable_deploy_item(obj) -> ExecutableDeployItem:
    """Maps a dictionary to execution information.
    
    """
    def _decode_module_bytes():
        return ExecutableDeployItem_ModuleBytes(
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
        return ExecutableDeployItem_Transfer(
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


def decode_execution_argument(obj) -> ExecutionArgument:
    """Maps a dictionary to an execution argument.
    
    """
    return ExecutionArgument(
        name=obj[0], 
        value=decode_cl_value(obj[1])
        )
