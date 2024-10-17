import dataclasses
import enum
import typing

from pycspr.type_defs.cl_types import CLT_Type
from pycspr.type_defs.crypto import KeyAlgorithm, PublicKey


@dataclasses.dataclass
class CLV_Value():
    """Represents a CL type value.

    """
    pass


@dataclasses.dataclass
class CLV_Any(CLV_Value):
    """Represents a CL type value: any = arbitrary data.

    """
    # Associated value.
    value: object

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CLV_Bool(CLV_Value):
    """Represents a CL type value: boolean.

    """
    # Associated value.
    value: bool

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CLV_ByteArray(CLV_Value):
    """Represents a CL type value: byte array.

    """
    # Associated value.
    value: bytes

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __len__(self) -> int:
        return len(self.value)


@dataclasses.dataclass
class CLV_Int(CLV_Value):
    """Represents a CL type value: integer.

    """
    # Associated value.
    value: int

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CLV_I32(CLV_Int):
    """Represents a CL type value: I32.

    """
    pass


@dataclasses.dataclass
class CLV_I64(CLV_Int):
    """Represents a CL type value: I64.

    """
    pass


class CLV_KeyType(enum.Enum):
    """Enumeration over set of global state key types.

    """
    ACCOUNT = 0
    HASH = 1
    UREF = 2


@dataclasses.dataclass
class CLV_Key(CLV_Value):
    """Represents a CL type value: state storage key.

    """
    # 32 byte key identifier.
    identifier: bytes

    # Key type identifier.
    key_type: CLV_KeyType

    def __eq__(self, other) -> bool:
        return self.identifier == other.identifier and self.key_type == other.key_type

    @staticmethod
    def from_str(value: str) -> "CLV_Key":
        identifier: bytes = bytes.fromhex(value.split("-")[-1])
        if value.startswith("account-hash-"):
            key_type: CLV_KeyType = CLV_KeyType.ACCOUNT
        elif value.startswith("hash-"):
            key_type: CLV_KeyType = CLV_KeyType.HASH
        elif value.startswith("uref-"):
            key_type: CLV_KeyType = CLV_KeyType.UREF
        else:
            raise ValueError(f"Invalid CL key: {value}")

        return CLV_Key(identifier, key_type)


@dataclasses.dataclass
class CLV_List(CLV_Value):
    """Represents a CL type value: array of items of identical type.

    """
    # Set of associated items.
    vector: typing.List[CLV_Value]

    def __eq__(self, other) -> bool:
        return self.vector == other.vector


@dataclasses.dataclass
class CLV_Map(CLV_Value):
    """Represents a CL type value: key-value hash map.

    """
    # A map of data represented as a vector of 2 member tuples.
    value: typing.List[typing.Tuple[CLV_Value, CLV_Value]]


@dataclasses.dataclass
class CLV_Option(CLV_Value):
    """Represents a CL type value: optional value.

    """
    # Associated value.
    value: typing.Union[None, CLV_Value]

    # Associated optional type.
    option_type: CLT_Type

    def __eq__(self, other) -> bool:
        return self.value == other.value and self.option_type == other.option_type


@dataclasses.dataclass
class CLV_PublicKey(CLV_Value):
    """Represents a CL type value: account holder's public key.

    """
    # Algorithm used to generate ECC key pair.
    algo: KeyAlgorithm

    # Public key as raw bytes.
    pbk: bytes

    @property
    def account_hash(self) -> bytes:
        """Returns on-chain account hash."""
        from pycspr.crypto import get_account_hash

        return get_account_hash(self.account_key)

    @property
    def account_key(self) -> bytes:
        """Returns on-chain account key."""
        from pycspr.crypto import get_account_key

        return get_account_key(self.algo, self.pbk)

    @staticmethod
    def from_public_key(key: PublicKey):
        return CLV_PublicKey(key.algo, key.pbk)

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pbk == other.pbk


@dataclasses.dataclass
class CLV_Result(CLV_Value):
    """Represents a CL type value: function invocation result.

    """
    # Associated value.
    value: object

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CLV_String(CLV_Value):
    """Represents a CL type value: string.

    """
    # Associated value.
    value: str

    def __eq__(self, other) -> bool:
        return self.value == other.value


@dataclasses.dataclass
class CLV_Tuple1(CLV_Value):
    """Represents a CL type value: a 1-ary tuple.

    """
    # 1st value within 1-ary tuple value.
    v0: CLV_Value

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0


@dataclasses.dataclass
class CLV_Tuple2(CLV_Value):
    """Represents a CL type value: a 2-ary tuple.

    """
    # 1st value within 2-ary tuple value.
    v0: CLV_Value

    # 2nd value within 2-ary tuple value.
    v1: CLV_Value

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0 and self.v1 == other.v1


@dataclasses.dataclass
class CLV_Tuple3(CLV_Value):
    """Represents a CL type value: a 3-ary tuple.

    """
    # 1st value within 3-ary tuple value.
    v0: CLV_Value

    # 2nd value within 3-ary tuple value.
    v1: CLV_Value

    # 3rd value within 3-ary tuple value.
    v2: CLV_Value

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0 and self.v1 == other.v1 and self.v2 == other.v2


@dataclasses.dataclass
class CLV_U8(CLV_Int):
    """Represents a CL type value: U8.

    """
    pass


@dataclasses.dataclass
class CLV_U32(CLV_Int):
    """Represents a CL type value: U32.

    """
    pass


@dataclasses.dataclass
class CLV_U64(CLV_Int):
    """Represents a CL type value: U64.

    """
    pass


@dataclasses.dataclass
class CLV_U128(CLV_Int):
    """Represents a CL type value: U128.

    """
    pass


@dataclasses.dataclass
class CLV_U256(CLV_Int):
    """Represents a CL type value: U256.

    """
    pass


@dataclasses.dataclass
class CLV_U512(CLV_Int):
    """Represents a CL type value: U512.

    """
    pass


@dataclasses.dataclass
class CLV_Unit(CLV_Value):
    """Represents a CL type value: unit, i.e. a null value.

    """
    def __eq__(self, other) -> bool:
        return True


class CLV_URefAccessRights(enum.Enum):
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
class CLV_URef(CLV_Value):
    """Represents a CL type value: unforgeable reference.

    """
    # Access rights granted by issuer.
    access_rights: CLV_URefAccessRights

    # Uref on-chain identifier.
    address: bytes

    def __eq__(self, other) -> bool:
        return self.access_rights == other.access_rights and \
               self.address == other.address

    @staticmethod
    def from_str(value: str) -> "CLV_URef":
        _, address, access_rights = value.split("-")

        return CLV_URef(
            CLV_URefAccessRights(int(access_rights)),
            bytes.fromhex(address)
            )
