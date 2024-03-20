import typing

from pycspr.types.cl import CL_Type
from pycspr.types.cl import CL_TypeKey
from pycspr.types.cl import CL_Type_Any
from pycspr.types.cl import CL_Type_Bool
from pycspr.types.cl import CL_Type_ByteArray
from pycspr.types.cl import CL_Type_I32
from pycspr.types.cl import CL_Type_I64
from pycspr.types.cl import CL_Type_U8
from pycspr.types.cl import CL_Type_U32
from pycspr.types.cl import CL_Type_U64
from pycspr.types.cl import CL_Type_U128
from pycspr.types.cl import CL_Type_U256
from pycspr.types.cl import CL_Type_U512
from pycspr.types.cl import CL_Type_Key
from pycspr.types.cl import CL_Type_List
from pycspr.types.cl import CL_Type_Map
from pycspr.types.cl import CL_Type_Option
from pycspr.types.cl import CL_Type_PublicKey
from pycspr.types.cl import CL_Type_Result
from pycspr.types.cl import CL_Type_String
from pycspr.types.cl import CL_Type_Tuple1
from pycspr.types.cl import CL_Type_Tuple2
from pycspr.types.cl import CL_Type_Tuple3
from pycspr.types.cl import CL_Type_Unit
from pycspr.types.cl import CL_Type_URef


def yield_cl_types(fixtures: list) -> typing.Iterator[CL_Type]:
    for fixture in fixtures:
        type_key = fixture["cl_type"]

        if type_key == CL_TypeKey.ANY:
            yield CL_Type_Any()

        elif type_key == CL_TypeKey.BOOL:
            yield CL_Type_Bool()

        elif type_key == CL_TypeKey.BYTE_ARRAY:
            yield CL_Type_ByteArray(fixture["cl_type_size"])

        elif type_key == CL_TypeKey.I32:
            yield CL_Type_I32()

        elif type_key == CL_TypeKey.I64:
            yield CL_Type_I64()

        elif type_key == CL_TypeKey.KEY:
            yield CL_Type_Key()

        elif type_key == CL_TypeKey.LIST:
            for inner_type in _get_inner_types():
                yield CL_Type_List(inner_type)

        elif type_key == CL_TypeKey.MAP:
            yield CL_Type_Map(CL_Type_String(), CL_Type_I32())

        elif type_key == CL_TypeKey.OPTION:
            for inner_type in _get_inner_types():
                yield CL_Type_Option(inner_type)

        elif type_key == CL_TypeKey.PUBLIC_KEY:
            yield CL_Type_PublicKey()

        elif type_key == CL_TypeKey.RESULT:
            yield CL_Type_Result()

        elif type_key == CL_TypeKey.STRING:
            yield CL_Type_String()

        elif type_key == CL_TypeKey.TUPLE_1:
            yield CL_Type_Tuple1(CL_Type_U64())

        elif type_key == CL_TypeKey.TUPLE_2:
            yield CL_Type_Tuple2(CL_Type_U64(), CL_Type_U128())

        elif type_key == CL_TypeKey.TUPLE_3:
            yield CL_Type_Tuple3(
                CL_Type_U64(), CL_Type_U128(), CL_Type_U256()
                )

        elif type_key == CL_TypeKey.U8:
            yield CL_Type_U8()

        elif type_key == CL_TypeKey.U32:
            yield CL_Type_U32()

        elif type_key == CL_TypeKey.U64:
            yield CL_Type_U64()

        elif type_key == CL_TypeKey.U128:
            yield CL_Type_U128()

        elif type_key == CL_TypeKey.U256:
            yield CL_Type_U256()

        elif type_key == CL_TypeKey.U512:
            yield CL_Type_U512()

        elif type_key == CL_TypeKey.UNIT:
            yield CL_Type_Unit()

        elif type_key == CL_TypeKey.UREF:
            yield CL_Type_URef()


def _get_inner_types():
    return [
        CL_Type_Any(),
        CL_Type_Bool(),
        CL_Type_ByteArray(32),
        CL_Type_I32(),
        CL_Type_I64(),
        CL_Type_Key(),
        CL_Type_List(CL_Type_U64()),
        CL_Type_Map(CL_Type_String(), CL_Type_I32()),
        CL_Type_PublicKey(),
        CL_Type_Result(),
        CL_Type_String(),
        CL_Type_Tuple1(CL_Type_U64()),
        CL_Type_Tuple2(CL_Type_U64(), CL_Type_U128()),
        CL_Type_Tuple3(CL_Type_U64(), CL_Type_U128(), CL_Type_U256()),
        CL_Type_U8(),
        CL_Type_U32(),
        CL_Type_U64(),
        CL_Type_U128(),
        CL_Type_U256(),
        CL_Type_U512(),
        CL_Type_Unit(),
        CL_Type_URef(),
    ]
