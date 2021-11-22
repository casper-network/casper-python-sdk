import typing

from pycspr import types
from pycspr.types import CL_Type
from pycspr.types import CL_TypeKey
from pycspr.types import CL_Value


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
            yield types.CL_Type_List(types.CL_Type_Any())
            yield types.CL_Type_List(types.CL_Type_Bool())
            yield types.CL_Type_List(types.CL_Type_ByteArray(32))
            yield types.CL_Type_List(types.CL_Type_I32())
            yield types.CL_Type_List(types.CL_Type_I64())
            yield types.CL_Type_List(types.CL_Type_Key())
            # yield types.CL_Type_List(
            # types.CL_Type_Map(types.CL_Type_String(), types.CL_Type_I32())
            # )
            yield types.CL_Type_List(types.CL_Type_PublicKey())
            yield types.CL_Type_List(types.CL_Type_Result())
            yield types.CL_Type_List(types.CL_Type_String())
            # yield types.CL_Type_List(
            # types.CL_Type_Tuple1(types.CL_Type_Boolean())
            # )
            # yield types.CL_Type_List(
            # types.CL_Type_Tuple2(types.CL_Type_Boolean(), types.CL_Type_I32())
            # )
            # yield types.CL_Type_List(
            # types.CL_Type_Tuple3(types.CL_Type_Boolean(),types.CL_Type_I32(), types.CL_Type_String())
            # )
            yield types.CL_Type_List(types.CL_Type_U8())
            yield types.CL_Type_List(types.CL_Type_U32())
            yield types.CL_Type_List(types.CL_Type_U64())
            yield types.CL_Type_List(types.CL_Type_U128())
            yield types.CL_Type_List(types.CL_Type_U256())
            yield types.CL_Type_List(types.CL_Type_U512())
            yield types.CL_Type_List(types.CL_Type_Unit())
            yield types.CL_Type_List(types.CL_Type_URef())
        elif type_key == CL_TypeKey.MAP:
            continue
            # yield types.CL_Type_Map(types.CL_Type_String(), types.CL_Type_I32())
        elif type_key == CL_TypeKey.OPTION:
            yield types.CL_Type_Option(types.CL_Type_Any())
            yield types.CL_Type_Option(types.CL_Type_Bool())
            yield types.CL_Type_Option(types.CL_Type_ByteArray(32))
            yield types.CL_Type_Option(types.CL_Type_I32())
            yield types.CL_Type_Option(types.CL_Type_I64())
            yield types.CL_Type_Option(types.CL_Type_Key())
            yield types.CL_Type_Option(types.CL_Type_List(types.CL_Type_Bool()))
            # yield types.CL_Type_Option(types.CL_Type_Map(types.CL_Type_String(), types.CL_Type_I32()))
            yield types.CL_Type_Option(types.CL_Type_Option(types.CL_Type_Bool()))
            yield types.CL_Type_Option(types.CL_Type_PublicKey())
            yield types.CL_Type_Option(types.CL_Type_Result())
            yield types.CL_Type_Option(types.CL_Type_String())
            # yield types.CL_Type_Option(types.CL_Type_Tuple1(types.CL_Type_Boolean()))
            # yield types.CL_Type_Option(types.CL_Type_Tuple2(types.CL_Type_Boolean(), types.CL_Type_I32()))
            # yield types.CL_Type_Option(types.CL_Type_Tuple3(types.CL_Type_Boolean(), types.CL_Type_I32(), types.CL_Type_String()))
            yield types.CL_Type_Option(types.CL_Type_U8())
            yield types.CL_Type_Option(types.CL_Type_U32())
            yield types.CL_Type_Option(types.CL_Type_U64())
            yield types.CL_Type_Option(types.CL_Type_U128())
            yield types.CL_Type_Option(types.CL_Type_U256())
            yield types.CL_Type_Option(types.CL_Type_U512())
            yield types.CL_Type_List(types.CL_Type_Unit())
            yield types.CL_Type_List(types.CL_Type_URef())
        elif type_key == CL_TypeKey.PUBLIC_KEY:
            yield types.CL_Type_PublicKey()
        elif type_key == CL_TypeKey.RESULT:
            yield types.CL_Type_Result()
        elif type_key == CL_TypeKey.STRING:
            yield types.CL_Type_String()
        elif type_key == CL_TypeKey.TUPLE_1:
            continue
            # yield types.CL_Type_Tuple1(types.CL_Type_Boolean())
        elif type_key == CL_TypeKey.TUPLE_2:
            continue
            # yield types.CL_Type_Tuple2(types.CL_Type_Boolean(), types.CL_Type_I32())
        elif type_key == CL_TypeKey.TUPLE_3:
            continue
            # yield types.CL_Type_Tuple3(types.CL_Type_Boolean(), types.CL_Type_I32(), types.CL_Type_String())
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
            continue
        elif type_key == CL_TypeKey.MAP:
            continue
        elif type_key == CL_TypeKey.OPTION:
            continue
        elif type_key == CL_TypeKey.PUBLIC_KEY:
            yield types.CL_PublicKey.from_string(value)
        elif type_key == CL_TypeKey.RESULT:
            continue
        elif type_key == CL_TypeKey.STRING:
            yield types.CL_String(value)
        elif type_key == CL_TypeKey.TUPLE_1:
            continue
        elif type_key == CL_TypeKey.TUPLE_2:
            continue
        elif type_key == CL_TypeKey.TUPLE_3:
            continue
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
