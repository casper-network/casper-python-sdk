from pycspr import factory
from pycspr.serialisation import cl_type as serialiser


def test_that_cl_types_serialise_as_bytes_correctly():
    for fixture in [i() for i in _FIXTURES]:
        _assert(fixture, bytes, serialiser.to_bytes, serialiser.from_bytes)


def test_that_cl_types_serialise_as_json_correctly():
    for fixture in [i() for i in _FIXTURES]:
        _assert(fixture, (dict, str), serialiser.to_json, serialiser.from_json)


def _assert(fixture, encoding, encoder, decoder):
    encoded = encoder(fixture)
    assert isinstance(encoded, encoding)
    decoded = decoder(encoded)
    assert isinstance(decoded, type(fixture))
    assert encoded == encoder(decoded)


_FIXTURES = [
    lambda: factory.cl_type.any(),
    lambda: factory.cl_type.boolean(),
    lambda: factory.cl_type.byte_array(32),
    lambda: factory.cl_type.i32(),
    lambda: factory.cl_type.i64(),
    lambda: factory.cl_type.key(),
    lambda: factory.cl_type.list(
        factory.cl_type.i64()
        ),
    lambda: factory.cl_type.map(
        factory.cl_type.string(),
        factory.cl_type.i64()
        ),
    lambda: factory.cl_type.option(
        factory.cl_type.i64()
        ),
    lambda: factory.cl_type.public_key(),
    lambda: factory.cl_type.result(),
    lambda: factory.cl_type.string(),
    lambda: factory.cl_type.tuple_1(
        factory.cl_type.string()
    ),
    lambda: factory.cl_type.tuple_2(
        factory.cl_type.string(),
        factory.cl_type.i64()
    ),
    lambda: factory.cl_type.tuple_3(
        factory.cl_type.string(),
        factory.cl_type.i64(),
        factory.cl_type.boolean()
    ),
    lambda: factory.cl_type.u8(),
    lambda: factory.cl_type.u32(),
    lambda: factory.cl_type.u64(),
    lambda: factory.cl_type.u128(),
    lambda: factory.cl_type.u256(),
    lambda: factory.cl_type.u512(),
    lambda: factory.cl_type.unit(),
    lambda: factory.cl_type.uref(),
]


def _get_cl_type(fixture: dict):
    if fixture["cl_type"] == CLTypeKey.ANY:
        return cl_type_factory.any()
    elif fixture["cl_type"] == CLTypeKey.BOOL:
        return cl_type_factory.boolean()
    elif fixture["cl_type"] == CLTypeKey.BYTE_ARRAY:
        return cl_type_factory.byte_array(fixture["cl_type_size"])
    elif fixture["cl_type"] == CLTypeKey.I32:
        return cl_type_factory.i32()
    elif fixture["cl_type"] == CLTypeKey.I64:
        return cl_type_factory.i64()
    elif fixture["cl_type"] == CLTypeKey.KEY:
        return cl_type_factory.key()
    elif fixture["cl_type"] == CLTypeKey.LIST:
        raise NotImplementedError()
    elif fixture["cl_type"] == CLTypeKey.MAP:
        raise NotImplementedError()
    elif fixture["cl_type"] == CLTypeKey.OPTION:
        raise NotImplementedError()
    elif fixture["cl_type"] == CLTypeKey.PUBLIC_KEY:
        return cl_type_factory.public_key()
    elif fixture["cl_type"] == CLTypeKey.RESULT:
        raise NotImplementedError()
    elif fixture["cl_type"] == CLTypeKey.STRING:
        return cl_type_factory.string()
    elif fixture["cl_type"] == CLTypeKey.TUPLE_1:
        raise NotImplementedError()
    elif fixture["cl_type"] == CLTypeKey.TUPLE_2:
        raise NotImplementedError()
    elif fixture["cl_type"] == CLTypeKey.TUPLE_3:
        raise NotImplementedError()
    elif fixture["cl_type"] == CLTypeKey.U8:
        return cl_type_factory.u8()
    elif fixture["cl_type"] == CLTypeKey.U32:
        return cl_type_factory.u32()
    elif fixture["cl_type"] == CLTypeKey.U64:
        return cl_type_factory.u64()
    elif fixture["cl_type"] == CLTypeKey.U128:
        return cl_type_factory.u128()
    elif fixture["cl_type"] == CLTypeKey.U256:
        return cl_type_factory.u256()
    elif fixture["cl_type"] == CLTypeKey.U512:
        return cl_type_factory.u512()
    elif fixture["cl_type"] == CLTypeKey.UNIT:
        return cl_type_factory.unit()
    elif fixture["cl_type"] == CLTypeKey.UREF:
        return cl_type_factory.uref()
