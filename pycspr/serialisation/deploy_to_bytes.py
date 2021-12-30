import typing

from pycspr.serialisation.cl_value_to_bytes import encode as cl_value_to_bytes
from pycspr.serialisation.cl_type_to_bytes import encode as cl_type_to_bytes
from pycspr.serialisation.cl_value_to_cl_type import encode as cl_value_to_cl_type
from pycspr.types import cl_values
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


def encode(entity: object) -> bytes:
    """Encodes a deploy related type instance as an array of bytes.

    :param entity: A deploy related type instance to be encoded.
    :returns: An array of bytes.
    
    """
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Unknown deploy type: {entity}")
    else:
        return encoder(entity)


def _encode_deploy(entity: Deploy) -> bytes:
    raise NotImplementedError()


def _encode_deploy_approval(entity: DeployApproval) -> bytes:
    return entity.signer + entity.signature


def _encode_deploy_argument(entity: DeployArgument) -> bytes:
    return \
        cl_value_to_bytes(cl_values.CL_String(entity.name)) + \
        _u8_array_to_bytes(cl_value_to_bytes(entity.value)) + \
        cl_type_to_bytes(cl_value_to_cl_type(entity.value))


def _encode_deploy_header(entity: DeployHeader) -> bytes:
    raise NotImplementedError()


def _encode_module_bytes(entity: ModuleBytes) -> bytes:
    return \
        bytes([0]) + \
        _u8_array_to_bytes(list(entity.module_bytes)) + \
        _vector_to_bytes(list(map(encode, entity.arguments)))


def _encode_stored_contract_by_hash(entity: StoredContractByHash) -> bytes:
    return \
        bytes([1]) + \
        cl_value_to_bytes(cl_values.CL_ByteArray(entity.hash)) + \
        cl_value_to_bytes(cl_values.CL_String(entity.entry_point)) + \
        _vector_to_bytes(list(map(encode, entity.arguments)))


def _encode_stored_contract_by_hash_versioned(entity: StoredContractByHashVersioned) -> bytes:
    return \
        bytes([2]) + \
        cl_value_to_bytes(cl_values.CL_ByteArray(entity.hash)) + \
        cl_value_to_bytes(cl_values.CL_U32(entity.version)) + \
        cl_value_to_bytes(cl_values.CL_String(entity.entry_point)) + \
        _vector_to_bytes(list(map(encode, entity.arguments)))


def _encode_stored_contract_by_name(entity: StoredContractByName) -> bytes:
    return \
        bytes([3]) + \
        cl_value_to_bytes(cl_values.CL_String(entity.name)) + \
        cl_value_to_bytes(cl_values.CL_String(entity.entry_point)) + \
        _vector_to_bytes(list(map(encode, entity.arguments)))


def _encode_stored_contract_by_name_versioned(entity: StoredContractByNameVersioned) -> bytes:
    return \
        bytes([4]) + \
        cl_value_to_bytes(cl_values.CL_String(entity.name)) + \
        cl_value_to_bytes(cl_values.CL_U32(entity.version)) + \
        cl_value_to_bytes(cl_values.CL_String(entity.entry_point)) + \
        _vector_to_bytes(list(map(encode, entity.arguments)))


def _encode_transfer(entity: Transfer) -> bytes:
    return \
        bytes([5]) + \
        _vector_to_bytes(list(map(encode, entity.arguments)))


def _u8_array_to_bytes(value: typing.List[int]) -> bytes:
    return cl_value_to_bytes(cl_values.CL_U32(len(value))) + bytes(value)


def _vector_to_bytes(value: typing.List) -> bytes:
    return \
        cl_value_to_bytes(cl_values.CL_U32(len(value))) + \
        bytes([i for j in value for i in j])


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
