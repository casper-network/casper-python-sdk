
from pycspr.codec._bytearray import cl
from pycspr.codec._bytearray import deploy_named_arg
from pycspr.types import CLType
from pycspr.types import DeployExecutable
from pycspr.types import DeployNamedArg

from pycspr.types.cl import CLType
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType



def _not_implemented(arg: DeployNamedArg):
    raise NotImplementedError("CL value type unencodeable")


def _encode_byte_array(arg):
    return {
        "ByteArray": len(arg.value)
        }


def _encode_option(arg):
    return {
        "Option": _CL_TYPE_ENCODERS[arg.cl_type_info.innter]
        }


# Map: cl-type <-> encoder.
_CL_TYPE_ENCODERS = {
    CLType.BOOL: lambda arg: arg.cl_typeof.name,
    CLType.I32: lambda arg: arg.cl_typeof.name,
    CLType.I64: lambda arg: arg.cl_typeof.name,
    CLType.U8: lambda arg: arg.cl_typeof.name,
    CLType.U32: lambda arg: arg.cl_typeof.name,
    CLType.U64: lambda arg: arg.cl_typeof.name,
    CLType.U128: lambda arg: arg.cl_typeof.name,
    CLType.U256: lambda arg: arg.cl_typeof.name,
    CLType.U512: lambda arg: arg.cl_typeof.name,
    CLType.UNIT: _not_implemented,
    CLType.STRING: _not_implemented,
    CLType.KEY: _not_implemented,
    CLType.UREF: _not_implemented,
    CLType.OPTION: _encode_option,
    CLType.LIST: _not_implemented,
    CLType.BYTE_ARRAY: _encode_byte_array,
    CLType.RESULT: _not_implemented,
    CLType.MAP: _not_implemented,
    CLType.TUPLE_1: _not_implemented,
    CLType.TUPLE_2: _not_implemented,
    CLType.TUPLE_3: _not_implemented,
    CLType.ANY: _not_implemented,
    CLType.PUBLIC_KEY: _not_implemented
}


def to_json(arg: DeployNamedArg) -> bytearray:
    """Maps domain type instance to a JSON string for interpretation by a CSPR node.
    
    :param DeployNamedArg instance: Named argument data to be encoded.

    """
    try:
        cl_type_encoder = _CL_TYPE_ENCODERS[arg.cl_type_info.typeof]
    except KeyError:
        raise NotImplementedError("CL value type unencodeable")
    else:
        return [
            arg.name,
            {
                "bytes": bytes([]),
                "cl_type": cl_type_encoder(arg),
                "parsed": str(arg.value),
            }
        ]
