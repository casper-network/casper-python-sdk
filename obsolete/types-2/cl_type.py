import dataclasses
import enum
import typing


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

    @staticmethod
    def from_bytes(value: bytes) -> object:
        from pycspr.types.cl_int import CL_U32

        type_tag = CL_TypeKey(value[0])
        kls = _CL_TYPE_KEY_CLASS[type_tag]
        if type_tag == CL_TypeKey.BYTE_ARRAY:
            return kls(CL_U32.from_bytes(value[1:]).value)
        elif type_tag == CL_TypeKey.LIST:
            return kls(CL_Type.from_bytes(value[1:]))
        elif type_tag == CL_TypeKey.MAP:
            return kls(CL_Type.from_bytes(value[1:]), CL_Type.from_bytes(value[1:]))
        elif type_tag == CL_TypeKey.OPTION:
            return kls(CL_Type.from_bytes(value[1:]))
        elif type_tag == CL_TypeKey.TUPLE_1:
            return kls(CL_Type.from_bytes(value[1:]))
        elif type_tag == CL_TypeKey.TUPLE_2:
            return kls(CL_Type.from_bytes(value[1:]), CL_Type.from_bytes(value[1:]))
        elif type_tag == CL_TypeKey.TUPLE_3:
            return kls(CL_Type.from_bytes(value[1:]), CL_Type.from_bytes(value[1:]), CL_Type.from_bytes(value[1:]))
        else:
            return kls()

    def to_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    @staticmethod
    def from_json(value: typing.Union[dict, str]) -> object:
        if isinstance(value, str):
            return _JSON_TAG_CL_TYPE[value]()
        elif "ByteArray" in value:
            return CL_Type_ByteArray(
                value["ByteArray"]
                )
        elif "List" in value:
            return CL_Type_List(
                CL_Type.from_json(value["List"])
                )
        elif "Map" in value:
            return CL_Type_Map(
                CL_Type.from_json(value["Map"]["key"]),
                CL_Type.from_json(value["Map"]["value"])
                )
        elif "Option" in value:
            return CL_Type_Option(
                CL_Type.from_json(value["Option"])
                )
        elif "Tuple1" in value:
            return CL_Type_Tuple1(
                CL_Type.from_json(value["Tuple1"])
                )
        elif "Tuple2" in value:
            return CL_Type_Tuple2(
                CL_Type.from_json(value["Tuple2"][0]),
                CL_Type.from_json(value["Tuple2"][1])
                )
        elif "Tuple3" in value:
            return CL_Type_Tuple3(
                CL_Type.from_json(value["Tuple3"][0]),
                CL_Type.from_json(value["Tuple3"][1]),
                CL_Type.from_json(value["Tuple3"][2])
                )
        else:
            raise NotImplementedError()


@dataclasses.dataclass
class CL_Type_Any(CL_Type):
    """Encapsulates CL type information associated with any value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.ANY

    def to_json(self) -> str:
        return "Any"


@dataclasses.dataclass
class CL_Type_Boolean(CL_Type):
    """Encapsulates CL type information associated with a Boolean value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.BOOL

    def to_json(self) -> str:
        return "Bool"

    def __eq__(self, other) -> bool:
        return super().__eq__(other)

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Type_Boolean":
        print(7657657)
        return CL_Type_Boolean()


@dataclasses.dataclass
class CL_Type_ByteArray(CL_Type):
    """Encapsulates CL type information associated with a byte array value.

    """
    # Size of associated byte array value.
    size: int

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.BYTE_ARRAY

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.size == other.size

    def to_bytes(self) -> bytes:
        from pycspr.types.cl_int import CL_U32

        return bytes([self.type_key.value]) + CL_U32(self.size).as_bytes()

    def to_json(self) -> str:
        return {
            "ByteArray": self.size
        }

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Type_ByteArray":
        from pycspr.types.cl_int import CL_U32
        size = CL_U32.from_bytes(as_bytes[1:]).value

        return CL_Type_ByteArray(size)


@dataclasses.dataclass
class CL_Type_I32(CL_Type):
    """Encapsulates CL type information associated with a I32 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.I32

    def to_json(self) -> str:
        return "I32"


@dataclasses.dataclass
class CL_Type_I64(CL_Type):
    """Encapsulates CL type information associated with a I64 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.I64

    def to_json(self) -> str:
        return "I64"


@dataclasses.dataclass
class CL_Type_Key(CL_Type):
    """Encapsulates CL type information associated with a key value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.KEY

    def to_json(self) -> str:
        return "Key"


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

    def to_bytes(self) -> bytes:
        return bytes([self.type_key.value]) + CL_Type.to_bytes(self.inner_type)

    def to_json(self) -> str:
        return {
            "List": 123
        }


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

    def to_bytes(self) -> bytes:
        return bytes([self.type_key.value]) + \
               self.key_type.to_bytes() + \
               self.value_type.to_bytes()

    def to_json(self) -> str:
        return {
            "Map": 123
        }


@dataclasses.dataclass
class CL_Type_Option(CL_Type):
    """Encapsulates CL type information associated with an optional value.

    """
    # Inner type within CSPR type system.
    inner_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.OPTION

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.inner_type == other.inner_type

    def to_bytes(self) -> bytes:
        return bytes([self.type_key.value]) + self.inner_type.to_bytes()

    def to_json(self) -> str:
        return {
            "Option": 123
        }

@dataclasses.dataclass
class CL_Type_PublicKey(CL_Type):
    """Encapsulates CL type information associated with a PublicKey value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.PUBLIC_KEY

    def to_json(self) -> str:
        return "PublicKey"


