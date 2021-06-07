import dataclasses
import enum



class CLType(enum.Enum):
    """Enumeration over set of CL types.
    
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


# Set of types considered to be simple.
CL_TYPES_SIMPLE = {
    CLType.BOOL,
    CLType.I32,
    CLType.I64,
    CLType.KEY,
    CLType.PUBLIC_KEY,
    CLType.STRING,
    CLType.U8,
    CLType.U32,
    CLType.U64,
    CLType.U128,
    CLType.U256,
    CLType.U512,
    CLType.UNIT,
    CLType.UREF,
}
            
                
@dataclasses.dataclass
class CLTypeInfo():
    """Encapsulates CL type information associated with a value.
    
    """
    # Associated type within CSPR type system.
    typeof: CLType

    @property
    def type_tag(self) -> int:
        """Returns a tag used when encoding/decoding."""
        return self.typeof.value


@dataclasses.dataclass
class CLTypeInfoForByteArray(CLTypeInfo):
    """Encapsulates CL type information associated with a byte array value.
    
    """
    # Size of associated byte array value.
    size: int


@dataclasses.dataclass
class CLTypeInfoForList(CLTypeInfo):
    """Encapsulates CL type information associated with a list value.
    
    """
    # Inner type within CSPR type system.
    inner_type_info: CLTypeInfo


@dataclasses.dataclass
class CLTypeInfoForMap(CLTypeInfo):
    """Encapsulates CL type information associated with a byte array value.
    
    """
    # Type info of map's key.
    key_type_info: CLType

    # Type info of map's value.
    value_type_info: CLTypeInfo


@dataclasses.dataclass
class CLTypeInfoForOption(CLTypeInfo):
    """Encapsulates CL type information associated with an optional value.
    
    """
    # Inner type within CSPR type system.
    inner_type_info: CLTypeInfo


@dataclasses.dataclass
class CLTypeInfoForSimple(CLTypeInfo):
    """Encapsulates CL type information associated with a simple value.
    
    """
    pass


@dataclasses.dataclass
class CLTypeInfoForTuple1(CLTypeInfo):
    """Encapsulates CL type information associated with a 1-ary tuple value value.
    
    """
    # Type of first value within 1-ary tuple value.
    t0_type_info: CLTypeInfo


@dataclasses.dataclass
class CLTypeInfoForTuple2(CLTypeInfo):
    """Encapsulates CL type information associated with a 2-ary tuple value value.
    
    """
    # Type of first value within 1-ary tuple value.
    t0_type_info: CLTypeInfo

    # Type of first value within 2-ary tuple value.
    t1_type_info: CLTypeInfo


@dataclasses.dataclass
class CLTypeInfoForTuple3(CLTypeInfo):
    """Encapsulates CL type information associated with a 3-ary tuple value value.
    
    """
    # Type of first value within 1-ary tuple value.
    t0_type_info: CLTypeInfo

    # Type of first value within 2-ary tuple value.
    t1_type_info: CLTypeInfo

    # Type of first value within 3-ary tuple value.
    t2_type_info: CLTypeInfo


@dataclasses.dataclass
class CLValue():
    """A CL value mapped from python type system.
    
    """
    # Byte array representation of underlying data.
    bytes: bytes

    # Parsed pythonic representation of underlying data (for human convenience only).
    parsed: object

    # Type information used by a deserializer.
    type_info: CLTypeInfo
