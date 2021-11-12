from pycspr.serialisation import cl_any
from pycspr.serialisation import cl_bool
from pycspr.serialisation import cl_byte_array
from pycspr.serialisation import cl_i32
from pycspr.serialisation import cl_i64
from pycspr.serialisation import cl_map
from pycspr.serialisation import cl_option
from pycspr.serialisation import cl_public_key
from pycspr.serialisation import cl_result
from pycspr.serialisation import cl_key
from pycspr.serialisation import cl_string
from pycspr.serialisation import cl_tuple_1
from pycspr.serialisation import cl_tuple_2
from pycspr.serialisation import cl_tuple_3
from pycspr.serialisation import cl_u8
from pycspr.serialisation import cl_u32
from pycspr.serialisation import cl_u64
from pycspr.serialisation import cl_u128
from pycspr.serialisation import cl_u256
from pycspr.serialisation import cl_u512
from pycspr.serialisation import cl_unit
from pycspr.serialisation import cl_uref
from pycspr.serialisation import cl_vector
from pycspr.types import CLTypeKey
from pycspr.types import List


# Map: CL type key <-> list item serialiser.
_ITEM_SERIALISERS = {
    CLTypeKey.ANY: cl_any,
    CLTypeKey.BOOL: cl_bool,
    CLTypeKey.BYTE_ARRAY: cl_byte_array,
    CLTypeKey.I32: cl_i32,
    CLTypeKey.I64: cl_i64,
    CLTypeKey.KEY: cl_key,
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


def from_bytes(value: bytes) -> List:
    raise NotImplementedError()


def to_bytes(value: List) -> bytes:
    item_serialiser = _ITEM_SERIALISERS[value.item_type.type_key]

    return cl_vector.to_bytes([item_serialiser.to_bytes(i) for i in value.items])


def from_json(value: dict) -> List:
    raise NotImplementedError()


def to_json(value: List) -> dict:
    item_serialiser = _ITEM_SERIALISERS[value.item_type]

    return [item_serialiser.to_json(i) for i in value.items]
