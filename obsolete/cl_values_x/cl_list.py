import dataclasses
import typing

from pycspr.types.cl_types import CL_Type
from pycspr.types.cl_types import CL_TypeKey
from pycspr.types.cl_types import CL_Type_List
from pycspr.types.cl_values.cl_any import CL_Any
from pycspr.types.cl_values.cl_bool import CL_Bool
from pycspr.types.cl_values.cl_byte_array import CL_ByteArray
from pycspr.types.cl_values.cl_int import CL_I32
from pycspr.types.cl_values.cl_int import CL_I64
from pycspr.types.cl_values.cl_int import CL_U8
from pycspr.types.cl_values.cl_int import CL_U32
from pycspr.types.cl_values.cl_int import CL_U64
from pycspr.types.cl_values.cl_int import CL_U128
from pycspr.types.cl_values.cl_int import CL_U256
from pycspr.types.cl_values.cl_int import CL_U512
from pycspr.types.cl_values.cl_key import CL_Key
from pycspr.types.cl_values.cl_map import CL_Map
from pycspr.types.cl_values.cl_option import CL_Option
from pycspr.types.cl_values.cl_public_key import CL_PublicKey
from pycspr.types.cl_values.cl_result import CL_Result
from pycspr.types.cl_values.cl_string import CL_String
from pycspr.types.cl_values.cl_tuple import CL_Tuple1
from pycspr.types.cl_values.cl_tuple import CL_Tuple2
from pycspr.types.cl_values.cl_tuple import CL_Tuple3
from pycspr.types.cl_values.cl_unit import CL_Unit
from pycspr.types.cl_values.cl_uref import CL_URef
from pycspr.types.cl_values.base import CL_Value
from pycspr.types.other.vector import Vector


@dataclasses.dataclass
class CL_List(CL_Value):
    """Represents a CL type value: array of items of identical type.
    
    """
    # Set of associated items.
    vector: typing.List[CL_Value]

    # Item type identifier.
    item_type: CL_Type


    def __eq__(self, other) -> bool:
        return self.vector == other.vector and self.item_type == other.item_type


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
