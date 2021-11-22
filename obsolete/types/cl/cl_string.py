import dataclasses

from pycspr.types.cl.cl_value import CL_ByteArray
from pycspr.types.cl.cl_value import CL_U32
from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class CL_String(CL_Value):
    # Associated value.
    value: str

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_String":
        return CL_String(as_bytes[CL_U32.BYTE_LENGTH:].decode("utf-8"))


    @staticmethod
    def from_json(as_json: str) -> "CL_String":
        return CL_String(as_json)


    def to_bytes(self) -> bytes:
        as_bytes = (self.value or "").encode("utf-8")
        as_bytes = CL_ByteArray(as_bytes).to_bytes()

        return CL_U32(len(as_bytes)).to_bytes() + as_bytes


    def to_json(self) -> str:
        return self.value
