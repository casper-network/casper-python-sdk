import typing

from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import int_to_le_bytes_trimmed
from pycspr.types.cl import CLTypeKey
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLValue
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
from pycspr.utils.constants import NUMERIC_CONSTRAINTS



def encode_bool(value: bool):
    return [int(value)]


def encode_byte_array(value: typing.Union[bytes, str]):    
    return [int(i) for i in value] if isinstance(value, bytes) else \
           [int(i) for i in bytes.fromhex(value)]


def encode_cl_value(value: CLValue) -> typing.List[int]:
    """Maps value to it's CL byte array representation.

    :param value: Value to be mapped.
    :returns: CL byte array representation.
        
    """
    return []


def encode_execution_argument(entity: ExecutionArgument) -> typing.List[int]:
    return encode_string(entity.name) + encode_cl_value(entity.value)


def encode_execution_info(entity: ExecutionInfo) -> typing.List[int]:
    _TYPE_TAGS = {
        ExecutionInfo_ModuleBytes: 0,
        ExecutionInfo_StoredContractByHash: 1,
        ExecutionInfo_StoredContractByHashVersioned: 3,
        ExecutionInfo_StoredContractByName: 2,
        ExecutionInfo_StoredContractByNameVersioned: 4,
        ExecutionInfo_Transfer: 5,
    }

    if type(entity) not in _TYPE_TAGS:
        raise ValueError("Invalid domain type.")

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

    return [_TYPE_TAGS[type(entity)]] + _ENCODERS[type(entity)]()


def encode_i32(value: int):
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.I32].LENGTH, True)


def encode_i64(value: int):
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.I64].LENGTH, True)
    

def encode_key(value: str):
    value = encode_byte_array((value or "").encode("utf-8"))

    return encode_u32(len(value)) + value


def encode_list(value: list):
    return []


def encode_map(value: list):
    return []


def encode_option(value: object, sub_encoder: typing.Callable):
    return [0] if value is None else [1] + sub_encoder(value)


def encode_public_key(value: str):
    value = encode_byte_array((value or "").encode("utf-8"))

    return encode_u32(len(value)) + value


def encode_string(value: str):
    value = encode_byte_array((value or "").encode("utf-8"))

    return encode_u32(len(value)) + value


def encode_tuple1(value: tuple):
    return []


def encode_tuple2(value: tuple):
    return []


def encode_tuple3(value: tuple):
    return []


def encode_u8(value: int):
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH, False)


def encode_u8_array(value: typing.List[int]) -> typing.List[int]:
    return encode_u32(len(value)) + value


def encode_u32(value: int):
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH, False)


def encode_u64(value: int):
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH, False)


def encode_u128(value: int):
    if value < NUMERIC_CONSTRAINTS[CLTypeKey.U128].MIN or \
       value > NUMERIC_CONSTRAINTS[CLTypeKey.U128].MAX:
        raise ValueError("Invalid U128: max size exceeded")
    
    if value >= NUMERIC_CONSTRAINTS[CLTypeKey.U8].MIN and \
       value <= NUMERIC_CONSTRAINTS[CLTypeKey.U8].MAX:
        encoded_length = NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH
        type_key = CLTypeKey.U8

    elif value >= NUMERIC_CONSTRAINTS[CLTypeKey.U32].MIN and \
         value <= NUMERIC_CONSTRAINTS[CLTypeKey.U32].MAX:
        encoded_length = NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH
        type_key = CLTypeKey.U32

    elif value >= NUMERIC_CONSTRAINTS[CLTypeKey.U64].MIN and \
         value <= NUMERIC_CONSTRAINTS[CLTypeKey.U64].MAX:
        encoded_length = NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH
        type_key = CLTypeKey.U64

    else:
        encoded_length = NUMERIC_CONSTRAINTS[CLTypeKey.U128].LENGTH
        type_key = CLTypeKey.U128
    
    return [type_key.value] + int_to_le_bytes_trimmed(value, encoded_length, False)


def encode_u256(value: int):
    if value < NUMERIC_CONSTRAINTS[CLTypeKey.U256].MIN or \
       value > NUMERIC_CONSTRAINTS[CLTypeKey.U256].MAX:
        raise ValueError("Invalid U256: max size exceeded")

    if value >= NUMERIC_CONSTRAINTS[CLTypeKey.U128].MIN and \
       value <= NUMERIC_CONSTRAINTS[CLTypeKey.U128].MAX:
       return [CLTypeKey.U256.value] + encode_u128(value)[1:]

    return [CLTypeKey.U256.value] + \
            int_to_le_bytes_trimmed(value, NUMERIC_CONSTRAINTS[CLTypeKey.U256].LENGTH, False)


def encode_u512(value: int):
    if value < NUMERIC_CONSTRAINTS[CLTypeKey.U512].MIN or \
       value > NUMERIC_CONSTRAINTS[CLTypeKey.U512].MAX:
        raise ValueError("Invalid U512: max size exceeded")

    if value >= NUMERIC_CONSTRAINTS[CLTypeKey.U256].MIN and \
       value <= NUMERIC_CONSTRAINTS[CLTypeKey.U256].MAX:
       return [CLTypeKey.U512.value] + encode_u256(value)[1:]

    return [CLTypeKey.U512.value] + \
            int_to_le_bytes_trimmed(value, NUMERIC_CONSTRAINTS[CLTypeKey.U512].LENGTH, False)


def encode_unit(value: None):
    return []


def encode_uref(value: str):
    return [int(i) for i in (value or "").encode("utf-8")]


def encode_vector_of_t(value: list):
    return encode_u32(len(value)) + [i for j in value for i in j]


# Map: entity type <-> encoder.
_ENCODERS = {
    CLTypeKey.ANY: None,
    CLTypeKey.BOOL: encode_bool,
    CLTypeKey.BYTE_ARRAY: encode_byte_array,
    CLTypeKey.I32: encode_i32,
    CLTypeKey.I64: encode_i64,
    CLTypeKey.KEY: encode_key,
    CLTypeKey.LIST: encode_list,    
    CLTypeKey.MAP: encode_map,    
    CLTypeKey.OPTION: encode_option,    
    CLTypeKey.PUBLIC_KEY: encode_public_key,
    CLTypeKey.STRING: encode_string,
    CLTypeKey.TUPLE_1: encode_tuple1,
    CLTypeKey.TUPLE_2: encode_tuple2,
    CLTypeKey.TUPLE_3: encode_tuple3,
    CLTypeKey.U8: encode_u8,
    CLTypeKey.U32: encode_u32,
    CLTypeKey.U64: encode_u64,
    CLTypeKey.U128: encode_u128,    
    CLTypeKey.U256: encode_u256,
    CLTypeKey.U512: encode_u512,
    CLTypeKey.UNIT: encode_unit,
    CLTypeKey.RESULT: None,
    CLTypeKey.UREF: encode_uref,
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


def encode(value) -> typing.List[int]:
    """Encodes a value as an array of bytes decodeable by a CSPR agent.
    
    """
    if type(value) == CLValue:
        encoder = _ENCODERS[value.cl_type.typeof]
        if type(value.cl_type) == CLType_Option:
            return encoder(value.parsed, _ENCODERS[value.cl_type.inner_type.typeof])
        else:
            return encoder(value.parsed)
    else:
        if type(value) not in _ENCODERS:
            raise ValueError("Unencodeable type: {type(value)}")
        return _ENCODERS[type(value)](value)
