import typing

from pycspr import serialisation
from pycspr.factory import cl_value_factory
from pycspr.types import CLTypeKey
from pycspr.types import CLValue


def test_that_cl_values_serialise_as_bytes_correctly(vector_cl_values):
    for value in _yield_cl_values(vector_cl_values.fixtures):
        if not value:
            continue
        assert value == serialisation.from_bytes(serialisation.to_bytes(value))


def test_that_cl_values_serialise_as_json_correctly(vector_cl_values):
    for value in _yield_cl_values(vector_cl_values.fixtures):
        if not value:
            continue
        assert value == serialisation.from_json(CLValue, serialisation.to_json(value))


def _yield_cl_values(fixtures: list) -> typing.Iterator[CLValue]:
    for fixture in fixtures:
        type_key = fixture["cl_type"]
        value = fixture["value"]
        if type_key == CLTypeKey.ANY:
            yield None
        elif type_key == CLTypeKey.BOOL:
            yield cl_value_factory.boolean(value)
        elif type_key == CLTypeKey.BYTE_ARRAY:   
            yield cl_value_factory.byte_array(bytes.fromhex(value))
        elif type_key == CLTypeKey.I32:
            yield cl_value_factory.i32(value)
        elif type_key == CLTypeKey.I64:
            yield cl_value_factory.i64(value)
        elif type_key == CLTypeKey.KEY:
            yield cl_value_factory.key_from_string(value)
        elif type_key == CLTypeKey.LIST:
            yield None
        elif type_key == CLTypeKey.MAP:
            yield None
        elif type_key == CLTypeKey.OPTION:
            yield None
        elif type_key == CLTypeKey.PUBLIC_KEY:
            yield cl_value_factory.public_key(bytes.fromhex(value))
        elif type_key == CLTypeKey.RESULT:
            yield None
        elif type_key == CLTypeKey.STRING:
            yield cl_value_factory.string(value)
        elif type_key == CLTypeKey.TUPLE_1:
            yield None
        elif type_key == CLTypeKey.TUPLE_2:
            yield None
        elif type_key == CLTypeKey.TUPLE_3:
            yield None
        elif type_key == CLTypeKey.U8:
            yield cl_value_factory.u8(value)
        elif type_key == CLTypeKey.U32:
            yield cl_value_factory.u32(value)
        elif type_key == CLTypeKey.U64:
            yield cl_value_factory.u64(value)
        elif type_key == CLTypeKey.U128:
            yield cl_value_factory.u128(value)
        elif type_key == CLTypeKey.U256:
            yield cl_value_factory.u256(value)
        elif type_key == CLTypeKey.U512:
            yield cl_value_factory.u512(value)
        elif type_key == CLTypeKey.UNIT:
            yield cl_value_factory.unit()
        elif type_key == CLTypeKey.UREF:
            yield cl_value_factory.uref_from_string(value)
