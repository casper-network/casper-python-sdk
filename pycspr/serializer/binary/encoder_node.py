import typing

from pycspr.serializer.binary.encoder_clt import encode as encode_clt
from pycspr.serializer.binary.encoder_clv import encode as encode_clv
from pycspr.serializer.utils import clv_to_clt
from pycspr.type_defs.cl_values import CLV_ByteArray
from pycspr.type_defs.cl_values import CLV_U32
from pycspr.type_defs.cl_values import CLV_U64
from pycspr.type_defs.cl_values import CLV_List
from pycspr.type_defs.cl_values import CLV_PublicKey
from pycspr.type_defs.cl_values import CLV_String
from pycspr.types.node import Deploy
from pycspr.types.node import DeployApproval
from pycspr.types.node import DeployArgument
from pycspr.types.node import DeployBody
from pycspr.types.node import DeployHeader
from pycspr.types.node import DeployOfModuleBytes
from pycspr.types.node import DeployOfStoredContractByHash
from pycspr.types.node import DeployOfStoredContractByHashVersioned
from pycspr.types.node import DeployOfStoredContractByName
from pycspr.types.node import DeployOfStoredContractByNameVersioned
from pycspr.types.node import DeployOfTransfer
from pycspr.types.node import EraEnd
from pycspr.types.node import EraEndReport
from pycspr.types.node import ProtocolVersion
from pycspr.types.node import ValidatorReward
from pycspr.types.node import ValidatorWeight


def encode(entity: object) -> bytes:
    """Encoder: Domain entity -> an array of bytes.

    :param entity: A deploy related type instance to be encoded.
    :returns: An array of bytes.

    """
    if entity is None:
        return bytes([])
    else:
        try:
            encoder = _ENCODERS[type(entity)]
        except KeyError:
            raise ValueError(f"Unknown entity type: {entity}")
        else:
            return encoder(entity)


def _encode_deploy(entity: Deploy) -> bytes:
    return \
        encode(entity.header) + \
        entity.hash + \
        encode(entity.payment) + \
        encode(entity.session) + \
        _encode_deploy_approval_set(entity.approvals)


def _encode_deploy_approval(entity: DeployApproval) -> bytes:
    # TODO: check why this logic is required
    if isinstance(entity.signer, bytes):
        return entity.signer + entity.signature.to_bytes()
    else:
        return entity.signer.to_bytes() + entity.signature.to_bytes()


def _encode_deploy_approval_set(entities: typing.List[DeployApproval]) -> bytes:
    return \
        encode_clv(
            CLV_U32(len(entities))
        ) + \
        bytes(
            [i for j in map(encode, entities) for i in j]
        )


def _encode_deploy_argument(entity: DeployArgument) -> bytes:
    return \
        encode_clv(
            CLV_String(entity.name)
        ) + \
        _u8_array_to_bytes(
            encode_clv(entity.value)
        ) + \
        encode_clt(
            clv_to_clt(entity.value)
        )


def _encode_deploy_body(entity: DeployBody) -> bytes:
    return \
        encode(entity.payment) + \
        encode(entity.session) + \
        entity.hash


def _encode_deploy_header(entity: DeployHeader) -> bytes:
    return \
        encode_clv(
            CLV_PublicKey.from_public_key(entity.account)
        ) + \
        encode_clv(
            CLV_U64(int(entity.timestamp.value * 1000))
        ) + \
        encode_clv(
            CLV_U64(entity.ttl.as_milliseconds)
        ) + \
        encode_clv(
            CLV_U64(entity.gas_price)
        ) + \
        encode_clv(
            CLV_ByteArray(entity.body_hash)
        ) + \
        encode_clv(
            CLV_List(entity.dependencies)
        ) + \
        encode_clv(
            CLV_String(entity.chain_name)
        )


def _encode_era_end(entity: EraEnd) -> bytes:
    return \
        encode(
            entity.era_report
        ) + \
        encode_clv(
            CLV_List(
                [CLV_ByteArray(encode(i)) for i in entity.next_era_validator_weights]
            )
        )


def _encode_era_end_report(entity: EraEndReport) -> bytes:
    return \
        encode_clv(
            CLV_List(
                [CLV_PublicKey(encode(i)) for i in entity.equivocators]
            )
        ) + \
        encode_clv(
            CLV_List(
                [CLV_ByteArray(encode(i)) for i in entity.rewards]
            )
        ) + \
        encode_clv(
            CLV_List(
                [CLV_PublicKey(encode(i)) for i in entity.inactive_validators]
            )
        )


