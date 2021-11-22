import dataclasses
import enum


class CL_TypeKey(enum.Enum):
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
class CL_Type():
    """Base class encapsulating CL type information associated with a value.

    """
    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key


@dataclasses.dataclass
class CL_Type_Any(CL_Type):
    """Encapsulates CL type information associated with any value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.ANY


@dataclasses.dataclass
class CL_Type_Bool(CL_Type):
    """Encapsulates CL type information associated with a Boolean value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.BOOL


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


@dataclasses.dataclass
class CL_Type_I32(CL_Type):
    """Encapsulates CL type information associated with a I32 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.I32


@dataclasses.dataclass
class CL_Type_I64(CL_Type):
    """Encapsulates CL type information associated with a I64 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.I64


@dataclasses.dataclass
class CL_Type_Key(CL_Type):
    """Encapsulates CL type information associated with a key value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.KEY


@dataclasses.dataclass
class CL_Type_List(CL_Type):
    """Encapsulates CL type information associated with a list value.

    """
    # Inner type within CSPR type system.
    inner_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.LIST

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.inner_type == other.inner_type


@dataclasses.dataclass
class CL_Type_Map(CL_Type):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Type info of map's key.
    key_type: CL_Type

    # Type info of map's value.
    value_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.MAP

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.key_type == other.key_type and \
               self.value_type == other.value_type


@dataclasses.dataclass
class CL_Type_Option(CL_Type):
    """Encapsulates CL type information associated with an optional value.

    """
    # Inner type within CSPR type system.
    inner_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.OPTION

    def __eq__(self, other) -> bool:
        return self.type_key == other.type_key and self.inner_type == other.inner_type


@dataclasses.dataclass
class CL_Type_PublicKey(CL_Type):
    """Encapsulates CL type information associated with a PublicKey value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.PUBLIC_KEY


@dataclasses.dataclass
class CL_Type_Result(CL_Type):
    """Encapsulates CL type information associated with a result value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.RESULT


@dataclasses.dataclass
class CL_Type_String(CL_Type):
    """Encapsulates CL type information associated with any value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.STRING


@dataclasses.dataclass
class CL_Type_Tuple1(CL_Type):
    """Encapsulates CL type information associated with a 1-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.TUPLE_1

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.t0_type == other.t0_type


@dataclasses.dataclass
class CL_Type_Tuple2(CL_Type):
    """Encapsulates CL type information associated with a 2-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CL_Type

    # Type of first value within 2-ary tuple value.
    t1_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.TUPLE_2

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.t0_type == other.t0_type and \
               self.t1_type == other.t1_type


@dataclasses.dataclass
class CL_Type_Tuple3(CL_Type):
    """Encapsulates CL type information associated with a 3-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CL_Type

    # Type of first value within 2-ary tuple value.
    t1_type: CL_Type

    # Type of first value within 3-ary tuple value.
    t2_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.TUPLE_3

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.t0_type == other.t0_type and \
               self.t1_type == other.t1_type and \
               self.t2_type == other.t2_type


@dataclasses.dataclass
class CL_Type_U8(CL_Type):
    """Encapsulates CL type information associated with a U8 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U8


@dataclasses.dataclass
class CL_Type_U32(CL_Type):
    """Encapsulates CL type information associated with a U32 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U32


@dataclasses.dataclass
class CL_Type_U64(CL_Type):
    """Encapsulates CL type information associated with a U64 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U64


@dataclasses.dataclass
class CL_Type_U128(CL_Type):
    """Encapsulates CL type information associated with a U128 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U128


@dataclasses.dataclass
class CL_Type_U256(CL_Type):
    """Encapsulates CL type information associated with a U256 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U256


@dataclasses.dataclass
class CL_Type_U512(CL_Type):
    """Encapsulates CL type information associated with a U512 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U512


@dataclasses.dataclass
class CL_Type_Unit(CL_Type):
    """Encapsulates CL type information associated with a result value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.UNIT


@dataclasses.dataclass
class CL_Type_URef(CL_Type):
    """Encapsulates CL type information associated with a result value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.UREF
