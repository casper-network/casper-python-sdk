import typing

from pycspr.serialisation.byte_array.encoder.cl import encode_cl_value
from pycspr.serialisation.byte_array.encoder.cl import encode_string
from pycspr.serialisation.byte_array.encoder.cl import encode_byte_array
from pycspr.serialisation.byte_array.encoder.cl import encode_u8_array
from pycspr.serialisation.byte_array.encoder.cl import encode_vector_of_t
from pycspr.types import Deploy
from pycspr.types import DeployHeader
from pycspr.types import ExecutionArgument
from pycspr.types import ExecutableDeployItem
from pycspr.types import ExecutableDeployItem_ModuleBytes
from pycspr.types import ExecutableDeployItem_StoredContract
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
    return encode_string(entity.name) + encode_cl_value(entity.value)


def encode_execution_info(entity: ExecutableDeployItem) -> bytes:
    """Encodes execution information for subsequent interpretation by VM.
    
    """
    def encode_args(args: typing.List[ExecutionArgument]):
        return encode_vector_of_t(list(map(encode_execution_argument, args)))

    def encode_module_bytes():
        return encode_u8_array(list(entity.module_bytes)) + \
               encode_args(entity.args)

    def encode_stored_contract_by_hash():
        return encode_byte_array(entity.hash) + \
               encode_string(entity.entry_point) + \
               encode_args(entity.args)

    def encode_stored_contract_by_hash_versioned():
        # TODO: encode optional U32 :: contract version
        return encode_byte_array(entity.hash) + \
               encode_string(entity.entry_point) + \
               encode_args(entity.args)

    def encode_stored_contract_by_name():
        return encode_string(entity.name) + \
               encode_string(entity.entry_point) + \
               encode_args(entity.args)

    def encode_stored_contract_by_name_versioned():
        # TODO: encode optional U32 :: contract version
        return encode_string(entity.name) + \
               encode_string(entity.entry_point) + \
               encode_args(entity.args)

    def encode_transfer():
        return encode_args(entity.args)

    _ENCODERS = {
        ExecutableDeployItem_ModuleBytes: (0, encode_module_bytes),
        ExecutableDeployItem_StoredContractByHash: (1, encode_stored_contract_by_hash),
        ExecutableDeployItem_StoredContractByHashVersioned: (3, encode_stored_contract_by_hash_versioned),
        ExecutableDeployItem_StoredContractByName: (2, encode_stored_contract_by_name),
        ExecutableDeployItem_StoredContractByNameVersioned: (4, encode_stored_contract_by_name_versioned),
        ExecutableDeployItem_Transfer: (5, encode_transfer),
    }

    try:
        type_tag, encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError("Unencodeable domain type.")
    else:
        return bytes([type_tag]) + encoder()


# Map: Deploy type <-> encoder.
ENCODERS = {
    Deploy: encode_deploy,
    DeployHeader: encode_deploy_header,
    ExecutionArgument: encode_execution_argument,
    ExecutableDeployItem_ModuleBytes: encode_execution_info,
    ExecutableDeployItem_StoredContractByHash: encode_execution_info,
    ExecutableDeployItem_StoredContractByHashVersioned: encode_execution_info,
    ExecutableDeployItem_StoredContractByName: encode_execution_info,
    ExecutableDeployItem_StoredContractByNameVersioned: encode_execution_info,
    ExecutableDeployItem_Transfer: encode_execution_info,
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