def _encode_module_bytes(entity: DeployOfModuleBytes) -> bytes:
    return \
        bytes([0]) + \
        _u8_array_to_bytes(
            list(entity.module_bytes)
        ) + \
        _vector_to_bytes(
            list(map(encode, entity.arguments))
        )


def _encode_protocol_version(entity: ProtocolVersion) -> bytes:
    return \
        encode_clv(
            CLV_U32(entity.major)
        ) + \
        encode_clv(
            CLV_U32(entity.minor)
        ) + \
        encode_clv(
            CLV_U32(entity.revision)
        )


def _encode_stored_contract_by_hash(entity: DeployOfStoredContractByHash) -> bytes:
    return \
        bytes([1]) + \
        encode_clv(
            CLV_ByteArray(entity.hash)
        ) + \
        encode_clv(
            CLV_String(entity.entry_point)
        ) + \
        _vector_to_bytes(
            list(map(encode, entity.arguments))
        )


def _encode_stored_contract_by_hash_versioned(
    entity: DeployOfStoredContractByHashVersioned
) -> bytes:
    return \
        bytes([2]) + \
        encode_clv(
            CLV_ByteArray(entity.hash)
        ) + \
        encode_clv(
            CLV_U32(entity.version)
        ) + \
        encode_clv(
            CLV_String(entity.entry_point)
        ) + \
        _vector_to_bytes(
            list(map(encode, entity.arguments))
        )


def _encode_stored_contract_by_name(entity: DeployOfStoredContractByName) -> bytes:
    return \
        bytes([3]) + \
        encode_clv(
            CLV_String(entity.name)
        ) + \
        encode_clv(
            CLV_String(entity.entry_point)
        ) + \
        _vector_to_bytes(
            list(map(encode, entity.arguments))
        )


def _encode_stored_contract_by_name_versioned(
    entity: DeployOfStoredContractByNameVersioned
) -> bytes:
    return \
        bytes([4]) + \
        encode_clv(
            CLV_String(entity.name)
        ) + \
        encode_clv(
            CLV_U32(entity.version)
        ) + \
        encode_clv(
            CLV_String(entity.entry_point)
        ) + \
        _vector_to_bytes(
            list(map(encode, entity.arguments))
        )


def _encode_transfer(entity: DeployOfTransfer) -> bytes:
    return \
        bytes([5]) + \
        _vector_to_bytes(
            list(map(encode, entity.arguments))
        )


def _encode_validator_reward(entity: ValidatorReward) -> bytes:
    return \
        encode_clv(
            CLV_PublicKey.from_public_key(entity.validator)
        ) + \
        encode_clv(
            CLV_U64(entity.amount)
        )


def _encode_validator_weight(entity: ValidatorWeight) -> bytes:
    return \
        encode_clv(
            CLV_PublicKey.from_public_key(entity.validator)
        ) + \
        encode_clv(
            CLV_U64(entity.weight)
        )


def _encode_validator_weight_set(entities: typing.List[ValidatorWeight]) -> bytes:
    return \
        encode_clv(
            CLV_U32(len(entities))
        ) + \
        bytes(
            [encode(i) for i in entities]
        )


def _u8_array_to_bytes(value: typing.List[int]) -> bytes:
    return \
        encode_clv(
            CLV_U32(len(value))
        ) + \
        bytes(value)


def _vector_to_bytes(value: typing.List) -> bytes:
    return \
        encode_clv(
            CLV_U32(len(value))
        ) + \
        bytes(
            [i for j in value for i in j]
        )


_ENCODERS = {
    Deploy: _encode_deploy,
    DeployApproval: _encode_deploy_approval,
    DeployArgument: _encode_deploy_argument,
    DeployBody: _encode_deploy_body,
    DeployHeader: _encode_deploy_header,
    DeployOfModuleBytes: _encode_module_bytes,
    DeployOfStoredContractByHash: _encode_stored_contract_by_hash,
    DeployOfStoredContractByHashVersioned: _encode_stored_contract_by_hash_versioned,
    DeployOfStoredContractByName: _encode_stored_contract_by_name,
    DeployOfStoredContractByNameVersioned: _encode_stored_contract_by_name_versioned,
    DeployOfTransfer: _encode_transfer,
    EraEnd: _encode_era_end,
    EraEndReport: _encode_era_end_report,
    ProtocolVersion: _encode_protocol_version,
    ValidatorReward: _encode_validator_reward,
    ValidatorWeight: _encode_validator_weight,
}
