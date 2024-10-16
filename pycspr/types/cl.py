import dataclasses
import enum
import typing

from pycspr.crypto import get_account_hash
from pycspr.crypto import get_account_key
from pycspr.crypto.types import KeyAlgorithm
from pycspr.crypto.types import PublicKey


class CLT_TypeKey(enum.Enum):
    """Enumeration over set of CL type keys.

    """
    ANY = 21
    BOOL = 0
    BYTE_ARRAY = 15
    I32 = 1
    I64 = 2
    KEY = 11
    LIST = 14
    MAP = 17
    OPTION = 13
    PUBLIC_KEY = 22
    RESULT = 16
    STRING = 10
    TUPLE_1 = 18
    TUPLE_2 = 19
    TUPLE_3 = 20
    U8 = 3
    U32 = 4
    U64 = 5
    U128 = 6
    U256 = 7
    U512 = 8
    UNIT = 9
    UREF = 12


@dataclasses.dataclass
class CLT_Type():
    """Base class encapsulating CL type information associated with a value.

    """
    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key


@dataclasses.dataclass
class CLT_Any(CLT_Type):
    """Encapsulates CL type information associated with any value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.ANY


@dataclasses.dataclass
class CLT_Bool(CLT_Type):
    """Encapsulates CL type information associated with a Boolean value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.BOOL


@dataclasses.dataclass
class CLT_ByteArray(CLT_Type):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Size of associated byte array value.
    size: int

    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.BYTE_ARRAY

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key and self.size == other.size


@dataclasses.dataclass
class CLT_I32(CLT_Type):
    """Encapsulates CL type information associated with a I32 value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.I32


@dataclasses.dataclass
class CLT_I64(CLT_Type):
    """Encapsulates CL type information associated with a I64 value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.I64


@dataclasses.dataclass
class CLT_Key(CLT_Type):
    """Encapsulates CL type information associated with a key value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.KEY


@dataclasses.dataclass
class CLT_List(CLT_Type):
    """Encapsulates CL type information associated with a list value.

    """
    # Inner type within CSPR type system.
    inner_type: CLT_Type

    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.LIST

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.inner_type == other.inner_type


@dataclasses.dataclass
class CLT_Map(CLT_Type):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Type info of map's key.
    key_type: CLT_Type

    # Type info of map's value.
    value_type: CLT_Type

    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.MAP

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.key_type == other.key_type and \
               self.value_type == other.value_type


@dataclasses.dataclass
class CLT_Option(CLT_Type):
    """Encapsulates CL type information associated with an optional value.

    """
    # Inner type within CSPR type system.
    inner_type: CLT_Type

    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.OPTION

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key and self.inner_type == other.inner_type


@dataclasses.dataclass
class CLT_PublicKey(CLT_Type):
    """Encapsulates CL type information associated with a PublicKey value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.PUBLIC_KEY


@dataclasses.dataclass
class CLT_Result(CLT_Type):
    """Encapsulates CL type information associated with a result value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.RESULT


@dataclasses.dataclass
class CLT_String(CLT_Type):
    """Encapsulates CL type information associated with any value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.STRING


@dataclasses.dataclass
class CLT_Tuple1(CLT_Type):
    """Encapsulates CL type information associated with a 1-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CLT_Type

    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.TUPLE_1

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.t0_type == other.t0_type


@dataclasses.dataclass
class CLT_Tuple2(CLT_Type):
    """Encapsulates CL type information associated with a 2-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CLT_Type

    # Type of first value within 2-ary tuple value.
    t1_type: CLT_Type

    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.TUPLE_2

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.t0_type == other.t0_type and \
               self.t1_type == other.t1_type


@dataclasses.dataclass
class CLT_Tuple3(CLT_Type):
    """Encapsulates CL type information associated with a 3-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CLT_Type

    # Type of first value within 2-ary tuple value.
    t1_type: CLT_Type

    # Type of first value within 3-ary tuple value.
    t2_type: CLT_Type

    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.TUPLE_3

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.t0_type == other.t0_type and \
               self.t1_type == other.t1_type and \
               self.t2_type == other.t2_type


@dataclasses.dataclass
class CLT_U8(CLT_Type):
    """Encapsulates CL type information associated with a U8 value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.U8


@dataclasses.dataclass
class CLT_U32(CLT_Type):
    """Encapsulates CL type information associated with a U32 value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.U32


@dataclasses.dataclass
class CLT_U64(CLT_Type):
    """Encapsulates CL type information associated with a U64 value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.U64


@dataclasses.dataclass
class CLT_U128(CLT_Type):
    """Encapsulates CL type information associated with a U128 value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.U128


@dataclasses.dataclass
class CLT_U256(CLT_Type):
    """Encapsulates CL type information associated with a U256 value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.U256


@dataclasses.dataclass
class CLT_U512(CLT_Type):
    """Encapsulates CL type information associated with a U512 value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.U512


@dataclasses.dataclass
class CLT_Unit(CLT_Type):
    """Encapsulates CL type information associated with a result value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.UNIT


@dataclasses.dataclass
class CLT_URef(CLT_Type):
    """Encapsulates CL type information associated with a result value.

    """
    # CSPR type key.
    type_key: CLT_TypeKey = CLT_TypeKey.UREF


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
        return get_account_hash(self.account_key)

    @property
    def account_key(self) -> bytes:
        """Returns on-chain account key."""
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


TYPESET_CLT: set = {
    CLT_Type,
    CLT_TypeKey,
    CLT_Any,
    CLT_Bool,
    CLT_ByteArray,
    CLT_I32,
    CLT_I64,
    CLT_U8,
    CLT_U32,
    CLT_U64,
    CLT_U128,
    CLT_U256,
    CLT_U512,
    CLT_Key,
    CLT_List,
    CLT_Map,
    CLT_Option,
    CLT_PublicKey,
    CLT_Result,
    CLT_String,
    CLT_Tuple1,
    CLT_Tuple2,
    CLT_Tuple3,
    CLT_Unit,
    CLT_URef,
}


TYPESET_CLV: set = {
    CLV_Value,
    CLV_Any,
    CLV_Bool,
    CLV_ByteArray,
    CLV_I32,
    CLV_I64,
    CLV_U8,
    CLV_U32,
    CLV_U64,
    CLV_U128,
    CLV_U256,
    CLV_U512,
    CLV_Key,
    CLV_KeyType,
    CLV_List,
    CLV_Map,
    CLV_Option,
    CLV_PublicKey,
    CLV_Result,
    CLV_String,
    CLV_Tuple1,
    CLV_Tuple2,
    CLV_Tuple3,
    CLV_Unit,
    CLV_URefAccessRights,
    CLV_URef,
}

TYPESET: set = TYPESET_CLT | TYPESET_CLV
