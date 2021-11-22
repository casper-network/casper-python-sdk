import dataclasses
from pycspr.types.cl_types.base import CL_Type
from pycspr.types.cl_types.base import CL_TypeKey



@dataclasses.dataclass
class CL_Type_Map(CL_Type):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Type info of map's key.
    key_type: CL_Type

    # Type info of map's value.
    value_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.MAP

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.key_type == other.key_type and \
               self.value_type == other.value_type
