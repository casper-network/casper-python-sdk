from pycspr.types import CLTypeKey
from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3


def boolean() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.BOOL)


def byte_array(size: int) -> CLType_ByteArray:
    return CLType_ByteArray(size=size)


def i32() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.I32)


def i64() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.I64)


def key() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.KEY)


def list(inner_type: CLType) -> CLType_List:
    return CLType_List(inner_type=inner_type)


def map(key_type: CLType, value_type: CLType) -> CLType_Map:
    return CLType_Map(key_type=key_type, value_type=value_type)


def option(inner_type: CLType) -> CLType_Option:
    return CLType_Option(inner_type=inner_type)


def public_key() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.PUBLIC_KEY)


def simple(type_key: CLTypeKey) -> CLType_Simple:
    return CLType_Simple(type_key)


def string() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.STRING)


def tuple_1(t0_type: CLType) -> CLType_Tuple1:
    return CLType_Tuple1(t0_type=t0_type)


def tuple_2(t0_type: CLType, t1_type: CLType) -> CLType_Tuple2:
    return CLType_Tuple2(t0_type=t0_type, t1_type=t1_type)


def tuple_3(t0_type: CLType, t1_type: CLType, t2_type: CLType) -> CLType_Tuple3:
    return CLType_Tuple3(t0_type=t0_type, t1_type=t1_type, t2_type=t2_type)


def u8() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.U8)


def u32() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.U32)


def u64() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.U64)


def u128() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.U128)


def u256() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.U256)


def u512() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.U512)


def unit() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.UNIT)


def uref() -> CLType_Simple:
    return CLType_Simple(CLTypeKey.UREF)
