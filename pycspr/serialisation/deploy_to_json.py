from pycspr.crypto import cl_checksum
from pycspr.serialisation.cl_value_to_json import encode as cl_value_to_json
from pycspr.types.deploys import Deploy
from pycspr.types.deploys import DeployApproval
from pycspr.types.deploys import DeployArgument
from pycspr.types.deploys import DeployHeader
from pycspr.types.deploys import ModuleBytes
from pycspr.types.deploys import StoredContractByHash
from pycspr.types.deploys import StoredContractByHashVersioned
from pycspr.types.deploys import StoredContractByName
from pycspr.types.deploys import StoredContractByNameVersioned
from pycspr.types.deploys import Transfer


def encode(entity: object) -> dict:
    """Encodes a deploy related type instance as a JSON compatible dictionary.

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
        "hash": cl_checksum.encode_digest(entity.hash),
        "header": encode(entity.header),
        "payment": encode(entity.payment),
        "session": encode(entity.session)
    }


def _encode_deploy_approval(entity: DeployApproval) -> dict:
    return {
        "signature": cl_checksum.encode_signature(entity.signature),
        "signer": cl_checksum.encode_account_key(entity.signer.account_key)
    }


def _encode_deploy_argument(entity: DeployArgument) -> dict:
    return [
        entity.name,
        cl_value_to_json(entity.value)
    ]


def _encode_deploy_header(entity: DeployHeader) -> dict:
    return {
        "account": cl_checksum.encode_account_key(entity.account_public_key.account_key),
        "body_hash": cl_checksum.encode_digest(entity.body_hash),
        "chain_name": entity.chain_name,
        "dependencies": entity.dependencies,
        "gas_price": entity.gas_price,
        "timestamp": entity.timestamp.to_string(),
        "ttl": entity.ttl.to_string()
    }


def _encode_module_bytes(entity: ModuleBytes) -> dict:
    return {
        "ModuleBytes": {
            "args": [encode(i) for i in entity.arguments],
            "module_bytes": cl_checksum.encode(entity.module_bytes)
        }
    }


def _encode_stored_contract_by_hash(entity: StoredContractByHash) -> dict:
    return {
        "StoredContractByHash": {
            "args": [encode(i) for i in entity.arguments],
            "entry_point": entity.entry_point,
            "hash": cl_checksum.encode(entity.hash)
        }
    }


def _encode_stored_contract_by_hash_versioned(entity: StoredContractByHashVersioned) -> dict:
    return {
        "StoredContractByHashVersioned": {
            "args": [encode(i) for i in entity.arguments],
            "entry_point": entity.entry_point,
            "hash": cl_checksum.encode(entity.hash),
            "version": entity.version
        }
    }


def _encode_stored_contract_by_name(entity: StoredContractByName) -> dict:
    return {
        "StoredContractByName": {
            "args": [encode(i) for i in entity.arguments],
            "entry_point": entity.entry_point,
            "name": entity.name
        }
    }


def _encode_stored_contract_by_name_versioned(entity: StoredContractByNameVersioned) -> dict:
    return {
        "StoredContractByNameVersioned": {
            "args": [encode(i) for i in entity.arguments],
            "entry_point": entity.entry_point,
            "name": entity.name,
            "version": entity.version
        }
    }


def _encode_transfer(entity: Transfer) -> dict:
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
    ModuleBytes: _encode_module_bytes,
    StoredContractByHash: _encode_stored_contract_by_hash,
    StoredContractByHashVersioned: _encode_stored_contract_by_hash_versioned,
    StoredContractByName: _encode_stored_contract_by_name,
    StoredContractByNameVersioned: _encode_stored_contract_by_name_versioned,
    Transfer: _encode_transfer,
}
