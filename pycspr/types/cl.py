import dataclasses
import enum


class CLTypeKey(enum.Enum):
    """Enumeration over set of CL type keys.

    """
    BOOL = 0
    I32 = 1
    I64 = 2
    U8 = 3
    U32 = 4
    U64 = 5
    U128 = 6
    U256 = 7
    U512 = 8
    UNIT = 9
    STRING = 10
    KEY = 11
    UREF = 12
    OPTION = 13
    LIST = 14
    BYTE_ARRAY = 15
    RESULT = 16
    MAP = 17
    TUPLE_1 = 18
    TUPLE_2 = 19
    TUPLE_3 = 20
    ANY = 21
    PUBLIC_KEY = 22


class CLAccessRights(enum.Enum):
    """Enumeration over set of CL storage item access rights.

    """
    NONE = 0
    READ = 1
    WRITE = 2
    ADD = 4
    READ_WRITE = 3
    READ_ADD = 5
    ADD_WRITE = 6
    READ_ADD_WRITE = 7


class CLStorageKeyType(enum.Enum):
    """Enumeration over set of CL storage key.

    """
    ACCOUNT = 0
    HASH = 1
    UREF = 2


# Set of CL types considered to be numeric.
TYPES_NUMERIC = {
    CLTypeKey.I32,
    CLTypeKey.I64,
    CLTypeKey.U8,
    CLTypeKey.U32,
    CLTypeKey.U64,
    CLTypeKey.U128,
    CLTypeKey.U256,
    CLTypeKey.U512,
}


# Set of CL types considered to be simple.
TYPES_SIMPLE = TYPES_NUMERIC.union({
    CLTypeKey.BOOL,
    CLTypeKey.PUBLIC_KEY,
    CLTypeKey.STRING,
    CLTypeKey.UNIT,
})


@dataclasses.dataclass
class CLType():
    """Base class encapsulating CL type information associated with a value.

    """
    pass


@dataclasses.dataclass
class CLType_ByteArray(CLType):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Size of associated byte array value.
    size: int

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.BYTE_ARRAY


@dataclasses.dataclass
class CLType_StorageKey(CLType):
    """Encapsulates CL type information associated with a storage key value.

    """
    # Key type within CSPR type system.
    key_type: CLStorageKeyType

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.KEY


@dataclasses.dataclass
class CLType_List(CLType):
    """Encapsulates CL type information associated with a list value.

    """
    # Inner type within CSPR type system.
    inner_type: CLType

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.LIST


@dataclasses.dataclass
class CLType_Map(CLType):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Type info of map's key.
    key_type: CLType

    # Type info of map's value.
    value_type: CLType

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.MAP


@dataclasses.dataclass
class CLType_Option(CLType):
    """Encapsulates CL type information associated with an optional value.

    """
    # Inner type within CSPR type system.
    inner_type: CLType

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.OPTION


@dataclasses.dataclass
class CLType_Simple(CLType):
    """Encapsulates CL type information associated with a simple value.

    """
    # CSPR type key.
    type_key: CLTypeKey


@dataclasses.dataclass
class CLType_Tuple1(CLType):
    """Encapsulates CL type information associated with a 1-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CLType

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.TUPLE_1


@dataclasses.dataclass
class CLType_Tuple2(CLType):
    """Encapsulates CL type information associated with a 2-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CLType

    # Type of first value within 2-ary tuple value.
    t1_type: CLType

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.TUPLE_2


@dataclasses.dataclass
class CLType_Tuple3(CLType):
    """Encapsulates CL type information associated with a 3-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CLType

    # Type of first value within 2-ary tuple value.
    t1_type: CLType

    # Type of first value within 3-ary tuple value.
    t2_type: CLType

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.TUPLE_3


@dataclasses.dataclass
class CLValue():
    """A CL value mapped from python type system.

    """
    # Type information used by a deserializer.
    cl_type: CLType

    # Parsed pythonic representation of underlying data (for human convenience only).
    parsed: object

    # Byte array representation of underlying data.
    bytes: bytes = None
