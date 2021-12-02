import dataclasses
import enum
import typing

from pycspr import crypto
from pycspr.types.cl_types import CL_Type
from pycspr.types.keys import PublicKey


@dataclasses.dataclass
class CL_Value():
    """Represents a CL type value.

    """
    pass


@dataclasses.dataclass
class CL_Any(CL_Value):
    """Represents a CL type value: any = arbitrary data.

    """
    # Associated value.
    value: object

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CL_Bool(CL_Value):
    """Represents a CL type value: boolean.

    """
    # Associated value.
    value: bool

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CL_ByteArray(CL_Value):
    """Represents a CL type value: byte array.

    """
    # Associated value.
    value: bytes

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __len__(self) -> int:
        return len(self.value)


@dataclasses.dataclass
class CL_Int(CL_Value):
    """Represents a CL type value: integer.

    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CL_I32(CL_Int):
    """Represents a CL type value: I32.

    """
    pass


@dataclasses.dataclass
class CL_I64(CL_Int):
    """Represents a CL type value: I64.

    """
    pass


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

    def __eq__(self, other) -> bool:
        return self.identifier == other.identifier and self.key_type == other.key_type

    def to_string(self) -> str:
        if self.key_type == CL_KeyType.ACCOUNT:
            prefix = "account-hash"
        elif self.key_type == CL_KeyType.HASH:
            prefix = "hash"
        elif self.key_type == CL_KeyType.UREF:
            prefix = "uref"
        return f"{prefix}-{self.identifier.hex()}"

    @staticmethod
    def from_string(value: str) -> "CL_Key":
        """Factory method: parses input string & returns type instance. 
        """
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


@dataclasses.dataclass
class CL_List(CL_Value):
    """Represents a CL type value: array of items of identical type.

    """
    # Set of associated items.
    vector: typing.List[CL_Value]

    # Item type identifier.
    item_type: CL_Type

    def __eq__(self, other) -> bool:
        return self.vector == other.vector and self.item_type == other.item_type


@dataclasses.dataclass
class CL_Map(CL_Value):
    """Represents a CL type value: key-value hash map.

    """
    pass


@dataclasses.dataclass
class CL_Option(CL_Value):
    """Represents a CL type value: optional value.

    """
    # Associated value.
    value: typing.Union[None, CL_Value]

    # Associated optional type.
    option_type: CL_Type

    def __eq__(self, other) -> bool:
        return self.value == other.value and self.option_type == other.option_type


@dataclasses.dataclass
class CL_PublicKey(PublicKey, CL_Value):
    """Represents a CL type value: account holder's public key.

    """
    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pbk == other.pbk

    @staticmethod
    def from_account_key(account_key: bytes) -> "CL_PublicKey":
        return CL_PublicKey(crypto.KeyAlgorithm(account_key[0]), account_key[1:])

    @staticmethod
    def from_key(as_key: PublicKey) -> "CL_PublicKey":
        return CL_PublicKey(as_key.algo, as_key.pbk)

    @staticmethod
    def from_string(as_string: str) -> "CL_PublicKey":
        return CL_PublicKey(
            crypto.KeyAlgorithm(bytes.fromhex(as_string)[0]),
            bytes.fromhex(as_string)[1:]
        )


@dataclasses.dataclass
class CL_Result(CL_Value):
    """Represents a CL type value: function invocation result.

    """
    # Associated value.
    value: object

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CL_String(CL_Value):
    """Represents a CL type value: string.

    """
    # Associated value.
    value: str

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CL_Tuple1(CL_Value):
    """Represents a CL type value: a 1-ary tuple.

    """
    # 1st value within 1-ary tuple value.
    v0: CL_Value

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0


@dataclasses.dataclass
class CL_Tuple2(CL_Value):
    """Represents a CL type value: a 2-ary tuple.

    """
    # 1st value within 2-ary tuple value.
    v0: CL_Value

    # 2nd value within 2-ary tuple value.
    v1: CL_Value

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0 and self.v1 == other.v1


@dataclasses.dataclass
class CL_Tuple3(CL_Value):
    """Represents a CL type value: a 3-ary tuple.

    """
    # 1st value within 3-ary tuple value.
    v0: CL_Value

    # 2nd value within 3-ary tuple value.
    v1: CL_Value

    # 3rd value within 3-ary tuple value.
    v2: CL_Value

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0 and self.v1 == other.v1 and self.v2 == other.v2


@dataclasses.dataclass
class CL_U8(CL_Int):
    """Represents a CL type value: U8.

    """
    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 8) - 1


@dataclasses.dataclass
class CL_U32(CL_Int):
    """Represents a CL type value: U32.

    """
    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 32) - 1


@dataclasses.dataclass
class CL_U64(CL_Int):
    """Represents a CL type value: U64.

    """
    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 64) - 1


@dataclasses.dataclass
class CL_U128(CL_Int):
    """Represents a CL type value: U128.

    """
    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 128) - 1


@dataclasses.dataclass
class CL_U256(CL_Int):
    """Represents a CL type value: U256.

    """
    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 256) - 1


@dataclasses.dataclass
class CL_U512(CL_Int):
    """Represents a CL type value: U512.

    """
    @staticmethod
    def is_in_range(value: int) -> bool:
        return value >= 0 and value <= (2 ** 512) - 1


@dataclasses.dataclass
class CL_Unit(CL_Value):
    """Represents a CL type value: unit, i.e. a null value.

    """
    def __eq__(self, other) -> bool:
        return True


class CL_URefAccessRights(enum.Enum):
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
    """Represents a CL type value: unforgeable reference.

    """
    # Access rights granted by issuer.
    access_rights: CL_URefAccessRights

    # Uref on-chain identifier.
    address: bytes

    def __eq__(self, other) -> bool:
        return self.access_rights == other.access_rights and \
               self.address == other.address

    def to_string(self):
        return f"uref-{self.address.hex()}-{self.access_rights.value:03}"

    @staticmethod
    def from_string(as_string: str) -> "CL_URef":
        _, address, access_rights = as_string.split("-")
        return CL_URef(
            CL_URefAccessRights(int(access_rights)),
            bytes.fromhex(address)
            )