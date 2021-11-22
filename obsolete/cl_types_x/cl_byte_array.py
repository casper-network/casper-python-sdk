import dataclasses
from pycspr.types.cl_types.base import CL_Type
from pycspr.types.cl_types.base import CL_TypeKey


@dataclasses.dataclass
class CL_Type_ByteArray(CL_Type):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Size of associated byte array value.
    size: int

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.BYTE_ARRAY

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key and self.size == other.size

