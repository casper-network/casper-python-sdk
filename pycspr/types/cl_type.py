import dataclasses

from pycspr.types.cl_enums import CLTypeKey


@dataclasses.dataclass
class CLType():
    """Base class encapsulating CL type information associated with a value.

    """
    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and self.type_key == other.type_key


@dataclasses.dataclass
class CLType_Any(CLType):
    """Encapsulates CL type information associated with any value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.ANY


@dataclasses.dataclass
class CLType_Boolean(CLType):
    """Encapsulates CL type information associated with a Boolean value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.BOOL


@dataclasses.dataclass
class CLType_ByteArray(CLType):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Size of associated byte array value.
    size: int

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.BYTE_ARRAY

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and self.size == other.size


@dataclasses.dataclass
class CLType_I32(CLType):
    """Encapsulates CL type information associated with a I32 value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.I32


@dataclasses.dataclass
class CLType_I64(CLType):
    """Encapsulates CL type information associated with a I64 value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.I64


@dataclasses.dataclass
class CLType_Key(CLType):
    """Encapsulates CL type information associated with a key value.

    """
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

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and self.inner_type == other.inner_type


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

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.key_type == other.key_type and \
               self.value_type == other.value_type


@dataclasses.dataclass
class CLType_Option(CLType):
    """Encapsulates CL type information associated with an optional value.

    """
    # Inner type within CSPR type system.
    inner_type: CLType

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.OPTION

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and self.inner_type == other.inner_type


@dataclasses.dataclass
class CLType_PublicKey(CLType):
    """Encapsulates CL type information associated with a PublicKey value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.PUBLIC_KEY


@dataclasses.dataclass
class CLType_Result(CLType):
    """Encapsulates CL type information associated with a result value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.RESULT


@dataclasses.dataclass
class CLType_String(CLType):
    """Encapsulates CL type information associated with a string value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.STRING


@dataclasses.dataclass
class CLType_Tuple1(CLType):
    """Encapsulates CL type information associated with a 1-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CLType

    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.TUPLE_1

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and self.t0_type == other.t0_type


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

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.t0_type == other.t0_type and \
               self.t1_type == other.t1_type
            


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

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.t0_type == other.t0_type and \
               self.t1_type == other.t1_type and \
               self.t2_type == other.t2_type


@dataclasses.dataclass
class CLType_U8(CLType):
    """Encapsulates CL type information associated with a U8 value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.U8


@dataclasses.dataclass
class CLType_U32(CLType):
    """Encapsulates CL type information associated with a U32 value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.U32


@dataclasses.dataclass
class CLType_U64(CLType):
    """Encapsulates CL type information associated with a U64 value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.U64


@dataclasses.dataclass
class CLType_U128(CLType):
    """Encapsulates CL type information associated with a U128 value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.U128


@dataclasses.dataclass
class CLType_U256(CLType):
    """Encapsulates CL type information associated with a U256 value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.U256


@dataclasses.dataclass
class CLType_U512(CLType):
    """Encapsulates CL type information associated with a U512 value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.U512


@dataclasses.dataclass
class CLType_Unit(CLType):
    """Encapsulates CL type information associated with a unit value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.UNIT


@dataclasses.dataclass
class CLType_URef(CLType):
    """Encapsulates CL type information associated with a uref value.

    """
    # CSPR type key.
    type_key: CLTypeKey = CLTypeKey.UREF
