import dataclasses
from pycspr.types.enums import CLTypeKey



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
    typeof: CLTypeKey = CLTypeKey.BYTE_ARRAY


@dataclasses.dataclass
class CLType_List(CLType):
    """Encapsulates CL type information associated with a list value.
    
    """
    # Inner type within CSPR type system.
    inner_type: CLType

    # CSPR type key.
    typeof: CLTypeKey = CLTypeKey.LIST


@dataclasses.dataclass
class CLType_Map(CLType):
    """Encapsulates CL type information associated with a byte array value.
    
    """
    # Type info of map's key.
    key_type: CLType

    # Type info of map's value.
    value_type: CLType

    # CSPR type key.
    typeof: CLTypeKey = CLTypeKey.MAP


@dataclasses.dataclass
class CLType_Option(CLType):
    """Encapsulates CL type information associated with an optional value.
    
    """
    # Inner type within CSPR type system.
    inner_type: CLType

    # CSPR type key.
    typeof: CLTypeKey = CLTypeKey.OPTION


@dataclasses.dataclass
class CLType_Simple(CLType):
    """Encapsulates CL type information associated with a simple value.
    
    """
    # CSPR type key.
    typeof: CLTypeKey


@dataclasses.dataclass
class CLType_Tuple1(CLType):
    """Encapsulates CL type information associated with a 1-ary tuple value value.
    
    """
    # Type of first value within 1-ary tuple value.
    t0_type: CLType

    # CSPR type key.
    typeof: CLTypeKey = CLTypeKey.TUPLE_1


@dataclasses.dataclass
class CLType_Tuple2(CLType):
    """Encapsulates CL type information associated with a 2-ary tuple value value.
    
    """
    # Type of first value within 1-ary tuple value.
    t0_type: CLType

    # Type of first value within 2-ary tuple value.
    t1_type: CLType

    # CSPR type key.
    typeof: CLTypeKey = CLTypeKey.TUPLE_2


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
    typeof: CLTypeKey = CLTypeKey.TUPLE_3


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
