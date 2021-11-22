import dataclasses
import enum

from pycspr.types.cl_value import CL_Value
from pycspr.types.cl_type import CL_Type_Key
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
    """Represents a CL type value: state storage key.
    
    """
    # 32 byte key identifier.
    identifier: bytes

    # Key type identifier.
    key_type: CL_KeyType

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.identifier == other.identifier and self.key_type == other.key_type

    def as_bytes(self) -> bytes:
        return bytes([self.key_type.value]) + self.identifier

    def as_cl_type(self) -> CL_Type_Key:
        return CL_Type_Key()

    def as_parsed(self) -> str:
        if self.key_type == CL_KeyType.ACCOUNT:
            prefix = "account-hash"
        elif self.key_type == CL_KeyType.HASH:
            prefix = "hash"
        elif self.key_type == CL_KeyType.UREF:
            prefix = "uref"
        else:
            raise ValueError(f"Invalid state key: {self}")
        
        return f"{prefix}-{self.identifier.hex()}"

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Key":
        return CL_Key(as_bytes[1:], CL_KeyType(as_bytes[0]))

    @staticmethod
    def from_string(value: str) -> "CL_Key":
        identifier = bytes.fromhex(value.split("-")[-1])
        if value.startswith("account-hash-"):
            key_type = CL_KeyType.ACCOUNT
        elif value.startswith("hash-"):
            key_type = CL_KeyType.HASH
        elif value.startswith("uref-"):
            key_type = CL_KeyType.UREF
        else:
            raise ValueError(f"Invalid CL key: {value}")

        return CL_Key(identifier, key_type)

    #endregion
    