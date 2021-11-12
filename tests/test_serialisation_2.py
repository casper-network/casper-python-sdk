import typing

from pycspr import serialisation
from pycspr.factory import create_cl_value
from pycspr.types import CLTypeKey
from pycspr.types import CLValue


def test_that_cl_values_serialise_to_bytes(cl_values_vector):
    for value in _yield_cl_values(cl_values_vector.fixtures):
        if not value:
            continue
        assert value == serialisation.from_bytes(serialisation.to_bytes(value))


def test_that_cl_values_serialise_to_json(cl_values_vector):
    for value in _yield_cl_values(cl_values_vector.fixtures):
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
            yield create_cl_value.boolean(value)
        elif type_key == CLTypeKey.BYTE_ARRAY:
            yield create_cl_value.byte_array(bytes.fromhex(value))
        elif type_key == CLTypeKey.I32:
            yield create_cl_value.i32(value)
        elif type_key == CLTypeKey.I64:
            yield create_cl_value.i64(value)
        elif type_key == CLTypeKey.KEY:
            yield create_cl_value.key_from_string(value)
        elif type_key == CLTypeKey.LIST:
            yield None
        elif type_key == CLTypeKey.MAP:
            yield None
        elif type_key == CLTypeKey.OPTION:
            yield None
        elif type_key == CLTypeKey.PUBLIC_KEY:
            yield create_cl_value.public_key(bytes.fromhex(value))
        elif type_key == CLTypeKey.RESULT:
            yield None
        elif type_key == CLTypeKey.STRING:
            yield create_cl_value.string(value)
        elif type_key == CLTypeKey.TUPLE_1:
            yield None
        elif type_key == CLTypeKey.TUPLE_2:
            yield None
        elif type_key == CLTypeKey.TUPLE_3:
            yield None
        elif type_key == CLTypeKey.U8:
            yield create_cl_value.u8(value)
        elif type_key == CLTypeKey.U32:
            yield create_cl_value.u32(value)
        elif type_key == CLTypeKey.U64:
            yield create_cl_value.u64(value)
        elif type_key == CLTypeKey.U128:
            yield create_cl_value.u128(value)
        elif type_key == CLTypeKey.U256:
            yield create_cl_value.u256(value)
        elif type_key == CLTypeKey.U512:
            yield create_cl_value.u512(value)
        elif type_key == CLTypeKey.UNIT:
            yield create_cl_value.unit()
        elif type_key == CLTypeKey.UREF:
            yield create_cl_value.uref_from_string(value)
