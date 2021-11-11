import typing

from pycspr.serialisation import cl_u32
from pycspr.types import CLType
from pycspr.types import CLTypeKey
from pycspr.types import CLType_Any
from pycspr.types import CLType_Boolean
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_I32
from pycspr.types import CLType_I64
from pycspr.types import CLType_Key
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_PublicKey
from pycspr.types import CLType_Result
from pycspr.types import CLType_String
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3
from pycspr.types import CLType_U8
from pycspr.types import CLType_U32
from pycspr.types import CLType_U64
from pycspr.types import CLType_U128
from pycspr.types import CLType_U256
from pycspr.types import CLType_U512
from pycspr.types import CLType_Unit
from pycspr.types import CLType_URef


# Map: CL type sub-class to JSON tag.
_CL_TYPE_JSON_TAG = {
    CLType_Any: "Any",
    CLType_Boolean: "Bool",
    CLType_ByteArray: "ByteArray",
    CLType_I32: "I32",
    CLType_I64: "I64",
    CLType_Key: "Key",
    CLType_List: "List",
    CLType_Map: "Map",
    CLType_Option: "Option",
    CLType_PublicKey: "PublicKey",
    CLType_Result: "Result",
    CLType_String: "String",
    CLType_Tuple1: "Tuple1",
    CLType_Tuple2: "Tuple2",
    CLType_Tuple3: "Tuple3",
    CLType_U8: "U8",
    CLType_U32: "U32",
    CLType_U64: "U64",
    CLType_U128: "U128",
    CLType_U256: "U256",
    CLType_U512: "U512",
    CLType_Unit: "Unit",
    CLType_URef: "URef",
}

# Map: JSON tag to CL type sub-class.
_JSON_TAG_CL_TYPE = {j: i for i, j in _CL_TYPE_JSON_TAG.items()}

# Map: CL type key to sub-class.
_CL_TYPE_KEY_CLASS = {
    CLTypeKey.ANY: CLType_Any,
    CLTypeKey.BOOL: CLType_Boolean,
    CLTypeKey.BYTE_ARRAY: CLType_ByteArray,
    CLTypeKey.I32: CLType_I32,
    CLTypeKey.I64: CLType_I64,
    CLTypeKey.KEY: CLType_Key,
    CLTypeKey.LIST: CLType_List,
    CLTypeKey.MAP: CLType_Map,
    CLTypeKey.OPTION: CLType_Option,
    CLTypeKey.PUBLIC_KEY: CLType_PublicKey,
    CLTypeKey.RESULT: CLType_Result,
    CLTypeKey.STRING: CLType_String,
    CLTypeKey.TUPLE_1: CLType_Tuple1,
    CLTypeKey.TUPLE_2: CLType_Tuple2,
    CLTypeKey.TUPLE_3: CLType_Tuple3,
    CLTypeKey.U8: CLType_U8,
    CLTypeKey.U32: CLType_U32,
    CLTypeKey.U64: CLType_U64,
    CLTypeKey.U128: CLType_U128,
    CLTypeKey.U256: CLType_U256,
    CLTypeKey.U512: CLType_U512,
    CLTypeKey.UNIT: CLType_Unit,
    CLTypeKey.UREF: CLType_URef,
}


def from_bytes(value: bytes) -> object:
    type_tag = CLTypeKey(value[0])
    kls = _CL_TYPE_KEY_CLASS[type_tag]
    if type_tag == CLTypeKey.BYTE_ARRAY:
        return kls(cl_u32.from_bytes(value[1:]))
    elif type_tag == CLTypeKey.LIST:
        return kls(from_bytes(value[1:]))
    elif type_tag == CLTypeKey.MAP:
        return kls(from_bytes(value[1:]), from_bytes(value[1:]))
    elif type_tag == CLTypeKey.OPTION:
        return kls(from_bytes(value[1:]))
    elif type_tag == CLTypeKey.TUPLE_1:
        return kls(from_bytes(value[1:]))
    elif type_tag == CLTypeKey.TUPLE_2:
        return kls(from_bytes(value[1:]), from_bytes(value[1:]))
    elif type_tag == CLTypeKey.TUPLE_3:
        return kls(from_bytes(value[1:]), from_bytes(value[1:]), from_bytes(value[1:]))
    else:
        return kls()


def to_bytes(entity: CLType) -> bytes:
    kls = type(entity)
    type_tag = bytes([entity.type_key.value])
    if kls == CLType_ByteArray:
        return type_tag + cl_u32.to_bytes(entity.size)
    elif kls == CLType_List:
        return type_tag + to_bytes(entity.inner_type)
    elif kls == CLType_Map:
        return type_tag + to_bytes(entity.key_type) + to_bytes(entity.value_type)
    elif kls == CLType_Option:
        return type_tag + to_bytes(entity.inner_type)
    elif kls == CLType_Tuple1:
        return type_tag + to_bytes(entity.t0_type)
    elif kls == CLType_Tuple2:
        return type_tag + to_bytes(entity.t0_type) + to_bytes(entity.t1_type)
    elif kls == CLType_Tuple3:
        return type_tag + to_bytes(entity.t0_type) + to_bytes(entity.t1_type) + \
               to_bytes(entity.t2_type)
    else:
        return type_tag


def from_json(value: typing.Union[dict, str]) -> object:
    if isinstance(value, str):
        return _JSON_TAG_CL_TYPE[value]()
    elif "ByteArray" in value:
        return CLType_ByteArray(
            value["ByteArray"]
            )
    elif "List" in value:
        return CLType_List(
            from_json(value["List"])
            )
    elif "Map" in value:
        return CLType_Map(
            from_json(value["Map"]["key"]),
            from_json(value["Map"]["value"])
            )
    elif "Option" in value:
        return CLType_Option(
            from_json(value["Option"])
            )
    elif "Tuple1" in value:
        return CLType_Tuple1(
            from_json(value["Tuple1"])
            )
    elif "Tuple2" in value:
        return CLType_Tuple2(
            from_json(value["Tuple2"][0]),
            from_json(value["Tuple2"][1])
            )
    elif "Tuple3" in value:
        return CLType_Tuple3(
            from_json(value["Tuple3"][0]),
            from_json(value["Tuple3"][1]),
            from_json(value["Tuple3"][2])
            )
    else:
        raise NotImplementedError()


def to_json(entity: CLType) -> dict:
    kls = type(entity)
    if kls not in _CL_TYPE_JSON_TAG:
        raise ValueError("Invalid cl type definition")

    type_tag = _CL_TYPE_JSON_TAG[kls]
    if kls == CLType_ByteArray:
        return {
            type_tag: entity.size
        }
    elif kls == CLType_List:
        return {
            type_tag: to_json(entity.inner_type)
        }
    elif kls == CLType_Map:
        return {
            type_tag: {
                "key": to_json(entity.key_type),
                "value": to_json(entity.value_type)
            }
        }
    elif kls == CLType_Option:
        return {
            type_tag: to_json(entity.inner_type)
        }
    elif kls == CLType_Tuple1:
        return {
            type_tag: to_json(entity.t0_type)
        }
    elif kls == CLType_Tuple2:
        return {
            type_tag: [
                to_json(entity.t0_type),
                to_json(entity.t1_type)
                ]
        }
    elif kls == CLType_Tuple3:
        return {
            type_tag: [
                to_json(entity.t0_type),
                to_json(entity.t1_type),
                to_json(entity.t2_type)
                ]
        }
    else:
        return type_tag
