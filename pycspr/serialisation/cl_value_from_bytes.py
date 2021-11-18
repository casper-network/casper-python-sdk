from pycspr import crypto
from pycspr.types import cl_values
from pycspr.utils.conversion import le_bytes_to_int


def decode(encoded: bytes, cl_value_type: cl_values.CL_Value) -> cl_values.CL_Value:
    if cl_value_type is cl_values.CL_Any:
        raise NotImplementedError()

    elif cl_value_type is cl_values.CL_Bool:
        return cl_values.CL_Bool(bool(encoded[0]))

    elif cl_value_type is cl_values.CL_ByteArray:
        return cl_values.CL_ByteArray(encoded)

    elif cl_value_type is cl_values.CL_I32:
        return cl_values.CL_I32(le_bytes_to_int(encoded, True))

    elif cl_value_type is cl_values.CL_I64:
        return cl_values.CL_I64(le_bytes_to_int(encoded, True))

    elif cl_value_type is cl_values.CL_Key:
        return cl_values.CL_Key(encoded[1:], cl_values.CL_KeyType(encoded[0]))

    elif cl_value_type is cl_values.CL_List:
        pass

    elif cl_value_type is cl_values.CL_Map:
        pass

    elif cl_value_type is cl_values.CL_Option:
        pass

    elif cl_value_type is cl_values.CL_PublicKey:
        return cl_values.CL_PublicKey(crypto.KeyAlgorithm(encoded[0]), encoded[1:])

    elif cl_value_type is cl_values.CL_Result:
        pass

    elif cl_value_type is cl_values.CL_String:
        return cl_values.CL_String(encoded[4:].decode("utf-8"))

    elif cl_value_type is cl_values.CL_Tuple1:
        pass

    elif cl_value_type is cl_values.CL_Tuple2:
        pass

    elif cl_value_type is cl_values.CL_Tuple3:
        pass

    elif cl_value_type is cl_values.CL_U8:
        return cl_values.CL_U8(le_bytes_to_int(encoded, False))

    elif cl_value_type is cl_values.CL_U32:
        return cl_values.CL_U32(le_bytes_to_int(encoded, False))

    elif cl_value_type is cl_values.CL_U64:
        return cl_values.CL_U64(le_bytes_to_int(encoded, False))

    elif cl_value_type is cl_values.CL_U128:
        return cl_values.CL_U128(le_bytes_to_int(encoded, False))

    elif cl_value_type is cl_values.CL_U256:
        return cl_values.CL_U256(le_bytes_to_int(encoded, False))

    elif cl_value_type is cl_values.CL_U512:
        return cl_values.CL_U512(le_bytes_to_int(encoded, False))

    elif cl_value_type is cl_values.CL_Unit:
        return cl_values.CL_Unit()

    elif cl_value_type is cl_values.CL_URef:
        return cl_values.CL_URef(cl_values.CL_AccessRights(encoded[-1]), encoded[:-1])

    else:
        raise ValueError(f"Unsupported CL value type: {cl_value_type}")
