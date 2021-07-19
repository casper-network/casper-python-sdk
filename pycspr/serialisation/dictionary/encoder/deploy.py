from pycspr import crypto

from pycspr.serialisation.dictionary.encoder.cl import encode_cl_value
from pycspr.serialisation.dictionary.encoder.misc import encode_account_key
from pycspr.serialisation.dictionary.encoder.misc import encode_digest
from pycspr.serialisation.dictionary.encoder.misc import encode_public_key
from pycspr.serialisation.dictionary.encoder.misc import encode_signature
from pycspr.serialisation.dictionary.encoder.misc import encode_timestamp
from pycspr.types import Deploy
from pycspr.types import DeployApproval
from pycspr.types import DeployHeader
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutableDeployItem
from pycspr.types import ExecutableDeployItem_ModuleBytes
from pycspr.types import ExecutableDeployItem_StoredContractByHash
from pycspr.types import ExecutableDeployItem_StoredContractByHashVersioned
from pycspr.types import ExecutableDeployItem_StoredContractByName
from pycspr.types import ExecutableDeployItem_StoredContractByNameVersioned
from pycspr.types import ExecutableDeployItem_Transfer



def encode_deploy(entity: Deploy) -> dict:
    """Encodes a deploy.

    """
    return {
        "approvals": [encode_deploy_approval(i) for i in entity.approvals],
        "hash": encode_digest(entity.hash),
        "header": encode_deploy_header(entity.header),
        "payment": encode_execution_info(entity.payment),
        "session": encode_execution_info(entity.session)
    }


def encode_deploy_approval(entity: DeployApproval) -> dict:
    """Encodes a deploy approval.

    """
    return {
        "signature": encode_signature(entity.signature),
        "signer": encode_account_key(entity.signer)
    }


def encode_deploy_header(entity: DeployHeader) -> dict:
    """Encodes a deploy header.

    """
    return {
        "account": encode_public_key(entity.accountPublicKey),
        "body_hash": encode_digest(entity.body_hash),
        "chain_name": entity.chain_name,
        "dependencies": entity.dependencies,
        "gas_price": entity.gas_price,
        "timestamp": encode_timestamp(entity.timestamp),
        "ttl": entity.ttl.humanized
    }


def encode_execution_argument(entity: ExecutionArgument) -> dict:
    """Encodes an execution argument.

    """
    return [
        entity.name,
        encode_cl_value(entity.value)
    ]


def encode_execution_info(entity: ExecutableDeployItem) -> dict:
    """Encodes execution information to be interpreted at a node.

    """
    def _encode_module_bytes() -> dict:
        return {
            "ModuleBytes": {
                "args": [encode_execution_argument(i) for i in entity.args],
                "module_bytes": entity.module_bytes.hex()
            }
        }

    def _encode_stored_contract_by_hash() -> dict:
        raise NotImplementedError()

    def _encode_stored_contract_by_hash_versioned() -> dict:
        raise NotImplementedError()

    def _encode_stored_contract_by_name() -> dict:
        raise NotImplementedError()

    def _encode_stored_contract_by_name_versioned() -> dict:
        raise NotImplementedError()

    def _encode_session_for_transfer() -> dict:
        return {
            "Transfer": {
                "args": [encode_execution_argument(i) for i in entity.args]            
            }
        }

    _ENCODERS = {
        ExecutableDeployItem_ModuleBytes: _encode_module_bytes,
        ExecutableDeployItem_StoredContractByHash: _encode_stored_contract_by_hash,
        ExecutableDeployItem_StoredContractByHashVersioned: _encode_stored_contract_by_hash_versioned,
        ExecutableDeployItem_StoredContractByName: _encode_stored_contract_by_name,
        ExecutableDeployItem_StoredContractByNameVersioned: _encode_stored_contract_by_name_versioned,
        ExecutableDeployItem_Transfer: _encode_session_for_transfer,
    }

    return _ENCODERS[type(entity)]()