@dataclasses.dataclass
class CL_Type_Result(CL_Type):
    """Encapsulates CL type information associated with a result value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.RESULT

    def to_json(self) -> str:
        raise NotImplementedError()


@dataclasses.dataclass
class CL_Type_String(CL_Type):
    """Encapsulates CL type information associated with a string value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.STRING

    def to_json(self) -> str:
        return "String"


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

    def to_bytes(self) -> bytes:
        return bytes([self.type_key.value]) + CL_Type.to_bytes(self.t0_type)

    def to_json(self) -> str:
        return {
            "Tuple1": self.t0_type.to_json()
        }


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
            
    def to_bytes(self) -> bytes:
        return bytes([self.type_key.value]) + \
               CL_Type.to_bytes(self.t0_type) + \
               CL_Type.to_bytes(self.t1_type)

    def to_json(self) -> str:
        return {
            "Tuple2": [
                self.t0_type.to_json(),
                self.t1_type.to_json()
            ]
        }


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

    def to_bytes(self) -> bytes:
        return bytes([self.type_key.value]) + \
               CL_Type.to_bytes(self.t0_type) + \
               CL_Type.to_bytes(self.t1_type) + \
               CL_Type.to_bytes(self.t2_type)

    def to_json(self) -> str:
        return {
            "Tuple2": [
                self.t0_type.to_json(),
                self.t1_type.to_json(),
                self.t2_type.to_json()
            ]
        }


@dataclasses.dataclass
class CL_Type_U8(CL_Type):
    """Encapsulates CL type information associated with a U8 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U8

    def to_json(self) -> str:
        return "U8"


@dataclasses.dataclass
class CL_Type_U32(CL_Type):
    """Encapsulates CL type information associated with a U32 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U32

    def to_json(self) -> str:
        return "U32"


@dataclasses.dataclass
class CL_Type_U64(CL_Type):
    """Encapsulates CL type information associated with a U64 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U64

    def to_json(self) -> str:
        return "U64"


@dataclasses.dataclass
class CL_Type_U128(CL_Type):
    """Encapsulates CL type information associated with a U128 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U128

    def to_json(self) -> str:
        return "U128"


@dataclasses.dataclass
class CL_Type_U256(CL_Type):
    """Encapsulates CL type information associated with a U256 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U256

    def to_json(self) -> str:
        return "U256"


@dataclasses.dataclass
class CL_Type_U512(CL_Type):
    """Encapsulates CL type information associated with a U512 value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.U512

    def to_json(self) -> str:
        return "U512"


@dataclasses.dataclass
class CL_Type_Unit(CL_Type):
    """Encapsulates CL type information associated with a unit value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.UNIT

    def to_json(self) -> str:
        return "Unit"


@dataclasses.dataclass
class CL_Type_URef(CL_Type):
    """Encapsulates CL type information associated with a uref value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.UREF

    def to_json(self) -> str:
        return "URef"


# Map: CL type key to sub-class.
_CL_TYPE_KEY_CLASS = {
    CL_TypeKey.ANY: CL_Type_Any,
    CL_TypeKey.BOOL: CL_Type_Boolean,
    CL_TypeKey.BYTE_ARRAY: CL_Type_ByteArray,
    CL_TypeKey.I32: CL_Type_I32,
    CL_TypeKey.I64: CL_Type_I64,
    CL_TypeKey.KEY: CL_Type_Key,
    CL_TypeKey.LIST: CL_Type_List,
    CL_TypeKey.MAP: CL_Type_Map,
    CL_TypeKey.OPTION: CL_Type_Option,
    CL_TypeKey.PUBLIC_KEY: CL_Type_PublicKey,
    CL_TypeKey.RESULT: CL_Type_Result,
    CL_TypeKey.STRING: CL_Type_String,
    CL_TypeKey.TUPLE_1: CL_Type_Tuple1,
    CL_TypeKey.TUPLE_2: CL_Type_Tuple2,
    CL_TypeKey.TUPLE_3: CL_Type_Tuple3,
    CL_TypeKey.U8: CL_Type_U8,
    CL_TypeKey.U32: CL_Type_U32,
    CL_TypeKey.U64: CL_Type_U64,
    CL_TypeKey.U128: CL_Type_U128,
    CL_TypeKey.U256: CL_Type_U256,
    CL_TypeKey.U512: CL_Type_U512,
    CL_TypeKey.UNIT: CL_Type_Unit,
    CL_TypeKey.UREF: CL_Type_URef,
}

# Map: CL type sub-class to JSON tag.
_CL_TYPE_JSON_TAG = {
    CL_Type_Any: "Any",
    CL_Type_Boolean: "Bool",
    CL_Type_ByteArray: "ByteArray",
    CL_Type_I32: "I32",
    CL_Type_I64: "I64",
    CL_Type_Key: "Key",
    CL_Type_List: "List",
    CL_Type_Map: "Map",
    CL_Type_Option: "Option",
    CL_Type_PublicKey: "PublicKey",
    CL_Type_Result: "Result",
    CL_Type_String: "String",
    CL_Type_Tuple1: "Tuple1",
    CL_Type_Tuple2: "Tuple2",
    CL_Type_Tuple3: "Tuple3",
    CL_Type_U8: "U8",
    CL_Type_U32: "U32",
    CL_Type_U64: "U64",
    CL_Type_U128: "U128",
    CL_Type_U256: "U256",
    CL_Type_U512: "U512",
    CL_Type_Unit: "Unit",
    CL_Type_URef: "URef",
}

# Map: JSON tag to CL type sub-class.
_JSON_TAG_CL_TYPE = {j: i for i, j in _CL_TYPE_JSON_TAG.items()}
