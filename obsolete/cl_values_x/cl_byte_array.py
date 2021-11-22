import dataclasses

from pycspr.types.cl_types import CL_Type_ByteArray
from pycspr.types.cl_values.base import CL_Value


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

    #endregion
