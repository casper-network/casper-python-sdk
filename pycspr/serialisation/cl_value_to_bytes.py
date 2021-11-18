from pycspr.types import cl_values
from pycspr.utils.conversion import int_to_le_bytes


def encode(entity: cl_values.CL_Value) -> bytes:
    if isinstance(entity, cl_values.CL_Any):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Bool):
        return bytes([int(entity.value)])

    elif isinstance(entity, cl_values.CL_ByteArray):
        return entity.value

    elif isinstance(entity, cl_values.CL_I32):
        return int_to_le_bytes(entity.value, 4, True)

    elif isinstance(entity, cl_values.CL_I64):
        return int_to_le_bytes(entity.value, 8, True)

    elif isinstance(entity, cl_values.CL_Key):
        return bytes([entity.key_type.value]) + entity.identifier

    elif isinstance(entity, cl_values.CL_List):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Map):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Option):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_PublicKey):
        return bytes([entity.algo.value]) + entity.pbk

    elif isinstance(entity, cl_values.CL_Result):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_String):
        encoded: bytes = (entity.value or "").encode("utf-8")
        return encode(cl_values.CL_U32(len(encoded))) + encoded

    elif isinstance(entity, cl_values.CL_Tuple1):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Tuple2):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Tuple3):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_U8):
        return int_to_le_bytes(entity.value, 1, False)

    elif isinstance(entity, cl_values.CL_U32):
        return int_to_le_bytes(entity.value, 4, False)

    elif isinstance(entity, cl_values.CL_U64):
        return int_to_le_bytes(entity.value, 8, False)

    elif isinstance(entity, cl_values.CL_U128):
        if cl_values.CL_U8.is_in_range(entity.value):
            byte_length = 1
        elif cl_values.CL_U32.is_in_range(entity.value):
            byte_length = 4
        elif cl_values.CL_U64.is_in_range(entity.value):
            byte_length = 8
        elif cl_values.CL_U128.is_in_range(entity.value):
            byte_length = 16
        else:
            raise ValueError("Invalid U128: max size exceeded")        
        return int_to_le_bytes(entity.value, byte_length, False)

    elif isinstance(entity, cl_values.CL_U256):
        if cl_values.CL_U8.is_in_range(entity.value):
            byte_length = 1
        elif cl_values.CL_U32.is_in_range(entity.value):
            byte_length = 4
        elif cl_values.CL_U64.is_in_range(entity.value):
            byte_length = 8
        elif cl_values.CL_U128.is_in_range(entity.value):
            byte_length = 16
        elif cl_values.CL_U256.is_in_range(entity.value):
            byte_length = 32
        else:
            raise ValueError("Invalid U256: max size exceeded")
        return int_to_le_bytes(entity.value, byte_length, False)

    elif isinstance(entity, cl_values.CL_U512):
        if cl_values.CL_U8.is_in_range(entity.value):
            byte_length = 1
        elif cl_values.CL_U32.is_in_range(entity.value):
            byte_length = 4
        elif cl_values.CL_U64.is_in_range(entity.value):
            byte_length = 8
        elif cl_values.CL_U128.is_in_range(entity.value):
            byte_length = 16
        elif cl_values.CL_U256.is_in_range(entity.value):
            byte_length = 32
        elif cl_values.CL_U512.is_in_range(entity.value):
            byte_length = 64
        else:
            raise ValueError("Invalid U512: max size exceeded")
        return int_to_le_bytes(entity.value, byte_length, False)

    elif isinstance(entity, cl_values.CL_Unit):
        return bytes([])

    elif isinstance(entity, cl_values.CL_URef):
        return entity.address + bytes([entity.access_rights.value])

    else:
        raise ValueError("CL value cannot be encoded as bytes")
