import dataclasses

from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class CL_ByteArray(CL_Value):
    # Associated value.
    value: bytes

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_ByteArray":
        return as_bytes


    @staticmethod
    def from_json(as_json: str) -> "CL_ByteArray":
        return CL_ByteArray(bytes.fromhex(as_json))


    def to_bytes(self) -> bytes:
        return bytes([]) if isinstance(self.value, type(None)) else self.value


    def to_json(self) -> str:
        return self.value.hex()
