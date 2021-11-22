import dataclasses
import enum

from pycspr.types.cl.cl_value import CL_Value
from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import le_bytes_to_int


BYTE_LENGTH = 8


class CL_KeyType(enum.Enum):
    """Enumeration over set of global state key types.

    """
    ACCOUNT = 0
    HASH = 1
    UREF = 2


@dataclasses.dataclass
class CL_Key(CL_Value):
    # 32 byte key identifier.
    identifier: bytes

    # Key type identifier.
    key_type: CL_KeyType


    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.identifier == other.identifier and \
               self.key_type == other.key_type


    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Key":
        return CL_Key(as_bytes[1:], CL_KeyType(as_bytes[0]))


    @staticmethod
    def from_json(as_json: str) -> "CL_Key":
        return CL_Key.from_string(as_json)


    @staticmethod
    def from_string(value: str) -> "CL_Key":
        identifier = bytes.fromhex(value.split("-")[-1])
        if value.startswith("account-hash-"):
            return CL_Key(identifier, CL_KeyType.ACCOUNT)
        elif value.startswith("hash-"):
            return CL_Key(identifier, CL_KeyType.HASH)
        elif value.startswith("uref-"):
            return CL_Key(identifier, CL_KeyType.UREF)
        else:
            raise ValueError(f"Invalid CL key: {value}")


    def to_bytes(self) -> bytes:
        return bytes([self.key_type.value]) + self.identifier


    def to_json(self) -> str:
        return self.to_string()


    def to_string(self) -> str:
        if self.key_type == CL_KeyType.ACCOUNT:
            return f"account-hash-{self.identifier.hex()}"
        elif self.key_type == CL_KeyType.HASH:
            return f"hash-{self.identifier.hex()}"
        elif self.key_type == CL_KeyType.UREF:
            return f"uref-{self.identifier.hex()}"
        else:
            raise ValueError(f"Invalid state key: {self}")
