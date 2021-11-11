from pycspr.types import CLType
from pycspr.types import CLType_Any
from pycspr.types import CLType_Boolean
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_I32
from pycspr.types import CLType_I64
from pycspr.types import CLType_Key
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_PublicKey
from pycspr.types import CLType_Result
from pycspr.types import CLType_String
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3
from pycspr.types import CLType_U8
from pycspr.types import CLType_U32
from pycspr.types import CLType_U64
from pycspr.types import CLType_U128
from pycspr.types import CLType_U256
from pycspr.types import CLType_U512
from pycspr.types import CLType_Unit
from pycspr.types import CLType_URef


def any() -> CLType_Any:
    return CLType_Any()


def boolean() -> CLType_Boolean:
    return CLType_Boolean()


def byte_array(size: int) -> CLType_ByteArray:
    return CLType_ByteArray(size=size)


def i32() -> CLType_I32:
    return CLType_I32()


def i64() -> CLType_I64:
    return CLType_I64()


def key() -> CLType_Key:
    return CLType_Key()


def list(inner_type: CLType) -> CLType_List:
    return CLType_List(inner_type=inner_type)


def map(key_type: CLType, value_type: CLType) -> CLType_Map:
    return CLType_Map(key_type=key_type, value_type=value_type)


def option(inner_type: CLType) -> CLType_Option:
    return CLType_Option(inner_type=inner_type)


def public_key() -> CLType_PublicKey:
    return CLType_PublicKey()


def result() -> CLType_Result:
    return CLType_Result()


def string() -> CLType_String:
    return CLType_String()


def tuple_1(t0_type: CLType) -> CLType_Tuple1:
    return CLType_Tuple1(t0_type=t0_type)


def tuple_2(t0_type: CLType, t1_type: CLType) -> CLType_Tuple2:
    return CLType_Tuple2(t0_type=t0_type, t1_type=t1_type)


def tuple_3(t0_type: CLType, t1_type: CLType, t2_type: CLType) -> CLType_Tuple3:
    return CLType_Tuple3(t0_type=t0_type, t1_type=t1_type, t2_type=t2_type)


def u8() -> CLType_U8:
    return CLType_U8()


def u32() -> CLType_U32:
    return CLType_U32()


def u64() -> CLType_U64:
    return CLType_U64()


def u128() -> CLType_U128:
    return CLType_U128()


def u256() -> CLType_U256:
    return CLType_U256()


def u512() -> CLType_U512:
    return CLType_U512()


def unit() -> CLType_Unit:
    return CLType_Unit()


def uref() -> CLType_URef:
    return CLType_URef()
