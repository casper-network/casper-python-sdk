import typing

from pycspr import types
from pycspr.types import CL_TypeKey
from pycspr.types import CL_Value


def yield_cl_values(fixtures: list) -> typing.Iterator[CL_Value]:
    for fixture in fixtures:
        type_key = fixture["cl_type"]
        value = fixture["value"]

        if type_key == CL_TypeKey.ANY:
            continue

        elif type_key == CL_TypeKey.BOOL:
            yield types.CL_Bool(value)

        elif type_key == CL_TypeKey.BYTE_ARRAY:
            yield types.CL_ByteArray(bytes.fromhex(value))

        elif type_key == CL_TypeKey.I32:
            yield types.CL_I32(value)

        elif type_key == CL_TypeKey.I64:
            yield types.CL_I64(value)

        elif type_key == CL_TypeKey.KEY:
            yield types.CL_Key.from_string(value)

        elif type_key == CL_TypeKey.LIST:
            yield types.CL_List([types.CL_U64(i) for i in value])

        elif type_key == CL_TypeKey.MAP:
            yield types.CL_Map(
                [(types.CL_String(k), types.CL_U64(v)) for k, v in value.items()]
            )

        elif type_key == CL_TypeKey.OPTION:
            yield types.CL_Option(types.CL_U64(value), types.CL_Type_U64())

        elif type_key == CL_TypeKey.PUBLIC_KEY:
            yield types.CL_PublicKey.from_account_key(bytes.fromhex(value))

        elif type_key == CL_TypeKey.RESULT:
            continue

        elif type_key == CL_TypeKey.STRING:
            yield types.CL_String(value)

        elif type_key == CL_TypeKey.TUPLE_1:
            yield types.CL_Tuple1(
                types.CL_U64(value[0])
                )

        elif type_key == CL_TypeKey.TUPLE_2:
            yield types.CL_Tuple2(
                types.CL_U64(value[0]),
                types.CL_U128(value[1])
                )

        elif type_key == CL_TypeKey.TUPLE_3:
            yield types.CL_Tuple3(
                types.CL_U64(value[0]),
                types.CL_U128(value[1]),
                types.CL_U256(value[2])
                )

        elif type_key == CL_TypeKey.U8:
            yield types.CL_U8(value)

        elif type_key == CL_TypeKey.U32:
            yield types.CL_U32(value)

        elif type_key == CL_TypeKey.U64:
            yield types.CL_U64(value)

        elif type_key == CL_TypeKey.U128:
            yield types.CL_U128(value)

        elif type_key == CL_TypeKey.U256:
            yield types.CL_U256(value)

        elif type_key == CL_TypeKey.U512:
            yield types.CL_U512(value)

        elif type_key == CL_TypeKey.UNIT:
            yield types.CL_Unit()

        elif type_key == CL_TypeKey.UREF:
            yield types.CL_URef.from_string(value)
