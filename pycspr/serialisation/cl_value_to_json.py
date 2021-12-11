from pycspr.types import cl_types
from pycspr.types import cl_values
from pycspr.serialisation.cl_value_to_bytes import encode as cl_value_to_bytes
from pycspr.serialisation.cl_value_to_cl_type import encode as cl_value_to_cl_type
from pycspr.serialisation.cl_type_to_json import encode as cl_type_to_json


def encode(entity: cl_values.CL_Value) -> dict:
    cl_type = cl_value_to_cl_type(entity)
    
    return {
        "cl_type": cl_type_to_json(cl_type),
        "bytes": cl_value_to_bytes(entity).hex(),
        "parsed": _get_parsed(entity)
    }


def _get_parsed(entity: cl_values.CL_Value) -> object:
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
        return [{
            "key": _get_parsed(k),
            "value": _get_parsed(v),
        } for (k, v) in entity.value]

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
