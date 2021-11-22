import dataclasses

from pycspr.types.cl_byte_array import CL_ByteArray
from pycspr.types.cl_int import CL_U32
from pycspr.types.cl_type import CL_Type_String
from pycspr.types.cl_value import CL_Value


@dataclasses.dataclass
class CL_String(CL_Value):
    """Represents a CL type value: string.
    
    """
    # Associated value.
    value: str

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def as_bytes(self) -> bytes:
        encoded: bytes = (self.value or "").encode("utf-8")
        encoded: bytes = CL_ByteArray(encoded).to_bytes()
        size: bytes = CL_U32(len(encoded)).to_bytes()

        return size + encoded

    def as_cl_type(self) -> CL_Type_String:
        return CL_Type_String()

    def as_parsed(self) -> str:
        return self.value

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_String":
        return CL_String(as_bytes[4:].decode("utf-8"))

    #endregion
