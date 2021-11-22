import dataclasses

from pycspr.types.cl_types import CL_Type_Result
from pycspr.types.cl_values.base import CL_Value


@dataclasses.dataclass
class CL_Result(CL_Value):
    """Represents a CL type value: function invocation result.
    
    """
    # Associated value.
    value: object

    def __eq__(self, other) -> bool:
        return self.value == other.value

