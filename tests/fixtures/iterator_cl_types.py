import typing

from pycspr.types.cl import CLT_Type
from pycspr.types.cl import CLT_TypeKey
from pycspr.types.cl import CLT_Any
from pycspr.types.cl import CLT_Bool
from pycspr.types.cl import CLT_ByteArray
from pycspr.types.cl import CLT_I32
from pycspr.types.cl import CLT_I64
from pycspr.types.cl import CLT_Type_U8
from pycspr.types.cl import CLT_Type_U32
from pycspr.types.cl import CLT_Type_U64
from pycspr.types.cl import CLT_Type_U128
from pycspr.types.cl import CLT_Type_U256
from pycspr.types.cl import CLT_Type_U512
from pycspr.types.cl import CLT_Type_Key
from pycspr.types.cl import CLT_Type_List
from pycspr.types.cl import CLT_Type_Map
from pycspr.types.cl import CLT_Type_Option
from pycspr.types.cl import CLT_Type_PublicKey
from pycspr.types.cl import CLT_Type_Result
from pycspr.types.cl import CLT_Type_String
from pycspr.types.cl import CLT_Type_Tuple1
from pycspr.types.cl import CLT_Type_Tuple2
from pycspr.types.cl import CLT_Type_Tuple3
from pycspr.types.cl import CLT_Type_Unit
from pycspr.types.cl import CLT_Type_URef


def yield_cl_types(fixtures: list) -> typing.Iterator[CLT_Type]:
    for fixture in fixtures:
        type_key = fixture["cl_type"]

        if type_key == CLT_TypeKey.ANY:
            yield CLT_Any()

        elif type_key == CLT_TypeKey.BOOL:
            yield CLT_Bool()

        elif type_key == CLT_TypeKey.BYTE_ARRAY:
            yield CLT_ByteArray(fixture["cl_type_size"])

        elif type_key == CLT_TypeKey.I32:
            yield CLT_I32()

        elif type_key == CLT_TypeKey.I64:
            yield CLT_I64()

        elif type_key == CLT_TypeKey.KEY:
            yield CLT_Type_Key()

        elif type_key == CLT_TypeKey.LIST:
            for inner_type in _get_inner_types():
                yield CLT_Type_List(inner_type)

        elif type_key == CLT_TypeKey.MAP:
            yield CLT_Type_Map(CLT_Type_String(), CLT_I32())

        elif type_key == CLT_TypeKey.OPTION:
            for inner_type in _get_inner_types():
                yield CLT_Type_Option(inner_type)

        elif type_key == CLT_TypeKey.PUBLIC_KEY:
            yield CLT_Type_PublicKey()

        elif type_key == CLT_TypeKey.RESULT:
            yield CLT_Type_Result()

        elif type_key == CLT_TypeKey.STRING:
            yield CLT_Type_String()

        elif type_key == CLT_TypeKey.TUPLE_1:
            yield CLT_Type_Tuple1(CLT_Type_U64())

        elif type_key == CLT_TypeKey.TUPLE_2:
            yield CLT_Type_Tuple2(CLT_Type_U64(), CLT_Type_U128())

        elif type_key == CLT_TypeKey.TUPLE_3:
            yield CLT_Type_Tuple3(
                CLT_Type_U64(), CLT_Type_U128(), CLT_Type_U256()
                )

        elif type_key == CLT_TypeKey.U8:
            yield CLT_Type_U8()

        elif type_key == CLT_TypeKey.U32:
            yield CLT_Type_U32()

        elif type_key == CLT_TypeKey.U64:
            yield CLT_Type_U64()

        elif type_key == CLT_TypeKey.U128:
            yield CLT_Type_U128()

        elif type_key == CLT_TypeKey.U256:
            yield CLT_Type_U256()

        elif type_key == CLT_TypeKey.U512:
            yield CLT_Type_U512()

        elif type_key == CLT_TypeKey.UNIT:
            yield CLT_Type_Unit()

        elif type_key == CLT_TypeKey.UREF:
            yield CLT_Type_URef()


def _get_inner_types():
    return [
        CLT_Any(),
        CLT_Bool(),
        CLT_ByteArray(32),
        CLT_I32(),
        CLT_I64(),
        CLT_Type_Key(),
        CLT_Type_List(CLT_Type_U64()),
        CLT_Type_Map(CLT_Type_String(), CLT_I32()),
        CLT_Type_PublicKey(),
        CLT_Type_Result(),
        CLT_Type_String(),
        CLT_Type_Tuple1(CLT_Type_U64()),
        CLT_Type_Tuple2(CLT_Type_U64(), CLT_Type_U128()),
        CLT_Type_Tuple3(CLT_Type_U64(), CLT_Type_U128(), CLT_Type_U256()),
        CLT_Type_U8(),
        CLT_Type_U32(),
        CLT_Type_U64(),
        CLT_Type_U128(),
        CLT_Type_U256(),
        CLT_Type_U512(),
        CLT_Type_Unit(),
        CLT_Type_URef(),
    ]
