import dataclasses
import typing

from pycspr.types.cl_type import CL_Type
from pycspr.types.cl_type import CL_Type_Option
from pycspr.types.cl_value import CL_Value


@dataclasses.dataclass
class CL_Option(CL_Value):
    """Represents a CL type value: optional value.
    
    """
    # Associated value.
    value: typing.Union[None, CL_Value]

    # Associated optional type.
    option_type: CL_Type

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value and self.option_type == other.option_type

    def as_bytes(self) -> bytes:
        if self.value:
            return bytes([1]) + self.value.to_bytes()
        else:
            return bytes([0])

    def as_cl_type(self) -> CL_Type_Option:
        return CL_Type_Option(self.option_type)

    def as_parsed(self) -> str:
        return self.value.as_parsed() if self.value else ""

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Option":
        raise NotImplementedError()

    #endregion
