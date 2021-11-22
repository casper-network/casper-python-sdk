import dataclasses

from pycspr.types.cl.cl_type import CL_TypeKey
from pycspr.types.cl.cl_value import CL_Value
from pycspr.utils.constants import is_within_range
from pycspr.utils.conversion import int_to_le_bytes_trimmed
from pycspr.utils.conversion import le_bytes_to_int


BYTE_LENGTH = 16


@dataclasses.dataclass
class CL_U128(CL_Value):
    # Associated value.
    value: int

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_U128":
        if as_bytes[0] <= BYTE_LENGTH:
            return CL_U128(le_bytes_to_int(as_bytes[1:], False))
        else:
            raise ValueError("Cannot decode U128 as bytes are too large")

    @staticmethod
    def from_json(as_json: str) -> "CL_U128":
        return CL_U128(int(as_json))


    def to_bytes(self) -> bytes:
        for type_key in (
            CL_TypeKey.U8,
            CL_TypeKey.U32,
            CL_TypeKey.U64,
            CL_TypeKey.U128
        ):
            if is_within_range(type_key, self.value):
                break
        else:
            raise ValueError("Invalid U128: max size exceeded")

        as_bytes = int_to_le_bytes_trimmed(self.value, BYTE_LENGTH, False)

        return bytes([len(as_bytes)]) + as_bytes


    def to_json(self) -> str:
        return str(self.value)
