import datetime

from pycspr.serialisation.json.encoder.cl import encode_cl_value
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
from pycspr.types import PublicKey
from pycspr.types import Timestamp


def encode_deploy(entity: Deploy) -> dict:
    """Encodes a deploy.

    """
    return {
        "approvals": [encode_deploy_approval(i) for i in entity.approvals],
        "hash": entity.hash.hex(),
        "header": encode_deploy_header(entity.header),
        "payment": encode_execution_info(entity.payment),
        "session": encode_execution_info(entity.session)
    }


def encode_deploy_approval(entity: DeployApproval) -> dict:
    """Encodes a deploy approval.

    """
    return {
        "signature": entity.signature.hex(),
        "signer": entity.signer.hex()
    }


def encode_deploy_header(entity: DeployHeader) -> dict:
    """Encodes a deploy header.

    """
    return {
        "account": encode_public_key(entity.account_public_key),
        "body_hash": entity.body_hash.hex(),
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
        return {
            "StoredContractByHash": {
                "args": [encode_execution_argument(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "hash": entity.hash.hex()
            }
        }

    def _encode_stored_contract_by_hash_versioned() -> dict:
        return {
            "StoredContractByHashVersioned": {
                "args": [encode_execution_argument(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "hash": entity.hash.hex(),
                "version": entity.version
            }
        }

    def _encode_stored_contract_by_name() -> dict:
        return {
            "StoredContractByName": {
                "args": [encode_execution_argument(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "name": entity.name
            }
        }

    def _encode_stored_contract_by_name_versioned() -> dict:
        return {
            "StoredContractByNameVersioned": {
                "args": [encode_execution_argument(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "name": entity.name,
                "version": entity.version
            }
        }

    def _encode_session_for_transfer() -> dict:
        return {
            "Transfer": {
                "args": [encode_execution_argument(i) for i in entity.args]
            }
        }

    _ENCODERS = {
        ExecutableDeployItem_ModuleBytes:
            _encode_module_bytes,
        ExecutableDeployItem_StoredContractByHash:
            _encode_stored_contract_by_hash,
        ExecutableDeployItem_StoredContractByHashVersioned:
            _encode_stored_contract_by_hash_versioned,
        ExecutableDeployItem_StoredContractByName:
            _encode_stored_contract_by_name,
        ExecutableDeployItem_StoredContractByNameVersioned:
            _encode_stored_contract_by_name_versioned,
        ExecutableDeployItem_Transfer:
            _encode_session_for_transfer,
    }

    return _ENCODERS[type(entity)]()


def encode_public_key(entity: PublicKey) -> str:
    """Encodes a public key.

    """
    return entity.account_key.hex()


def encode_timestamp(entity: Timestamp) -> str:
    """Encodes a millisecond precise timestamp.

    """
    # Node understands ISO millisecond precise timestamps.
    as_ts_3_decimal_places = round(entity, 3)
    as_datetime = datetime.datetime.fromtimestamp(
        as_ts_3_decimal_places,
        tz=datetime.timezone.utc
        )
    as_iso = as_datetime.isoformat()

    return f"{as_iso[:-9]}Z"
