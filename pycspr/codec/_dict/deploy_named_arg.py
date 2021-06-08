
from pycspr.codec._bytearray import cl
from pycspr.codec._bytearray import deploy_named_arg
from pycspr.types.cl import CLTypeKey
from pycspr.types.deploy import ExecutionInfo
from pycspr.types.deploy import ExecutionArgument



def _not_implemented(arg: ExecutionInfo):
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
    CLTypeKey.BOOL: lambda arg: arg.cl_typeof.name,
    CLTypeKey.I32: lambda arg: arg.cl_typeof.name,
    CLTypeKey.I64: lambda arg: arg.cl_typeof.name,
    CLTypeKey.U8: lambda arg: arg.cl_typeof.name,
    CLTypeKey.U32: lambda arg: arg.cl_typeof.name,
    CLTypeKey.U64: lambda arg: arg.cl_typeof.name,
    CLTypeKey.U128: lambda arg: arg.cl_typeof.name,
    CLTypeKey.U256: lambda arg: arg.cl_typeof.name,
    CLTypeKey.U512: lambda arg: arg.cl_typeof.name,
    CLTypeKey.UNIT: _not_implemented,
    CLTypeKey.STRING: _not_implemented,
    CLTypeKey.KEY: _not_implemented,
    CLTypeKey.UREF: _not_implemented,
    CLTypeKey.OPTION: _encode_option,
    CLTypeKey.LIST: _not_implemented,
    CLTypeKey.BYTE_ARRAY: _encode_byte_array,
    CLTypeKey.RESULT: _not_implemented,
    CLTypeKey.MAP: _not_implemented,
    CLTypeKey.TUPLE_1: _not_implemented,
    CLTypeKey.TUPLE_2: _not_implemented,
    CLTypeKey.TUPLE_3: _not_implemented,
    CLTypeKey.ANY: _not_implemented,
    CLTypeKey.PUBLIC_KEY: _not_implemented
}


def to_json(arg: ExecutionInfo) -> bytearray:
    """Maps domain type instance to a JSON string for interpretation by a CSPR node.
    
    :param ExecutionInfo instance: An execution argument data to be encoded.

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
