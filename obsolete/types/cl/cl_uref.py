import dataclasses
import enum

from pycspr.types.cl.cl_value import CL_Value
from pycspr.types.cl.cl_byte_array import CL_ByteArray


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

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.access_rights == other.access_rights and \
               self.address == other.address


    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_URef":
        return CL_URef(
            CL_AccessRights(as_bytes[-1]),
            as_bytes[:-1]
        )


    @staticmethod
    def from_json(as_json: str) -> "CL_URef":
        return CL_URef.from_string(as_json)


    @staticmethod
    def from_string(as_string: str) -> "CL_URef":
        _, address, access_rights = as_string.split("-")
        return CL_URef(
            CL_AccessRights(int(access_rights)),
            bytes.fromhex(address)
            )


    def to_bytes(self) -> bytes:
        return CL_ByteArray(
            self.address + bytes([self.access_rights.value])
            ).to_bytes()


    def to_json(self) -> str:
        return self.to_string()


    def to_string(self):
        return f"uref-{self.address.hex()}-{self.access_rights.value:03}"
