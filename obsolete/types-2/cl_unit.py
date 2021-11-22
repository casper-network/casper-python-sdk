import dataclasses

from pycspr.types.cl_type import CL_Type_Unit
from pycspr.types.cl_value import CL_Value


@dataclasses.dataclass
class CL_Unit(CL_Value):
    """Represents a CL type value: unit, i.e. a null value.
    
    """
    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return True

    def as_bytes(self) -> bytes:
        return bytes([])

    def as_cl_type(self) -> CL_Type_Unit:
        return CL_Type_Unit()

    def as_parsed(self) -> str:
        return ""

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Unit":
        if len(as_bytes) != 0:
            raise ValueError("Invalid unit bytes")
        return CL_Unit()
    
    #endregion
