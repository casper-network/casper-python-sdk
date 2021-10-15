from pycspr.serialisation.byte_array.encoder.cl_primitive import encode_u32
from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLType_StorageKey
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3


def encode_cl_type(entity: CLType) -> bytes:
    """Encodes a CL type definition.

    """
    def encode_byte_array():
        return bytes([entity.type_key.value]) + encode_u32(entity.size)

    def encode_list():
        raise NotImplementedError()

    def encode_map():
        raise NotImplementedError()

    def encode_option():
        return bytes([entity.type_key.value]) + encode_cl_type(entity.inner_type)

    def encode_simple():
        return bytes([entity.type_key.value])

    def encode_storage_key():
        return bytes([entity.type_key.value]) + bytes([entity.key_type.value])

    def encode_tuple_1():
        raise NotImplementedError()

    def encode_tuple_2():
        raise NotImplementedError()

    def encode_tuple_3():
        raise NotImplementedError()

    _ENCODERS = {
        CLType_ByteArray: encode_byte_array,
        CLType_List: encode_list,
        CLType_Map: encode_map,
        CLType_Option: encode_option,
        CLType_Simple: encode_simple,
        CLType_StorageKey: encode_storage_key,
        CLType_Tuple1: encode_tuple_1,
        CLType_Tuple2: encode_tuple_2,
        CLType_Tuple3: encode_tuple_3,
    }

    return _ENCODERS[type(entity)]()
