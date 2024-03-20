import typing

from pycspr.types.cl import CL_TypeKey
from pycspr.types.cl import CL_Type_U64
from pycspr.types.cl import CL_Value
from pycspr.types.cl import CL_Bool
from pycspr.types.cl import CL_ByteArray
from pycspr.types.cl import CL_I32
from pycspr.types.cl import CL_I64
from pycspr.types.cl import CL_U8
from pycspr.types.cl import CL_U32
from pycspr.types.cl import CL_U64
from pycspr.types.cl import CL_U128
from pycspr.types.cl import CL_U256
from pycspr.types.cl import CL_U512
from pycspr.types.cl import CL_Key
from pycspr.types.cl import CL_List
from pycspr.types.cl import CL_Map
from pycspr.types.cl import CL_Option
from pycspr.types.cl import CL_PublicKey
from pycspr.types.cl import CL_String
from pycspr.types.cl import CL_Tuple1
from pycspr.types.cl import CL_Tuple2
from pycspr.types.cl import CL_Tuple3
from pycspr.types.cl import CL_Unit
from pycspr.types.cl import CL_URef


def yield_cl_values(fixtures: list) -> typing.Iterator[CL_Value]:
    for fixture in fixtures:
        type_key = fixture["cl_type"]
        value = fixture["value"]

        if type_key == CL_TypeKey.ANY:
            continue

        elif type_key == CL_TypeKey.BOOL:
            yield CL_Bool(value)

        elif type_key == CL_TypeKey.BYTE_ARRAY:
            yield CL_ByteArray(bytes.fromhex(value))

        elif type_key == CL_TypeKey.I32:
            yield CL_I32(value)

        elif type_key == CL_TypeKey.I64:
            yield CL_I64(value)

        elif type_key == CL_TypeKey.KEY:
            yield CL_Key.from_string(value)

        elif type_key == CL_TypeKey.LIST:
            yield CL_List([CL_U64(i) for i in value])

        elif type_key == CL_TypeKey.MAP:
            yield CL_Map(
                [(CL_String(k), CL_U64(v)) for k, v in value.items()]
            )

        elif type_key == CL_TypeKey.OPTION:
            yield CL_Option(CL_U64(value), CL_Type_U64())

        elif type_key == CL_TypeKey.PUBLIC_KEY:
            yield CL_PublicKey.from_account_key(bytes.fromhex(value))

        elif type_key == CL_TypeKey.RESULT:
            continue

        elif type_key == CL_TypeKey.STRING:
            yield CL_String(value)

        elif type_key == CL_TypeKey.TUPLE_1:
            yield CL_Tuple1(
                CL_U64(value[0])
                )

        elif type_key == CL_TypeKey.TUPLE_2:
            yield CL_Tuple2(
                CL_U64(value[0]),
                CL_U128(value[1])
                )

        elif type_key == CL_TypeKey.TUPLE_3:
            yield CL_Tuple3(
                CL_U64(value[0]),
                CL_U128(value[1]),
                CL_U256(value[2])
                )

        elif type_key == CL_TypeKey.U8:
            yield CL_U8(value)

        elif type_key == CL_TypeKey.U32:
            yield CL_U32(value)

        elif type_key == CL_TypeKey.U64:
            yield CL_U64(value)

        elif type_key == CL_TypeKey.U128:
            yield CL_U128(value)

        elif type_key == CL_TypeKey.U256:
            yield CL_U256(value)

        elif type_key == CL_TypeKey.U512:
            yield CL_U512(value)

        elif type_key == CL_TypeKey.UNIT:
            yield CL_Unit()

        elif type_key == CL_TypeKey.UREF:
            yield CL_URef.from_string(value)
