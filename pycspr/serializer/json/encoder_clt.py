import typing

from pycspr.type_defs.cl_types import CLT_Type
from pycspr.type_defs.cl_types import CLT_TypeKey


def encode(entity: CLT_Type) -> typing.Union[str, dict]:
    """Encodes a domain entity instance to a JSON encodeable dictionary.

    :param entity: A Cl type related type instance to be encoded.
    :returns: A JSON encodeable dictionary.

    """
    try:
        encoder = _ENCODERS[entity.type_key]
    except KeyError:
        raise ValueError("Invalid CL type")
    else:
        return encoder(entity)


_ENCODERS: dict = {
    CLT_TypeKey.ANY:
        lambda _: "Any",
    CLT_TypeKey.BOOL:
        lambda _: "Bool",
    CLT_TypeKey.BYTE_ARRAY:
        lambda x: {
            "ByteArray": x.size
        },
    CLT_TypeKey.I32:
        lambda _: "I32",
    CLT_TypeKey.I64:
        lambda _: "I64",
    CLT_TypeKey.KEY:
        lambda _: "Key",
    CLT_TypeKey.LIST:
        lambda x: {
            "List": encode(x.inner_type)
        },
    CLT_TypeKey.MAP:
        lambda x: {
            "Map": {
                "key": encode(x.key_type),
                "value": encode(x.value_type)
            }
        },
    CLT_TypeKey.OPTION:
        lambda x: {
            "Option": encode(x.inner_type)
        },
    CLT_TypeKey.PUBLIC_KEY:
        lambda _: "PublicKey",
    CLT_TypeKey.RESULT:
        lambda _: "Result",
    CLT_TypeKey.STRING:
        lambda _: "String",
    CLT_TypeKey.TUPLE_1:
        lambda x: {
            "Tuple1": encode(x.t0_type)
        },
    CLT_TypeKey.TUPLE_2:
        lambda x: {
            "Tuple2": [
                encode(x.t0_type),
                encode(x.t1_type),
            ]
        },
    CLT_TypeKey.TUPLE_3:
        lambda x: {
            "Tuple3": [
                encode(x.t0_type),
                encode(x.t1_type),
                encode(x.t2_type)
            ]
        },
    CLT_TypeKey.U8:
        lambda _: "U8",
    CLT_TypeKey.U32:
        lambda _: "U32",
    CLT_TypeKey.U64:
        lambda _: "U64",
    CLT_TypeKey.U128:
        lambda _: "U128",
    CLT_TypeKey.U256:
        lambda _: "U256",
    CLT_TypeKey.U512:
        lambda _: "U512",
    CLT_TypeKey.UNIT:
        lambda _: "Unit",
    CLT_TypeKey.UREF:
        lambda _: "URef",
}
