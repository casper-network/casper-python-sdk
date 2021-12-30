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
    if isinstance(entity, Deploy):
        return {
            "approvals": [encode(i) for i in entity.approvals],
            "hash": cl_checksum.encode_digest(entity.hash),
            "header": encode(entity.header),
            "payment": encode(entity.payment),
            "session": encode(entity.session)
        }

    elif isinstance(entity, DeployApproval):
        return {
            "signature": cl_checksum.encode_signature(entity.signature),
            "signer": cl_checksum.encode_account_key(entity.signer.account_key)
        }

    elif isinstance(entity, DeployArgument):
        return [
            entity.name,
            cl_value_to_json(entity.value)
        ]

    elif isinstance(entity, DeployHeader):
        return {
            "account": cl_checksum.encode_account_key(entity.account_public_key.account_key),
            "body_hash": cl_checksum.encode_digest(entity.body_hash),
            "chain_name": entity.chain_name,
            "dependencies": entity.dependencies,
            "gas_price": entity.gas_price,
            "timestamp": entity.timestamp.to_string(),
            "ttl": entity.ttl.to_string()
        }

    elif isinstance(entity, ModuleBytes):
        return {
            "ModuleBytes": {
                "args": [encode(i) for i in entity.args],
                "module_bytes": cl_checksum.encode(entity.module_bytes)
            }
        }

    elif isinstance(entity, StoredContractByHash):
        return {
            "StoredContractByHash": {
                "args": [encode(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "hash": cl_checksum.encode(entity.hash)
            }
        }

    elif isinstance(entity, StoredContractByHashVersioned):
        return {
            "StoredContractByHashVersioned": {
                "args": [encode(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "hash": cl_checksum.encode(entity.hash),
                "version": entity.version
            }
        }

    elif isinstance(entity, StoredContractByName):
        return {
            "StoredContractByName": {
                "args": [encode(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "name": encode.name
            }
        }

    elif isinstance(entity, StoredContractByNameVersioned):
        return {
            "StoredContractByNameVersioned": {
                "args": [encode(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "name": encode.name,
                "version": encode.version
            }
        }

    elif isinstance(entity, Transfer):
        return {
            "Transfer": {
                "args": [encode(i) for i in entity.args],
            }
        }
