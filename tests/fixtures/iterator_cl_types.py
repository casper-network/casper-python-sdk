import typing

from pycspr.type_defs.cl_types import CLT_Type
from pycspr.type_defs.cl_types import CLT_TypeKey
from pycspr.type_defs.cl_types import CLT_Any
from pycspr.type_defs.cl_types import CLT_Bool
from pycspr.type_defs.cl_types import CLT_ByteArray
from pycspr.type_defs.cl_types import CLT_I32
from pycspr.type_defs.cl_types import CLT_I64
from pycspr.type_defs.cl_types import CLT_U8
from pycspr.type_defs.cl_types import CLT_U32
from pycspr.type_defs.cl_types import CLT_U64
from pycspr.type_defs.cl_types import CLT_U128
from pycspr.type_defs.cl_types import CLT_U256
from pycspr.type_defs.cl_types import CLT_U512
from pycspr.type_defs.cl_types import CLT_Key
from pycspr.type_defs.cl_types import CLT_List
from pycspr.type_defs.cl_types import CLT_Map
from pycspr.type_defs.cl_types import CLT_Option
from pycspr.type_defs.cl_types import CLT_PublicKey
from pycspr.type_defs.cl_types import CLT_Result
from pycspr.type_defs.cl_types import CLT_String
from pycspr.type_defs.cl_types import CLT_Tuple1
from pycspr.type_defs.cl_types import CLT_Tuple2
from pycspr.type_defs.cl_types import CLT_Tuple3
from pycspr.type_defs.cl_types import CLT_Unit
from pycspr.type_defs.cl_types import CLT_URef


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
            yield CLT_Key()

        elif type_key == CLT_TypeKey.LIST:
            for inner_type in _get_inner_types():
                yield CLT_List(inner_type)

        elif type_key == CLT_TypeKey.MAP:
            yield CLT_Map(CLT_String(), CLT_I32())

        elif type_key == CLT_TypeKey.OPTION:
            for inner_type in _get_inner_types():
                yield CLT_Option(inner_type)

        elif type_key == CLT_TypeKey.PUBLIC_KEY:
            yield CLT_PublicKey()

        elif type_key == CLT_TypeKey.RESULT:
            yield CLT_Result()

        elif type_key == CLT_TypeKey.STRING:
            yield CLT_String()

        elif type_key == CLT_TypeKey.TUPLE_1:
            yield CLT_Tuple1(CLT_U64())

        elif type_key == CLT_TypeKey.TUPLE_2:
            yield CLT_Tuple2(CLT_U64(), CLT_U128())

        elif type_key == CLT_TypeKey.TUPLE_3:
            yield CLT_Tuple3(
                CLT_U64(), CLT_U128(), CLT_U256()
                )

        elif type_key == CLT_TypeKey.U8:
            yield CLT_U8()

        elif type_key == CLT_TypeKey.U32:
            yield CLT_U32()

        elif type_key == CLT_TypeKey.U64:
            yield CLT_U64()

        elif type_key == CLT_TypeKey.U128:
            yield CLT_U128()

        elif type_key == CLT_TypeKey.U256:
            yield CLT_U256()

        elif type_key == CLT_TypeKey.U512:
            yield CLT_U512()

        elif type_key == CLT_TypeKey.UNIT:
            yield CLT_Unit()

        elif type_key == CLT_TypeKey.UREF:
            yield CLT_URef()


def _get_inner_types():
    return [
        CLT_Any(),
        CLT_Bool(),
        CLT_ByteArray(32),
        CLT_I32(),
        CLT_I64(),
        CLT_Key(),
        CLT_List(CLT_U64()),
        CLT_Map(CLT_String(), CLT_I32()),
        CLT_PublicKey(),
        CLT_Result(),
        CLT_String(),
        CLT_Tuple1(CLT_U64()),
        CLT_Tuple2(CLT_U64(), CLT_U128()),
        CLT_Tuple3(CLT_U64(), CLT_U128(), CLT_U256()),
        CLT_U8(),
        CLT_U32(),
        CLT_U64(),
        CLT_U128(),
        CLT_U256(),
        CLT_U512(),
        CLT_Unit(),
        CLT_URef(),
    ]
