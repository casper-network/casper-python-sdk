import dataclasses

from pycspr.types.cl_types.cl_string import CL_Type_String
from pycspr.types.cl_values.cl_byte_array import CL_ByteArray
from pycspr.types.cl_values.cl_int import CL_U32
from pycspr.types.cl_values.base import CL_Value


@dataclasses.dataclass
class CL_String(CL_Value):
    """Represents a CL type value: string.
    
    """
    # Associated value.
    value: str

    def __eq__(self, other) -> bool:
        return self.value == other.value
