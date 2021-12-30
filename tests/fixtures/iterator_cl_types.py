import typing

from pycspr import types
from pycspr.types import CL_Type
from pycspr.types import CL_TypeKey


def yield_cl_types(fixtures: list) -> typing.Iterator[CL_Type]:
    for fixture in fixtures:
        type_key = fixture["cl_type"]

        if type_key == CL_TypeKey.ANY:
            yield types.CL_Type_Any()

        elif type_key == CL_TypeKey.BOOL:
            yield types.CL_Type_Bool()

        elif type_key == CL_TypeKey.BYTE_ARRAY:
            yield types.CL_Type_ByteArray(fixture["cl_type_size"])

        elif type_key == CL_TypeKey.I32:
            yield types.CL_Type_I32()

        elif type_key == CL_TypeKey.I64:
            yield types.CL_Type_I64()

        elif type_key == CL_TypeKey.KEY:
            yield types.CL_Type_Key()

        elif type_key == CL_TypeKey.LIST:
            for inner_type in _get_inner_types():
                yield types.CL_Type_List(inner_type)

        elif type_key == CL_TypeKey.MAP:
            yield types.CL_Type_Map(types.CL_Type_String(), types.CL_Type_I32())

        elif type_key == CL_TypeKey.OPTION:
            for inner_type in _get_inner_types():
                yield types.CL_Type_Option(inner_type)

        elif type_key == CL_TypeKey.PUBLIC_KEY:
            yield types.CL_Type_PublicKey()

        elif type_key == CL_TypeKey.RESULT:
            yield types.CL_Type_Result()

        elif type_key == CL_TypeKey.STRING:
            yield types.CL_Type_String()

        elif type_key == CL_TypeKey.TUPLE_1:
            yield types.CL_Type_Tuple1(types.CL_Type_U64())

        elif type_key == CL_TypeKey.TUPLE_2:
            yield types.CL_Type_Tuple2(types.CL_Type_U64(), types.CL_Type_U128())

        elif type_key == CL_TypeKey.TUPLE_3:
            yield types.CL_Type_Tuple3(
                types.CL_Type_U64(), types.CL_Type_U128(), types.CL_Type_U256()
                )

        elif type_key == CL_TypeKey.U8:
            yield types.CL_Type_U8()

        elif type_key == CL_TypeKey.U32:
            yield types.CL_Type_U32()

        elif type_key == CL_TypeKey.U64:
            yield types.CL_Type_U64()

        elif type_key == CL_TypeKey.U128:
            yield types.CL_Type_U128()

        elif type_key == CL_TypeKey.U256:
            yield types.CL_Type_U256()

        elif type_key == CL_TypeKey.U512:
            yield types.CL_Type_U512()

        elif type_key == CL_TypeKey.UNIT:
            yield types.CL_Type_Unit()

        elif type_key == CL_TypeKey.UREF:
            yield types.CL_Type_URef()


def _get_inner_types():
    return [
        types.CL_Type_Any(),
        types.CL_Type_Bool(),
        types.CL_Type_ByteArray(32),
        types.CL_Type_I32(),
        types.CL_Type_I64(),
        types.CL_Type_Key(),
        types.CL_Type_List(types.CL_Type_U64()),
        types.CL_Type_Map(types.CL_Type_String(), types.CL_Type_I32()),
        types.CL_Type_PublicKey(),
        types.CL_Type_Result(),
        types.CL_Type_String(),
        types.CL_Type_Tuple1(types.CL_Type_U64()),
        types.CL_Type_Tuple2(types.CL_Type_U64(), types.CL_Type_U128()),
        types.CL_Type_Tuple3(types.CL_Type_U64(), types.CL_Type_U128(), types.CL_Type_U256()),
        types.CL_Type_U8(),
        types.CL_Type_U32(),
        types.CL_Type_U64(),
        types.CL_Type_U128(),
        types.CL_Type_U256(),
        types.CL_Type_U512(),
        types.CL_Type_Unit(),
        types.CL_Type_URef(),
    ]
