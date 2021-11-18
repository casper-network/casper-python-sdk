from pycspr.serialisation.cl_type_from_json import decode as cl_type_from_json
from pycspr.serialisation.cl_value_from_bytes import decode as cl_value_from_bytes

from pycspr.types import cl_types
from pycspr.types import cl_values
from pycspr.types import CL_TYPEKEY_TO_CL_VALUE_TYPE


def decode(encoded: dict):
    cl_type: cl_types.CL_Type = cl_type_from_json(encoded["cl_type"])
    cl_value_type: cl_values.CL_Value = CL_TYPEKEY_TO_CL_VALUE_TYPE[cl_type.type_key]

    return cl_value_from_bytes(encoded["bytes"], cl_value_type)
