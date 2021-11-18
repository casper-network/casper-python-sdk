import dataclasses

from pycspr.types.cl_types import CL_Type_Any
from pycspr.types.cl_values.base import CL_Value


@dataclasses.dataclass
class CL_Any(CL_Value):
    """Represents a CL type value: any = arbitrary data.
    
    """    
    # Associated value.
    value: object

    def __eq__(self, other) -> bool:
        return self.value == other.value
