import dataclasses

from pycspr.types.cl.cl_value import CL_Value
from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import le_bytes_to_int


BYTE_LENGTH = 4


@dataclasses.dataclass
class CL_I32(CL_Value):
    # Associated value.
    value: int

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_I32":
        return CL_I32(le_bytes_to_int(as_bytes, True))


    @staticmethod
    def from_json(as_json: str) -> "CL_I32":
        return CL_I32(int(as_json))


    def to_bytes(self) -> bytes:
        return int_to_le_bytes(self.value, BYTE_LENGTH, True)


    def to_json(self) -> str:
        return str(self.value)
