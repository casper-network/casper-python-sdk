from pycspr.codec.json.encoder_cl import encode_cl_value
from pycspr.codec.json.encoder_misc import encode_digest
from pycspr.codec.json.encoder_misc import encode_public_key
from pycspr.codec.json.encoder_misc import encode_timestamp
from pycspr.types import Deploy
from pycspr.types import DeployApproval
from pycspr.types import DeployHeader
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutionInfo
from pycspr.types import ExecutionInfo_ModuleBytes
from pycspr.types import ExecutionInfo_Transfer



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
        "signer": entity.signer.hex(),
        "signature": entity.signature.hex(),
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


def encode_execution_info(entity: ExecutionInfo) -> str:
    """Encodes execution information to be interpreted at a node.

    """
    def _encode_module_bytes() -> dict:
        return {
            "ModuleBytes": {
                "args": [encode_execution_argument(i) for i in entity.args],
                "module_bytes": entity.module_bytes.hex()
            }
        }


    def _encode_session_for_transfer() -> dict:
        return {
            "Transfer": {
                "args": [encode_execution_argument(i) for i in entity.args]            
            }
        }

    _ENCODERS = {
        ExecutionInfo_ModuleBytes: _encode_module_bytes,
        ExecutionInfo_Transfer: _encode_session_for_transfer,
    }

    return _ENCODERS[type(entity)]()
