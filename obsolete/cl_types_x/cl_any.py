import dataclasses
from pycspr.types.cl_types.base import CL_Type
from pycspr.types.cl_types.base import CL_TypeKey



@dataclasses.dataclass
class CL_Type_Any(CL_Type):
    """Encapsulates CL type information associated with any value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.ANY

