import dataclasses

from pycspr.types.cl_type import CL_Type_ByteArray
from pycspr.types.cl_value import CL_Value


@dataclasses.dataclass
class CL_ByteArray(CL_Value):
    """Represents a CL type value: byte array.
    
    """
    # Associated value.
    value: bytes

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        return self.value

    def as_cl_type(self) -> CL_Type_ByteArray:
        return CL_Type_ByteArray(len(self.value))

    def as_parsed(self) -> str:
        return self.value.hex()

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_ByteArray":
        return CL_ByteArray(as_bytes)

    #endregion
