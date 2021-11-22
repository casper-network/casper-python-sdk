import typing

from pycspr.serialisation.bytearray import cl_u32
from pycspr.types import CLType
from pycspr.types import CLTypeKey
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_Key
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3


# Map: CL type key to JSON tag.
_JSON_TYPE_TAGS = {
    CLTypeKey.ANY: "Any",
    CLTypeKey.BOOL: "Bool",
    CLTypeKey.BYTE_ARRAY: "ByteArray",
    CLTypeKey.I32: "I32",
    CLTypeKey.I64: "I64",
    CLTypeKey.KEY: "Key",
    CLTypeKey.LIST: "List",
    CLTypeKey.MAP: "Map",
    CLTypeKey.OPTION: "Option",
    CLTypeKey.PUBLIC_KEY: "PublicKey",
    CLTypeKey.RESULT: "Result",
    CLTypeKey.STRING: "String",
    CLTypeKey.TUPLE_1: "Tuple1",
    CLTypeKey.TUPLE_2: "Tuple2",
    CLTypeKey.TUPLE_3: "Tuple3",
    CLTypeKey.U8: "U8",
    CLTypeKey.U32: "U32",
    CLTypeKey.U64: "U64",
    CLTypeKey.U128: "U128",
    CLTypeKey.U256: "U256",
    CLTypeKey.U512: "U512",
    CLTypeKey.UNIT: "Unit",
    CLTypeKey.UREF: "URef",
}

# Map: JSON tag to CL type key.
_JSON_TYPE_TAGS_INVERSE = {j: i for i, j in _JSON_TYPE_TAGS.items()}


def from_bytes(value: bytes) -> object:
    raise NotImplementedError()


def from_json(value: typing.Union[dict, str]) -> object:
    def _byte_array():
        return CLType_ByteArray(size=value["ByteArray"])

    def _list():
        return CLType_List(
            inner_type=decode_cl_type(value["List"])
            )

    def _map():
        return CLType_Map(
            value_type=decode_cl_type(value["Map"])
            )

    def _option():
        return CLType_Option(
            inner_type=decode_cl_type(value["Option"])
            )

    def _simple():
        return CLType_Simple(
            type_key=_JSON_TYPE_TAGS_INVERSE[value]
            )

    def _tuple_1():
        return CLType_Tuple1(
            t0_type=from_json(value["Tuple1"])
            )

    def _tuple_2():
        return CLType_Tuple2(
            t0_type=from_json(value["Tuple2"][0]),
            t1_type=from_json(value["Tuple2"][1])
            )

    def _tuple_3():
        return CLType_Tuple3(
            t0_type=from_json(value["Tuple3"][0]),
            t1_type=from_json(value["Tuple3"][1]),
            t2_type=from_json(value["Tuple3"][2])
            )

    if isinstance(value, dict):
        if "ByteArray" in value:
            return _byte_array()
        elif "List" in value:
            return _list()
        elif "Map" in value:
            return _map()
        elif "Option" in value:
            return _option()
        elif "Tuple1" in value:
            return _tuple_1()
        elif "Tuple2" in value:
            return _tuple_2()
        elif "Tuple3" in value:
            return _tuple_3()
        else:
            raise NotImplementedError()
    else:
        return _simple()


def to_bytes(entity: CLType) -> bytes:
    def _byte_array():
        return bytes([entity.type_key.value]) + cl_u32.to_bytes(entity.size)

    def _key():
        return bytes([entity.type_key.value]) + bytes([entity.key_type.value])

    def _list():
        return bytes([entity.type_key.value]) + to_bytes(entity.inner_type)

    def _map():
        raise NotImplementedError()

    def _option():
        return bytes([entity.type_key.value]) + to_bytes(entity.inner_type)

    def _simple():
        return bytes([entity.type_key.value])

    def _tuple_1():
        raise NotImplementedError()

    def _tuple_2():
        raise NotImplementedError()

    def _tuple_3():
        raise NotImplementedError()

    _ENCODERS = {
        CLType_ByteArray: _byte_array,
        CLType_Key: _key,
        CLType_List: _list,
        CLType_Map: _map,
        CLType_Option: _option,
        CLType_Simple: _simple,
        CLType_Tuple1: _tuple_1,
        CLType_Tuple2: _tuple_2,
        CLType_Tuple3: _tuple_3,
    }

    return _ENCODERS[type(entity)]()


def to_json(entity: CLType) -> dict:
    def _byte_array():
        return {
            "ByteArray": entity.size
        }

    def _key():
        return "Key"

    def _list():
        return {
            "List": to_json(entity.inner_type)
        }

    def _map():
        return {
            "Map": to_json(entity.inner_type)
        }

    def _option():
        return {
            "Option": to_json(entity.inner_type)
        }

    def _simple():
        return _JSON_TYPE_TAGS[entity.type_key]

    def _tuple_1():
        return {
            "Tuple1": to_json(entity.t0_type)
        }

    def _tuple_2():
        return {
            "Tuple2": [
                to_json(entity.t0_type),
                to_json(entity.t1_type)
                ]
        }

    def _tuple_3():
        return {
            "Tuple3": [
                to_json(entity.t0_type),
                to_json(entity.t1_type),
                to_json(entity.t2_type)
                ]
        }

    _ENCODERS = {
        CLType_ByteArray: _byte_array,
        CLType_Key: _key,
        CLType_List: _list,
        CLType_Map: _map,
        CLType_Option: _option,
        CLType_Simple: _simple,
        CLType_Tuple1: _tuple_1,
        CLType_Tuple2: _tuple_2,
        CLType_Tuple3: _tuple_3,
    }

    return _ENCODERS[type(entity)]()
