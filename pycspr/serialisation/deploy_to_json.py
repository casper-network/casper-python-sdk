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
            "hash": entity.hash.hex(),
            "header": encode(entity.header),
            "payment": encode(entity.payment),
            "session": encode(entity.session)
        }

    if isinstance(entity, DeployApproval):
        return {
            "signature": entity.signature.hex(),
            "signer": entity.signer.hex()
        }

    if isinstance(entity, DeployArgument):
        return [
            entity.name,
            cl_value_to_json(entity.value)
        ]

    if isinstance(entity, DeployHeader):
        return {
            "account": entity.account_public_key.account_key.hex(),
            "body_hash": entity.body_hash.hex(),
            "chain_name": entity.chain_name,
            "dependencies": entity.dependencies,
            "gas_price": entity.gas_price,
            "timestamp": entity.timestamp.to_string(),
            "ttl": entity.ttl.to_string()
        }

    if isinstance(entity, ModuleBytes):
        return {
            "ModuleBytes": {
                "args": [encode(i) for i in entity.args],
                "module_bytes": entity.module_bytes.hex()
            }
        }

    if isinstance(entity, StoredContractByHash):
        return {
            "StoredContractByHash": {
                "args": [encode(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "hash": entity.hash.hex()
            }
        }

    if isinstance(entity, StoredContractByHashVersioned):
        return {
            "StoredContractByHashVersioned": {
                "args": [encode(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "hash": entity.hash.hex(),
                "version": entity.version
            }
        }

    if isinstance(entity, StoredContractByName):
        return {
            "StoredContractByName": {
                "args": [encode(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "name": encode.name
            }
        }

    if isinstance(entity, StoredContractByNameVersioned):
        return {
            "StoredContractByNameVersioned": {
                "args": [encode(i) for i in entity.args],
                "entry_point": entity.entry_point,
                "name": encode.name,
                "version": encode.version
            }
        }

    if isinstance(entity, Transfer):
        return {
            "Transfer": {
                "args": [encode(i) for i in entity.args],
            }
        }
