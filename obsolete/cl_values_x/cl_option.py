import dataclasses
import typing

from pycspr.types.cl_types import CL_Type
from pycspr.types.cl_types import CL_Type_Option
from pycspr.types.cl_values.base import CL_Value


@dataclasses.dataclass
class CL_Option(CL_Value):
    """Represents a CL type value: optional value.
    
    """
    # Associated value.
    value: typing.Union[None, CL_Value]

    # Associated optional type.
    option_type: CL_Type

    def __eq__(self, other) -> bool:
        return self.value == other.value and self.option_type == other.option_type
