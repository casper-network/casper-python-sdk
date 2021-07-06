import typing

from pycspr.codec.byte_array.encoder_cl import encode_cl_value
from pycspr.codec.byte_array.encoder_cl import encode_string
from pycspr.codec.byte_array.encoder_cl import encode_byte_array
from pycspr.codec.byte_array.encoder_cl import encode_u8_array
from pycspr.codec.byte_array.encoder_cl import encode_vector_of_t
from pycspr.types.deploy import Deploy
from pycspr.types.deploy import DeployHeader
from pycspr.types.deploy import ExecutionArgument
from pycspr.types.deploy import ExecutionInfo
from pycspr.types.deploy import ExecutionInfo_ModuleBytes
from pycspr.types.deploy import ExecutionInfo_StoredContract
from pycspr.types.deploy import ExecutionInfo_StoredContractByHash
from pycspr.types.deploy import ExecutionInfo_StoredContractByHashVersioned
from pycspr.types.deploy import ExecutionInfo_StoredContractByName
from pycspr.types.deploy import ExecutionInfo_StoredContractByNameVersioned
from pycspr.types.deploy import ExecutionInfo_Transfer



def encode_execution_argument(entity: ExecutionArgument) -> typing.List[int]:
    """Encodes a domain value: CL execution argument.
    
    """
    return encode_string(entity.name) + encode_cl_value(entity.value)


def encode_execution_info(entity: ExecutionInfo) -> typing.List[int]:
    """Encodes a domain value: CL execution information.
    
    """
    def _encode_args(args: typing.List[ExecutionArgument]):
        return encode_vector_of_t(list(map(encode_execution_argument, args)))

    def _encode_module_bytes():
        return encode_u8_array(list(entity.module_bytes)) + _encode_args(entity.args)

    def _encode_stored_contract_by_hash():
        return encode_byte_array(entity.hash) + encode_string(entity.entry_point) + _encode_args(entity.args)

    def _encode_stored_contract_by_hash_versioned():
        # TODO: encode optional U32 :: contract version
        return encode_byte_array(entity.hash) + encode_string(entity.entry_point) + _encode_args(entity.args)

    def _encode_stored_contract_by_name():
        return encode_string(entity.name) + encode_string(entity.entry_point) + _encode_args(entity.args)

    def _encode_stored_contract_by_name_versioned():
        # TODO: encode optional U32 :: contract version
        return encode_string(entity.name) + encode_string(entity.entry_point) + _encode_args(entity.args)

    def _encode_transfer():
        return _encode_args(entity.args)

    _ENCODERS = {
        ExecutionInfo_ModuleBytes: _encode_module_bytes,
        ExecutionInfo_StoredContractByHash: _encode_stored_contract_by_hash,
        ExecutionInfo_StoredContractByHashVersioned: _encode_stored_contract_by_hash_versioned,
        ExecutionInfo_StoredContractByName: _encode_stored_contract_by_name,
        ExecutionInfo_StoredContractByNameVersioned: _encode_stored_contract_by_name_versioned,
        ExecutionInfo_Transfer: _encode_transfer,
    }

    _TYPE_TAGS = {
        ExecutionInfo_ModuleBytes: 0,
        ExecutionInfo_StoredContractByHash: 1,
        ExecutionInfo_StoredContractByHashVersioned: 3,
        ExecutionInfo_StoredContractByName: 2,
        ExecutionInfo_StoredContractByNameVersioned: 4,
        ExecutionInfo_Transfer: 5,
    }

    if type(entity) not in _ENCODERS or type(entity) not in _TYPE_TAGS:
        raise ValueError("Invalid domain type.")

    return [_TYPE_TAGS[type(entity)]] + _ENCODERS[type(entity)]()


# Map: Deploy type <-> encoder.
ENCODERS = {
    Deploy: None,
    DeployHeader: None,
    ExecutionArgument: encode_execution_argument,
    ExecutionInfo_ModuleBytes: encode_execution_info,
    ExecutionInfo_StoredContractByHash: encode_execution_info,
    ExecutionInfo_StoredContractByHashVersioned: encode_execution_info,
    ExecutionInfo_StoredContractByName: encode_execution_info,
    ExecutionInfo_StoredContractByNameVersioned: encode_execution_info,
    ExecutionInfo_Transfer: encode_execution_info,
}


def encode(entity) -> typing.List[int]:
    """Encodes a higher order domain entity as an array of bytes.
    
    """
    try:
        encoder = ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Unencodeable type: {type(entity)}")
    else:
        return encoder(entity)
