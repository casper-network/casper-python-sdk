import typing

from pycspr.crypto import checksummer
from pycspr.serializer.json.encoder_clv import encode as encode_clv
from pycspr.serializer.json.encoder_crypto import ENCODERS as CRYPTO_ENCODERS
from pycspr.serializer.json.encoder_primitives import ENCODERS as CRYPTO_PRIMITIVES
from pycspr.type_defs.cl_values import CLV_Value
from pycspr.type_defs.crypto import DigestHex
from pycspr.types.node import Deploy
from pycspr.types.node import DeployHeader
from pycspr.types.node import Block
from pycspr.types.node import BlockBody
from pycspr.types.node import BlockHeader
from pycspr.types.node import BlockSignature
from pycspr.types.node import DeployApproval
from pycspr.types.node import DeployArgument
from pycspr.types.node import DeployHash
from pycspr.types.node import DeployOfModuleBytes
from pycspr.types.node import DeployOfStoredContractByHash
from pycspr.types.node import DeployOfStoredContractByHashVersioned
from pycspr.types.node import DeployOfStoredContractByName
from pycspr.types.node import DeployOfStoredContractByNameVersioned
from pycspr.types.node import DeployOfTransfer
from pycspr.types.node import EraEnd
from pycspr.types.node import ProtocolVersion
from pycspr.utils import convertor


def encode(entity: object) -> dict:
    """Encodes a domain entity instance to a JSON encodeable dictionary.

    :param entity: A node related type instance to be encoded.
    :returns: A JSON encodeable dictionary.

    """
    typedef = type(entity)
    try:
        encoder = _ENCODERS[typedef]
    except KeyError:
        raise ValueError(f"Unknown entity type: {typedef} :: {entity}")
    else:
        return encoder(entity)


def _encode_block(entity: Block) -> dict:
    return {
        "hash": encode(entity.hash),
        "header": encode(entity.header),
        "body": encode(entity.body),
        "proofs": [encode(i) for i in entity.proofs]
    }


def _encode_block_body(entity: BlockBody) -> dict:
    return {
        "proposer": encode(entity.proposer),
        "deploy_hashes": [encode(i) for i in entity.deploy_hashes],
        "transfer_hashes": [encode(i) for i in entity.transfer_hashes],
    }


def _encode_block_header(entity: BlockHeader) -> dict:
    return {
        "parent_hash": encode(entity.parent_hash),
        "state_root_hash": encode(entity.state_root),
        "body_hash": encode(entity.body_hash),
        "random_bit": encode(entity.random_bit),
        "accumulated_seed": encode(entity.accumulated_seed),
        "era_end": None if entity.era_end is None else encode(entity.era_end),
        "timestamp": convertor.iso_datetime_from_timestamp(entity.timestamp.value),
        "era_id": encode(entity.era_id),
        "height": encode(entity.height),
        "protocol_version": encode(entity.protocol_version),
    }


def _encode_block_signature(entity: BlockSignature) -> dict:
    return {
        "public_key": encode(entity.public_key),
        "signature": encode(entity.signature),
    }


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
    return (entity.name, encode_clv(entity.value))


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


def _encode_era_end(entity: EraEnd) -> dict:
    return dict()


def _encode_module_bytes(entity: DeployOfModuleBytes) -> dict:
    return {
        "ModuleBytes": {
            "args": [encode(i) for i in entity.arguments],
            "module_bytes": checksummer.encode_bytes(entity.module_bytes)
        }
    }


def _encode_protocol_version(entity: ProtocolVersion) -> str:
    return f"{entity.major}.{entity.minor}.{entity.revision}"


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


_ENCODERS = CRYPTO_ENCODERS | CRYPTO_PRIMITIVES | {
    DeployHash: lambda x: encode(DigestHex, x),

    Block: _encode_block,
    BlockBody: _encode_block_body,
    BlockHeader: _encode_block_header,
    BlockSignature: _encode_block_signature,
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
    EraEnd: _encode_era_end,
    ProtocolVersion: _encode_protocol_version,
}
