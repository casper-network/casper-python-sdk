import typing

from pycspr.serialisation.byte_array.constants import TypeTag_ExecutableDeployItem
from pycspr.serialisation.byte_array.encoder.cl_complex import encode_vector_of_t
from pycspr.serialisation.byte_array.encoder.cl_primitive import encode_string
from pycspr.serialisation.byte_array.encoder.cl_primitive import encode_byte_array
from pycspr.serialisation.byte_array.encoder.cl_primitive import encode_u32
from pycspr.serialisation.byte_array.encoder.cl_primitive import encode_u8_array
from pycspr.serialisation.byte_array.encoder.cl_type import encode_cl_type
from pycspr.serialisation.byte_array.encoder.cl_value import encode as encode_cl_value
from pycspr.types import Deploy
from pycspr.types import DeployHeader
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutableDeployItem
from pycspr.types import ExecutableDeployItem_ModuleBytes
from pycspr.types import ExecutableDeployItem_StoredContractByHash
from pycspr.types import ExecutableDeployItem_StoredContractByHashVersioned
from pycspr.types import ExecutableDeployItem_StoredContractByName
from pycspr.types import ExecutableDeployItem_StoredContractByNameVersioned
from pycspr.types import ExecutableDeployItem_Transfer


def encode_deploy(entity: Deploy) -> bytes:
    """Encodes a deploy.

    """
    raise NotImplementedError()


def encode_deploy_header(entity: DeployHeader) -> bytes:
    """Encodes a deploy header.

    """
    raise NotImplementedError()


def encode_execution_argument(entity: ExecutionArgument) -> bytes:
    """Encodes an execution argument.

    """
    return \
        encode_string(entity.name) + \
        encode_u8_array(encode_cl_value(entity.value)) + \
        encode_cl_type(entity.value.cl_type)


def encode_executable_deploy_item(entity: ExecutableDeployItem) -> bytes:
    """Encodes execution information for subsequent interpretation by VM.

    """
    def _encode_type_tag(tag: TypeTag_ExecutableDeployItem):
        return bytes([tag.value])

    def _encode_args(args: typing.List[ExecutionArgument]):
        return encode_vector_of_t(list(map(encode_execution_argument, args)))

    def _encode_module_bytes():
        return _encode_type_tag(TypeTag_ExecutableDeployItem.ModuleBytes) + \
               encode_u8_array(list(entity.module_bytes)) + \
               _encode_args(entity.args)

    def _encode_stored_contract_by_hash():
        return _encode_type_tag(TypeTag_ExecutableDeployItem.StoredContractByHash) + \
               encode_byte_array(entity.hash) + \
               encode_string(entity.entry_point) + \
               _encode_args(entity.args)

    def _encode_stored_contract_by_hash_versioned():
        return _encode_type_tag(TypeTag_ExecutableDeployItem.StoredContractByHashVersioned) + \
               encode_byte_array(entity.hash) + \
               encode_u32(entity.version) + \
               encode_string(entity.entry_point) + \
               _encode_args(entity.args)

    def _encode_stored_contract_by_name():
        return _encode_type_tag(TypeTag_ExecutableDeployItem.StoredContractByName) + \
               encode_string(entity.name) + \
               encode_string(entity.entry_point) + \
               _encode_args(entity.args)

    def _encode_stored_contract_by_name_versioned():
        return _encode_type_tag(TypeTag_ExecutableDeployItem.StoredContractByNameVersioned) + \
               encode_string(entity.name) + \
               encode_u32(entity.version) + \
               encode_string(entity.entry_point) + \
               _encode_args(entity.args)

    def _encode_transfer():
        return _encode_type_tag(TypeTag_ExecutableDeployItem.Transfer) + \
               _encode_args(entity.args)

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
            _encode_transfer,
    }

    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError("Unencodeable domain type.")
    else:
        return encoder()


# Map: Deploy type <-> encoder.
ENCODERS = {
    Deploy: encode_deploy,
    DeployHeader: encode_deploy_header,
    ExecutionArgument: encode_execution_argument,
    ExecutableDeployItem_ModuleBytes: encode_executable_deploy_item,
    ExecutableDeployItem_StoredContractByHash: encode_executable_deploy_item,
    ExecutableDeployItem_StoredContractByHashVersioned: encode_executable_deploy_item,
    ExecutableDeployItem_StoredContractByName: encode_executable_deploy_item,
    ExecutableDeployItem_StoredContractByNameVersioned: encode_executable_deploy_item,
    ExecutableDeployItem_Transfer: encode_executable_deploy_item,
}


def encode(entity) -> bytes:
    """Encodes a deploy related domain entity as an array of bytes.

    """
    try:
        encoder = ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Unencodeable type: {type(entity)}")
    else:
        return encoder(entity)
