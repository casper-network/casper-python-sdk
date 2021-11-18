import dataclasses
from pycspr.types.cl_types.base import CL_Type
from pycspr.types.cl_types.base import CL_TypeKey

from pycspr.types.cl_types.cl_any import CL_Type_Any
from pycspr.types.cl_types.cl_bool import CL_Type_Bool
from pycspr.types.cl_types.cl_byte_array import CL_Type_ByteArray
from pycspr.types.cl_types.cl_int import CL_Type_I32
from pycspr.types.cl_types.cl_int import CL_Type_I64
from pycspr.types.cl_types.cl_int import CL_Type_U8
from pycspr.types.cl_types.cl_int import CL_Type_U32
from pycspr.types.cl_types.cl_int import CL_Type_U64
from pycspr.types.cl_types.cl_int import CL_Type_U128
from pycspr.types.cl_types.cl_int import CL_Type_U256
from pycspr.types.cl_types.cl_int import CL_Type_U512
from pycspr.types.cl_types.cl_key import CL_Type_Key
from pycspr.types.cl_types.cl_list import CL_Type_List
from pycspr.types.cl_types.cl_map import CL_Type_Map
from pycspr.types.cl_types.cl_public_key import CL_Type_PublicKey
from pycspr.types.cl_types.cl_result import CL_Type_Result
from pycspr.types.cl_types.cl_string import CL_Type_String
from pycspr.types.cl_types.cl_tuple import CL_Type_Tuple1
from pycspr.types.cl_types.cl_tuple import CL_Type_Tuple2
from pycspr.types.cl_types.cl_tuple import CL_Type_Tuple3
from pycspr.types.cl_types.cl_unit import CL_Type_Unit
from pycspr.types.cl_types.cl_uref import CL_Type_URef


@dataclasses.dataclass
class CL_Type_Option(CL_Type):
    """Encapsulates CL type information associated with an optional value.

    """
    # Inner type within CSPR type system.
    inner_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.OPTION

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key and self.inner_type == other.inner_type

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value]) + self.inner_type.as_bytes()

    def as_json(self) -> str:
        return {
            "Option": self.inner_type.as_json()
        }

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Type_Option":
        inner_type_key = CL_TypeKey(int(as_bytes[1]))
        inner_type_cls = _TYPEKEY_TO_TYPE[inner_type_key]
        inner_type = inner_type_cls.from_bytes(as_bytes[1:])

        return CL_Type_Option(inner_type)


# Map of type key to type.
_TYPEKEY_TO_TYPE = {    
    CL_TypeKey.ANY: CL_Type_Any,
    CL_TypeKey.BOOL: CL_Type_Bool,
    CL_TypeKey.BYTE_ARRAY: CL_Type_ByteArray,
    CL_TypeKey.I32: CL_Type_I32,
    CL_TypeKey.I64: CL_Type_I64,
    CL_TypeKey.KEY: CL_Type_Key,
    CL_TypeKey.LIST: CL_Type_List,
    CL_TypeKey.OPTION: CL_Type_Option,
    CL_TypeKey.MAP: CL_Type_Map,
    CL_TypeKey.PUBLIC_KEY: CL_Type_PublicKey,
    CL_TypeKey.RESULT: CL_Type_Result,    
    CL_TypeKey.STRING: CL_Type_String,
    CL_TypeKey.TUPLE_1: CL_Type_Tuple1,
    CL_TypeKey.TUPLE_2: CL_Type_Tuple2,
    CL_TypeKey.TUPLE_3: CL_Type_Tuple3,
    CL_TypeKey.U8: CL_Type_U8,
    CL_TypeKey.U32: CL_Type_U32,
    CL_TypeKey.U64: CL_Type_U64,
    CL_TypeKey.U128: CL_Type_U128,
    CL_TypeKey.U256: CL_Type_U256,
    CL_TypeKey.U512: CL_Type_U512,
    CL_TypeKey.UNIT: CL_Type_Unit,
    CL_TypeKey.UREF: CL_Type_URef
}
