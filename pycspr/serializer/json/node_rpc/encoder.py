import typing

from pycspr.crypto import checksummer
from pycspr.serializer.json.cl_value import encode as encode_cl_value
from pycspr.types.node.rpc import Deploy
from pycspr.types.node.rpc import DeployHeader
from pycspr.types.cl import CLV_Value
from pycspr.types.node.rpc import DeployApproval
from pycspr.types.node.rpc import DeployArgument
from pycspr.types.node.rpc import DeployOfModuleBytes
from pycspr.types.node.rpc import DeployOfStoredContractByHash
from pycspr.types.node.rpc import DeployOfStoredContractByHashVersioned
from pycspr.types.node.rpc import DeployOfStoredContractByName
from pycspr.types.node.rpc import DeployOfStoredContractByNameVersioned
from pycspr.types.node.rpc import DeployOfTransfer
from pycspr.utils import convertor


def encode(entity: object) -> dict:
    """Encoder: Domain entity instance -> JSON blob.

    :param entity: A deploy related type instance to be encoded.
    :returns: A JSON compatible dictionary.

    """
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Unknown deploy type: {entity}")
    else:
        return encoder(entity)


def _encode_deploy(entity: Deploy) -> dict:
    return {
        "approvals": [encode(i) for i in entity.approvals],
        "hash": checksummer.encode_digest(entity.hash),
        "header": encode(entity.header),
        "payment": encode(entity.payment),
        "session": encode(entity.session)
    }


def _encode_deploy_approval(entity: DeployApproval) -> dict:
    return {
        "signature": checksummer.encode_signature(entity.signature),
        "signer": checksummer.encode_account_key(entity.signer.account_key)
    }


def _encode_deploy_argument(entity: DeployArgument) -> typing.Tuple[str, CLV_Value]:
    return (entity.name, encode_cl_value(entity.value))


def _encode_deploy_header(entity: DeployHeader) -> dict:
    return {
        "account": checksummer.encode_account_key(entity.account.account_key),
        "body_hash": checksummer.encode_digest(entity.body_hash),
        "chain_name": entity.chain_name,
        "dependencies": entity.dependencies,
        "gas_price": entity.gas_price,
        "timestamp": convertor.iso_datetime_from_timestamp(entity.timestamp.value),
        "ttl": entity.ttl.humanized
    }


def _encode_module_bytes(entity: DeployOfModuleBytes) -> dict:
    return {
        "ModuleBytes": {
            "args": [encode(i) for i in entity.arguments],
            "module_bytes": checksummer.encode_bytes(entity.module_bytes)
        }
    }


def _encode_stored_contract_by_hash(entity: DeployOfStoredContractByHash) -> dict:
    return {
        "StoredContractByHash": {
            "args": [encode(i) for i in entity.arguments],
            "entry_point": entity.entry_point,
            "hash": checksummer.encode_bytes(entity.hash)
        }
    }


def _encode_stored_contract_by_hash_versioned(
    entity: DeployOfStoredContractByHashVersioned
) -> dict:
    return {
        "StoredVersionedContractByHash": {
            "args": [encode(i) for i in entity.arguments],
            "entry_point": entity.entry_point,
            "hash": checksummer.encode_bytes(entity.hash),
            "version": entity.version
        }
    }


def _encode_stored_contract_by_name(entity: DeployOfStoredContractByName) -> dict:
    return {
        "StoredContractByName": {
            "args": [encode(i) for i in entity.arguments],
            "entry_point": entity.entry_point,
            "name": entity.name
        }
    }


def _encode_stored_contract_by_name_versioned(
    entity: DeployOfStoredContractByNameVersioned
) -> dict:
    return {
        "StoredVersionedContractByName": {
            "args": [encode(i) for i in entity.arguments],
            "entry_point": entity.entry_point,
            "name": entity.name,
            "version": entity.version
        }
    }


def _encode_transfer(entity: DeployOfTransfer) -> dict:
    return {
        "Transfer": {
            "args": [encode(i) for i in entity.arguments],
        }
    }


_ENCODERS = {
    Deploy: _encode_deploy,
    DeployApproval: _encode_deploy_approval,
    DeployArgument: _encode_deploy_argument,
    DeployHeader: _encode_deploy_header,
    DeployOfModuleBytes: _encode_module_bytes,
    DeployOfStoredContractByHash: _encode_stored_contract_by_hash,
    DeployOfStoredContractByHashVersioned: _encode_stored_contract_by_hash_versioned,
    DeployOfStoredContractByName: _encode_stored_contract_by_name,
    DeployOfStoredContractByNameVersioned: _encode_stored_contract_by_name_versioned,
    DeployOfTransfer: _encode_transfer,
}
