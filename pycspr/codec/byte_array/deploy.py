import operator
import itertools
import typing

from pycspr.codec.byte_array.cl import encode_byte_array
from pycspr.codec.byte_array.cl import encode_string
from pycspr.codec.byte_array.cl import encode_u8_array
from pycspr.codec.byte_array.cl import encode_vector_of_t

from pycspr.codec.byte_array.cl_value import encode as encode_cl_value

from pycspr.types.deploy import ExecutionArgument
from pycspr.types.deploy import ExecutionInfo
from pycspr.types.deploy import ExecutionInfo_ModuleBytes
from pycspr.types.deploy import ExecutionInfo_StoredContract
from pycspr.types.deploy import ExecutionInfo_StoredContractByHash
from pycspr.types.deploy import ExecutionInfo_StoredContractByHashVersioned
from pycspr.types.deploy import ExecutionInfo_StoredContractByName
from pycspr.types.deploy import ExecutionInfo_StoredContractByNameVersioned
from pycspr.types.deploy import ExecutionInfo_Transfer



# Map: domain type <-> encoding tag.
_TYPE_TAGS = {
    ExecutionInfo_ModuleBytes : 0,
    ExecutionInfo_StoredContractByHash : 1,
    ExecutionInfo_StoredContractByHashVersioned : 3,
    ExecutionInfo_StoredContractByName : 2,
    ExecutionInfo_StoredContractByNameVersioned : 4,
    ExecutionInfo_Transfer : 5,
}


def _encode_arg(entity: ExecutionArgument):
    return encode_string(entity.name) + \
           encode_cl_value(entity.value)


def _encode_args(args: typing.List[ExecutionArgument]):
    return encode_vector_of_t(list(map(_encode_arg, args)))


def _encode_module_bytes(entity: ExecutionInfo_ModuleBytes):
    return encode_u8_array(list(entity.module_bytes)) + \
           _encode_args(entity.args)


def _encode_stored_contract_by_hash(entity: ExecutionInfo_StoredContractByHash):
    return encode_byte_array(entity.hash) + \
           encode_string(entity.entry_point) + \
           _encode_args(entity.args)


def _encode_stored_contract_by_hash_versioned(entity: ExecutionInfo_StoredContractByHashVersioned):
    # TODO: encode optional U32 :: contract version
    return encode_byte_array(entity.hash) + \
           encode_string(entity.entry_point) + \
           _encode_args(entity.args)


def _encode_stored_contract_by_name(entity: ExecutionInfo_StoredContractByName):
    return encode_string(entity.name) + \
           encode_string(entity.entry_point) + \
           _encode_args(entity.args)


def _encode_stored_contract_by_name_versioned(entity: ExecutionInfo_StoredContractByNameVersioned):
    # TODO: encode optional U32 :: contract version
    return encode_string(entity.name) + \
           encode_string(entity.entry_point) + \
           _encode_args(entity.args)


def _encode_transfer(entity: ExecutionInfo_Transfer):
    return _encode_args(entity.args)


# Map: domain type <-> encoding function.
_ENCODERS = {
    ExecutionInfo_ModuleBytes : _encode_module_bytes,
    ExecutionInfo_StoredContractByHash : _encode_stored_contract_by_hash,
    ExecutionInfo_StoredContractByHashVersioned : _encode_stored_contract_by_hash_versioned,
    ExecutionInfo_StoredContractByName : _encode_stored_contract_by_name,
    ExecutionInfo_StoredContractByNameVersioned : _encode_stored_contract_by_name_versioned,
    ExecutionInfo_Transfer : _encode_transfer,
}


def encode(value: ExecutionInfo) -> typing.List[int]:
    """Maps value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    try:
        type_tag = _TYPE_TAGS[type(value)]
    except KeyError:
        raise ValueError("Invalid domin type.")
    encoder = _ENCODERS[type(value)]

    return [type_tag] + encoder(value)
