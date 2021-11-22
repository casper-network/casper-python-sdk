import dataclasses
import typing

from pycspr.types.cl.cl_any import CL_Any
from pycspr.types.cl.cl_bool import CL_Bool
from pycspr.types.cl.cl_byte_array import CL_ByteArray
from pycspr.types.cl.cl_i32 import CL_I32
from pycspr.types.cl.cl_i64 import CL_I64
from pycspr.types.cl.cl_key import CL_Key
from pycspr.types.cl.cl_map import CL_Map
from pycspr.types.cl.cl_option import CL_Option
from pycspr.types.cl.cl_public_key import CL_PublicKey
from pycspr.types.cl.cl_result import CL_Result
from pycspr.types.cl.cl_string import CL_String
from pycspr.types.cl.cl_tuple_1 import CL_Tuple1
from pycspr.types.cl.cl_tuple_2 import CL_Tuple2
from pycspr.types.cl.cl_tuple_3 import CL_Tuple3
from pycspr.types.cl.cl_type import CL_Type
from pycspr.types.cl.cl_type import CL_TypeKey
from pycspr.types.cl.cl_u8 import CL_U8
from pycspr.types.cl.cl_u32 import CL_U32
from pycspr.types.cl.cl_u64 import CL_U64
from pycspr.types.cl.cl_u128 import CL_U128
from pycspr.types.cl.cl_u256 import CL_U256
from pycspr.types.cl.cl_u512 import CL_U512
from pycspr.types.cl.cl_unit import CL_Unit
from pycspr.types.cl.cl_uref import CL_URef
from pycspr.types.cl.cl_value import CL_Value
from pycspr.types.cl.cl_vector import CL_Vector


@dataclasses.dataclass
class CL_List(CL_Value):
    # Set of associated items.
    vector: typing.List[object]

    # Item type identifier.
    item_type: CL_Type

    @property
    def item_serialiser(self):
        return _ITEM_SERIALISERS[self.item_type]


    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.vector == other.vector and \
               self.item_type == other.item_type


    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_List":
        raise NotImplementedError()


    @staticmethod
    def from_json(as_json: str) -> "CL_List":        
        raise NotImplementedError()


    def to_bytes(self) -> bytes:
        return self.to_cl_vector().to_bytes()


    def to_cl_vector(self) -> bytes:
        return CL_Vector([self.item_serialiser.to_bytes(i) for i in self.vector]).to_bytes()


    def to_json(self) -> dict:
        return [self.item_serialiser.to_json(i) for i in self.vector]


# Map: CL type key <-> list item serialiser.
_ITEM_SERIALISERS = {
    CL_TypeKey.ANY: CL_Any,
    CL_TypeKey.BOOL: CL_Bool,
    CL_TypeKey.BYTE_ARRAY: CL_ByteArray,
    CL_TypeKey.I32: CL_I32,
    CL_TypeKey.I64: CL_I64,
    CL_TypeKey.KEY: CL_Key,
    CL_TypeKey.MAP: CL_Map,
    CL_TypeKey.LIST: CL_List,
    CL_TypeKey.OPTION: CL_Option,
    CL_TypeKey.PUBLIC_KEY: CL_PublicKey,
    CL_TypeKey.RESULT: CL_Result,
    CL_TypeKey.STRING: CL_String,
    CL_TypeKey.TUPLE_1: CL_Tuple1,
    CL_TypeKey.TUPLE_2: CL_Tuple2,
    CL_TypeKey.TUPLE_3: CL_Tuple3,
    CL_TypeKey.U8: CL_U8,
    CL_TypeKey.U32: CL_U32,
    CL_TypeKey.U64: CL_U64,
    CL_TypeKey.U128: CL_U128,
    CL_TypeKey.U256: CL_U256,
    CL_TypeKey.U512: CL_U512,
    CL_TypeKey.UNIT: CL_Unit,
    CL_TypeKey.UREF: CL_URef,
}
