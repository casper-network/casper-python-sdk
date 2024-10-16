import typing

from pycspr.types.cl import CLT_TypeKey
from pycspr.types.cl import CLT_U64
from pycspr.types.cl import CLV_Value
from pycspr.types.cl import CLV_Bool
from pycspr.types.cl import CLV_ByteArray
from pycspr.types.cl import CLV_I32
from pycspr.types.cl import CLV_I64
from pycspr.types.cl import CLV_U8
from pycspr.types.cl import CLV_U32
from pycspr.types.cl import CLV_U64
from pycspr.types.cl import CLV_U128
from pycspr.types.cl import CLV_U256
from pycspr.types.cl import CLV_U512
from pycspr.types.cl import CLV_Key
from pycspr.types.cl import CLV_List
from pycspr.types.cl import CLV_Map
from pycspr.types.cl import CLV_Option
from pycspr.types.cl import CLV_PublicKey
from pycspr.types.cl import CLV_String
from pycspr.types.cl import CLV_Tuple1
from pycspr.types.cl import CLV_Tuple2
from pycspr.types.cl import CLV_Tuple3
from pycspr.types.cl import CLV_Unit
from pycspr.types.cl import CLV_URef
from pycspr.crypto.types import PublicKey


def yield_cl_values(fixtures: list) -> typing.Iterator[CLV_Value]:
    for fixture in fixtures:
        type_key: str = fixture["cl_type"]
        value: str = fixture["value"]

        if type_key == CLT_TypeKey.ANY:
            continue

        elif type_key == CLT_TypeKey.BOOL:
            yield CLV_Bool(value)

        elif type_key == CLT_TypeKey.BYTE_ARRAY:
            yield CLV_ByteArray(bytes.fromhex(value))

        elif type_key == CLT_TypeKey.I32:
            yield CLV_I32(value)

        elif type_key == CLT_TypeKey.I64:
            yield CLV_I64(value)

        elif type_key == CLT_TypeKey.KEY:
            yield CLV_Key.from_str(value)

        elif type_key == CLT_TypeKey.LIST:
            yield CLV_List([CLV_U64(i) for i in value])

        elif type_key == CLT_TypeKey.MAP:
            yield CLV_Map(
                [(CLV_String(k), CLV_U64(v)) for k, v in value.items()]
            )

        elif type_key == CLT_TypeKey.OPTION:
            yield CLV_Option(CLV_U64(value), CLT_U64())

        elif type_key == CLT_TypeKey.PUBLIC_KEY:
            yield CLV_PublicKey.from_public_key(
                PublicKey.from_bytes(bytes.fromhex(value))
                )

        elif type_key == CLT_TypeKey.RESULT:
            continue

        elif type_key == CLT_TypeKey.STRING:
            yield CLV_String(value)

        elif type_key == CLT_TypeKey.TUPLE_1:
            yield CLV_Tuple1(
                CLV_U64(value[0])
                )

        elif type_key == CLT_TypeKey.TUPLE_2:
            yield CLV_Tuple2(
                CLV_U64(value[0]),
                CLV_U128(value[1])
                )

        elif type_key == CLT_TypeKey.TUPLE_3:
            yield CLV_Tuple3(
                CLV_U64(value[0]),
                CLV_U128(value[1]),
                CLV_U256(value[2])
                )

        elif type_key == CLT_TypeKey.U8:
            yield CLV_U8(value)

        elif type_key == CLT_TypeKey.U32:
            yield CLV_U32(value)

        elif type_key == CLT_TypeKey.U64:
            yield CLV_U64(value)

        elif type_key == CLT_TypeKey.U128:
            yield CLV_U128(value)

        elif type_key == CLT_TypeKey.U256:
            yield CLV_U256(value)

        elif type_key == CLT_TypeKey.U512:
            yield CLV_U512(value)

        elif type_key == CLT_TypeKey.UNIT:
            yield CLV_Unit()

        elif type_key == CLT_TypeKey.UREF:
            yield CLV_URef.from_str(value)
