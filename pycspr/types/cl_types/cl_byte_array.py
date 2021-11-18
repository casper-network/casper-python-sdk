import dataclasses
from pycspr.types.cl_types.base import CL_Type
from pycspr.types.cl_types.base import CL_TypeKey


@dataclasses.dataclass
class CL_Type_ByteArray(CL_Type):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Size of associated byte array value.
    size: int

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.BYTE_ARRAY

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key and self.size == other.size

    def as_bytes(self) -> bytes:
        from pycspr.types.cl_values.cl_int import CL_U32

        return bytes([self.type_key.value]) + CL_U32(self.size).as_bytes()

    def as_json(self) -> str:
        return {
            "ByteArray": self.size
        }

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Type_ByteArray":
        from pycspr.types.cl_values.cl_int import CL_U32
        size = CL_U32.from_bytes(as_bytes[1:]).value

        return CL_Type_ByteArray(size)

    @staticmethod
    def from_json(obj: dict) -> "CL_Type_ByteArray":
        return CL_Type_ByteArray(obj["ByteArray"])
