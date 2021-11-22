import dataclasses

from pycspr.types.cl_values.base import CL_Value


@dataclasses.dataclass
class CL_Map(CL_Value):
    # Associated value.
    value: object


