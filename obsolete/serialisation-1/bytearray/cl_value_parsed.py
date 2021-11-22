from pycspr.serialisation.bytearray import cl_any
from pycspr.serialisation.bytearray import cl_bool
from pycspr.serialisation.bytearray import cl_byte_array
from pycspr.serialisation.bytearray import cl_i32
from pycspr.serialisation.bytearray import cl_i64
from pycspr.serialisation.bytearray import cl_key
from pycspr.serialisation.bytearray import cl_list
from pycspr.serialisation.bytearray import cl_map
from pycspr.serialisation.bytearray import cl_option
from pycspr.serialisation.bytearray import cl_public_key
from pycspr.serialisation.bytearray import cl_result
from pycspr.serialisation.bytearray import cl_string
from pycspr.serialisation.bytearray import cl_tuple_1
from pycspr.serialisation.bytearray import cl_tuple_2
from pycspr.serialisation.bytearray import cl_tuple_3
from pycspr.serialisation.bytearray import cl_u8
from pycspr.serialisation.bytearray import cl_u32
from pycspr.serialisation.bytearray import cl_u64
from pycspr.serialisation.bytearray import cl_u128
from pycspr.serialisation.bytearray import cl_u256
from pycspr.serialisation.bytearray import cl_u512
from pycspr.serialisation.bytearray import cl_unit
from pycspr.serialisation.bytearray import cl_uref
from pycspr.types import CLType
from pycspr.types import CLTypeKey
from pycspr.types import CLValue
from pycspr.types import TYPES_NUMERIC


# Map: CL type key <-> serialiser.
_SERIALISERS = {
    CLTypeKey.ANY: cl_any,
    CLTypeKey.BOOL: cl_bool,
    CLTypeKey.BYTE_ARRAY: cl_byte_array,
    CLTypeKey.I32: cl_i32,
    CLTypeKey.I64: cl_i64,
    CLTypeKey.KEY: cl_key,
    CLTypeKey.LIST: cl_list,
    CLTypeKey.MAP: cl_map,
    CLTypeKey.OPTION: cl_option,
    CLTypeKey.PUBLIC_KEY: cl_public_key,
    CLTypeKey.RESULT: cl_result,
    CLTypeKey.STRING: cl_string,
    CLTypeKey.TUPLE_1: cl_tuple_1,
    CLTypeKey.TUPLE_2: cl_tuple_2,
    CLTypeKey.TUPLE_3: cl_tuple_3,
    CLTypeKey.U8: cl_u8,
    CLTypeKey.U32: cl_u32,
    CLTypeKey.U64: cl_u64,
    CLTypeKey.U128: cl_u128,
    CLTypeKey.U256: cl_u256,
    CLTypeKey.U512: cl_u512,
    CLTypeKey.UNIT: cl_unit,
    CLTypeKey.UREF: cl_uref,
}


def from_bytes(value: bytes) -> object:
    raise NotImplementedError()


def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_bytes(value: CLValue) -> bytes:
    serialiser = _SERIALISERS[value.cl_type.type_key]
    if value.cl_type.type_key in {CLTypeKey.LIST, CLTypeKey.OPTION}:
        inner_serialiser = _SERIALISERS[value.cl_type.inner_type.type_key]
        return serialiser.to_bytes(value.parsed, inner_serialiser)
    else:
        return serialiser.to_bytes(value.parsed)


def to_json(entity: CLValue, type_info: CLType = None) -> str:
    type_info = type_info or entity.cl_type

    if entity.cl_type.type_key in {CLTypeKey.LIST, CLTypeKey.OPTION}:
        serialiser = _SERIALISERS[entity.cl_type.inner_type.type_key]
    else:
        serialiser = _SERIALISERS[entity.cl_type.type_key]

    print(serialiser)

    return serialiser.to_json(entity.parsed)


    if type_info.type_key in TYPES_NUMERIC:
        return str(int(entity.parsed))
    elif type_info.type_key == CLTypeKey.BYTE_ARRAY:
        return cl_byte_array.to_json(entity.parsed)
    elif type_info.type_key == CLTypeKey.KEY:
        print(777)
        if type_info.key_type == KeyType.ACCOUNT:
            return {
                "Account": entity.parsed.as_string()
            }
        return entity.parsed.as_string()
    elif type_info.type_key == CLTypeKey.PUBLIC_KEY:
        return entity.parsed.account_key.hex()
    elif type_info.type_key == CLTypeKey.UREF:
        return entity.parsed.as_string()
    elif type_info.type_key == CLTypeKey.OPTION:
        return to_json(entity, type_info.inner_type)
    else:
        return str(entity.parsed)

