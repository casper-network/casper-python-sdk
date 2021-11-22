from pycspr.types.cl import cl_types
from pycspr.types.cl import cl_values
from pycspr.serialisation.cl_value_to_bytes import encode as cl_value_to_bytes
from pycspr.serialisation.cl_type_to_json import encode as cl_type_to_json


def encode(entity: cl_values.CL_Value) -> dict:
    return {
        "cl_type": cl_type_to_json(_get_cl_type(entity)),
        "bytes": cl_value_to_bytes(entity).hex(),
        "parsed": _get_parsed(entity)
    }


def _get_cl_type(entity: cl_types.CL_Type) -> cl_types.CL_Type:
    if isinstance(entity, cl_values.CL_Any):
        pass

    elif isinstance(entity, cl_values.CL_Bool):
        return cl_types.CL_Type_Bool()

    elif isinstance(entity, cl_values.CL_ByteArray):
        return cl_types.CL_Type_ByteArray(len(entity.value))

    elif isinstance(entity, cl_values.CL_I32):
        return cl_types.CL_Type_I32()

    elif isinstance(entity, cl_values.CL_I64):
        return cl_types.CL_Type_I64()

    elif isinstance(entity, cl_values.CL_Key):
        return cl_types.CL_Type_Key()

    elif isinstance(entity, cl_values.CL_List):
        return cl_types.CL_Type_List(entity.item_type)

    elif isinstance(entity, cl_values.CL_Map):
        pass

    elif isinstance(entity, cl_values.CL_Option):
        return cl_types.CL_Type_Option(entity.option_type)

    elif isinstance(entity, cl_values.CL_PublicKey):
        return cl_types.CL_Type_PublicKey()

    elif isinstance(entity, cl_values.CL_Result):
        return cl_types.CL_Type_Result()

    elif isinstance(entity, cl_values.CL_String):
        return cl_types.CL_Type_String()

    elif isinstance(entity, cl_values.CL_Tuple1):
        pass

    elif isinstance(entity, cl_values.CL_Tuple2):
        pass

    elif isinstance(entity, cl_values.CL_Tuple3):
        pass

    elif isinstance(entity, cl_values.CL_U8):
        return cl_types.CL_Type_U8()

    elif isinstance(entity, cl_values.CL_U32):
        return cl_types.CL_Type_U32()

    elif isinstance(entity, cl_values.CL_U64):
        return cl_types.CL_Type_U64()

    elif isinstance(entity, cl_values.CL_U128):
        return cl_types.CL_Type_U128()

    elif isinstance(entity, cl_values.CL_U256):
        return cl_types.CL_Type_U256()

    elif isinstance(entity, cl_values.CL_U512):
        return cl_types.CL_Type_U512()

    elif isinstance(entity, cl_values.CL_Unit):
        return cl_types.CL_Type_Unit()

    elif isinstance(entity, cl_values.CL_URef):
        return cl_types.CL_Type_URef()

    raise ValueError(f"CL value cannot be mapped to a CL type: {entity}")


def _get_parsed(entity: cl_types.CL_Type) -> cl_types.CL_Type:
    if isinstance(entity, cl_values.CL_Any):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Bool):
        return str(entity.value)

    elif isinstance(entity, cl_values.CL_ByteArray):
        return entity.value.hex()

    elif isinstance(entity, cl_values.CL_I32):
        return entity.value

    elif isinstance(entity, cl_values.CL_I64):
        return entity.value

    elif isinstance(entity, cl_values.CL_Key):
        return entity.to_string()

    elif isinstance(entity, cl_values.CL_List):
        return [str(i) for i in entity.vector]

    elif isinstance(entity, cl_values.CL_Map):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Option):
        return _get_parsed(entity.value) if entity.value else ""

    elif isinstance(entity, cl_values.CL_PublicKey):
        return entity.account_key.hex()

    elif isinstance(entity, cl_values.CL_Result):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_String):
        return entity.value

    elif isinstance(entity, cl_values.CL_Tuple1):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Tuple2):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_Tuple3):
        raise NotImplementedError()

    elif isinstance(entity, cl_values.CL_U8):
        return entity.value

    elif isinstance(entity, cl_values.CL_U32):
        return entity.value

    elif isinstance(entity, cl_values.CL_U64):
        return entity.value

    elif isinstance(entity, cl_values.CL_U128):
        return str(entity.value)

    elif isinstance(entity, cl_values.CL_U256):
        return str(entity.value)

    elif isinstance(entity, cl_values.CL_U512):
        return str(entity.value)

    elif isinstance(entity, cl_values.CL_Unit):
        return ""

    elif isinstance(entity, cl_values.CL_URef):
        return entity.to_string()
