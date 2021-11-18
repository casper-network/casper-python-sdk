from pycspr.types import CL_Type
from pycspr.types import CL_Type_Any
from pycspr.types import CL_Type_Bool
from pycspr.types import CL_Type_ByteArray
from pycspr.types import CL_Type_I32
from pycspr.types import CL_Type_I64
from pycspr.types import CL_Type_Key
from pycspr.types import CL_Type_List
from pycspr.types import CL_Type_Map
from pycspr.types import CL_Type_Option
from pycspr.types import CL_Type_PublicKey
from pycspr.types import CL_Type_Result
from pycspr.types import CL_Type_String
from pycspr.types import CL_Type_Tuple1
from pycspr.types import CL_Type_Tuple2
from pycspr.types import CL_Type_Tuple3
from pycspr.types import CL_Type_U8
from pycspr.types import CL_Type_U32
from pycspr.types import CL_Type_U64
from pycspr.types import CL_Type_U128
from pycspr.types import CL_Type_U256
from pycspr.types import CL_Type_U512
from pycspr.types import CL_Type_Unit
from pycspr.types import CL_Type_URef


def any() -> CL_Type_Any:
    return CL_Type_Any()


def boolean() -> CL_Type_Bool:
    return CL_Type_Bool()


def byte_array(size: int) -> CL_Type_ByteArray:
    return CL_Type_ByteArray(size=size)


def i32() -> CL_Type_I32:
    return CL_Type_I32()


def i64() -> CL_Type_I64:
    return CL_Type_I64()


def key() -> CL_Type_Key:
    return CL_Type_Key()


def list(inner_type: CL_Type) -> CL_Type_List:
    return CL_Type_List(inner_type=inner_type)


def map(key_type: CL_Type, value_type: CL_Type) -> CL_Type_Map:
    return CL_Type_Map(key_type=key_type, value_type=value_type)


def option(inner_type: CL_Type) -> CL_Type_Option:
    return CL_Type_Option(inner_type=inner_type)


def public_key() -> CL_Type_PublicKey:
    return CL_Type_PublicKey()


def result() -> CL_Type_Result:
    return CL_Type_Result()


def string() -> CL_Type_String:
    return CL_Type_String()


def tuple_1(t0_type: CL_Type) -> CL_Type_Tuple1:
    return CL_Type_Tuple1(t0_type=t0_type)


def tuple_2(t0_type: CL_Type, t1_type: CL_Type) -> CL_Type_Tuple2:
    return CL_Type_Tuple2(t0_type=t0_type, t1_type=t1_type)


def tuple_3(t0_type: CL_Type, t1_type: CL_Type, t2_type: CL_Type) -> CL_Type_Tuple3:
    return CL_Type_Tuple3(t0_type=t0_type, t1_type=t1_type, t2_type=t2_type)


def u8() -> CL_Type_U8:
    return CL_Type_U8()


def u32() -> CL_Type_U32:
    return CL_Type_U32()


def u64() -> CL_Type_U64:
    return CL_Type_U64()


def u128() -> CL_Type_U128:
    return CL_Type_U128()


def u256() -> CL_Type_U256:
    return CL_Type_U256()


def u512() -> CL_Type_U512:
    return CL_Type_U512()


def unit() -> CL_Type_Unit:
    return CL_Type_Unit()


def uref() -> CL_Type_URef:
    return CL_Type_URef()
