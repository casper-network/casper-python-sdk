import dataclasses
import enum

from pycspr.types.cl_types import CL_Type_URef
from pycspr.types.cl_values.base import CL_Value
from pycspr.types.cl_values.cl_byte_array import CL_ByteArray


class CL_AccessRights(enum.Enum):
    """Enumeration over set of CL item access rights.

    """
    NONE = 0
    READ = 1
    WRITE = 2
    ADD = 4
    READ_WRITE = 3
    READ_ADD = 5
    ADD_WRITE = 6
    READ_ADD_WRITE = 7


@dataclasses.dataclass
class CL_URef(CL_Value):
    # Access rights granted by issuer.
    access_rights: CL_AccessRights

    # Uref on-chain identifier.
    address: bytes

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.access_rights == other.access_rights and \
               self.address == other.address

    def as_bytes(self) -> bytes:
        as_bytes = self.address + bytes([self.access_rights.value])

        return CL_ByteArray(as_bytes).as_bytes()

    def as_cl_type(self) -> CL_Type_URef:
        return CL_Type_URef()

    def as_parsed(self) -> str:
        return f"uref-{self.address.hex()}-{self.access_rights.value:03}"

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_URef":
        return CL_URef(
            CL_AccessRights(as_bytes[-1]),
            as_bytes[:-1]
        )
    
    @staticmethod
    def from_string(as_string: str) -> "CL_URef":
        _, address, access_rights = as_string.split("-")
        return CL_URef(
            CL_AccessRights(int(access_rights)),
            bytes.fromhex(address)
            )
    
    #endregion
