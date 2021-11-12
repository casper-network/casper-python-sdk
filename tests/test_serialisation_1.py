import typing

from pycspr import factory
from pycspr import serialisation
from pycspr.types import CLType
from pycspr.types import CLTypeKey


def test_that_cl_types_serialise_to_bytes(cl_types_vector):
    for value in _yield_cl_types(cl_types_vector.fixtures):
        if not value:
            continue
        assert value == serialisation.from_bytes(serialisation.to_bytes(value))


def test_that_cl_types_serialise_to_json(cl_types_vector):
    for value in _yield_cl_types(cl_types_vector.fixtures):
        if not value:
            continue
        assert value == serialisation.from_json(CLType, serialisation.to_json(value))


def _yield_cl_types(fixtures: list) -> typing.Iterator[CLType]:
    for fixture in fixtures:
        type_key = fixture["cl_type"]
        if type_key == CLTypeKey.ANY:
            yield None
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
            yield None
        elif type_key == CLTypeKey.MAP:
            yield None
        elif type_key == CLTypeKey.OPTION:
            yield None
        elif type_key == CLTypeKey.PUBLIC_KEY:
            yield factory.cl_type.public_key()
        elif type_key == CLTypeKey.RESULT:
            yield None
        elif type_key == CLTypeKey.STRING:
            yield factory.cl_type.string()
        elif type_key == CLTypeKey.TUPLE_1:
            yield None
        elif type_key == CLTypeKey.TUPLE_2:
            yield None
        elif type_key == CLTypeKey.TUPLE_3:
            yield None
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
