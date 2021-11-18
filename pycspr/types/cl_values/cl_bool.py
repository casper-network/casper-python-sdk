import dataclasses

from pycspr.types.cl_types import CL_Type_Bool
from pycspr.types.cl_values.base import CL_Value


@dataclasses.dataclass
class CL_Bool(CL_Value):
    """Represents a CL type value: boolean.
    
    """
    # Associated value.
    value: bool

    def __eq__(self, other) -> bool:
        return self.value == other.value
