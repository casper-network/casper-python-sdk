import typing

from pycspr import factory
from pycspr.types import CLType
from pycspr.types import CLTypeKey
from pycspr.types import CLValue


def yield_cl_types(fixtures: list) -> typing.Iterator[CLType]:
    for fixture in fixtures:
        type_key = fixture["cl_type"]
        if type_key == CLTypeKey.ANY:
            continue
        elif type_key == CLTypeKey.BOOL:
            yield factory.cl_type.boolean()
        elif type_key == CLTypeKey.BYTE_ARRAY:
            yield factory.cl_type.byte_array(fixture["cl_type_size"])
        elif type_key == CLTypeKey.I32:
            yield factory.cl_type.i32()
        elif type_key == CLTypeKey.I64:
            yield factory.cl_type.i64()
        elif type_key == CLTypeKey.KEY:
            yield factory.cl_type.key()
        elif type_key == CLTypeKey.LIST:
            continue
        elif type_key == CLTypeKey.MAP:
            continue
        elif type_key == CLTypeKey.OPTION:
            continue
        elif type_key == CLTypeKey.PUBLIC_KEY:
            yield factory.cl_type.public_key()
        elif type_key == CLTypeKey.RESULT:
            continue
        elif type_key == CLTypeKey.STRING:
            yield factory.cl_type.string()
        elif type_key == CLTypeKey.TUPLE_1:
            continue
        elif type_key == CLTypeKey.TUPLE_2:
            continue
        elif type_key == CLTypeKey.TUPLE_3:
            continue
        elif type_key == CLTypeKey.U8:
            yield factory.cl_type.u8()
        elif type_key == CLTypeKey.U32:
            yield factory.cl_type.u32()
        elif type_key == CLTypeKey.U64:
            yield factory.cl_type.u64()
        elif type_key == CLTypeKey.U128:
            yield factory.cl_type.u128()
        elif type_key == CLTypeKey.U256:
            yield factory.cl_type.u256()
        elif type_key == CLTypeKey.U512:
            yield factory.cl_type.u512()
        elif type_key == CLTypeKey.UNIT:
            yield factory.cl_type.unit()
        elif type_key == CLTypeKey.UREF:
            yield factory.cl_type.uref()


def yield_cl_values(fixtures: list) -> typing.Iterator[CLValue]:
    for fixture in fixtures:
        type_key = fixture["cl_type"]
        value = fixture["value"]
        if type_key == CLTypeKey.ANY:
            continue
        elif type_key == CLTypeKey.BOOL:
            yield factory.create_cl_value.boolean(value)
        elif type_key == CLTypeKey.BYTE_ARRAY:
            yield factory.create_cl_value.byte_array(bytes.fromhex(value))
        elif type_key == CLTypeKey.I32:
            yield factory.create_cl_value.i32(value)
        elif type_key == CLTypeKey.I64:
            yield factory.create_cl_value.i64(value)
        elif type_key == CLTypeKey.KEY:
            yield factory.create_cl_value.key_from_string(value)
        elif type_key == CLTypeKey.LIST:
            continue
        elif type_key == CLTypeKey.MAP:
            continue
        elif type_key == CLTypeKey.OPTION:
            continue
        elif type_key == CLTypeKey.PUBLIC_KEY:
            yield factory.create_cl_value.public_key(bytes.fromhex(value))
        elif type_key == CLTypeKey.RESULT:
            continue
        elif type_key == CLTypeKey.STRING:
            yield factory.create_cl_value.string(value)
        elif type_key == CLTypeKey.TUPLE_1:
            continue
        elif type_key == CLTypeKey.TUPLE_2:
            continue
        elif type_key == CLTypeKey.TUPLE_3:
            continue
        elif type_key == CLTypeKey.U8:
            yield factory.create_cl_value.u8(value)
        elif type_key == CLTypeKey.U32:
            yield factory.create_cl_value.u32(value)
        elif type_key == CLTypeKey.U64:
            yield factory.create_cl_value.u64(value)
        elif type_key == CLTypeKey.U128:
            yield factory.create_cl_value.u128(value)
        elif type_key == CLTypeKey.U256:
            yield factory.create_cl_value.u256(value)
        elif type_key == CLTypeKey.U512:
            yield factory.create_cl_value.u512(value)
        elif type_key == CLTypeKey.UNIT:
            yield factory.create_cl_value.unit()
        elif type_key == CLTypeKey.UREF:
            yield factory.create_cl_value.uref_from_string(value)
