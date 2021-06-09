from pycspr.codec.json.encode_execution_arg import encode as encode_execution_arg
from pycspr.types.deploy import ExecutionInfo
from pycspr.types.deploy import ExecutionInfo_ModuleBytes
from pycspr.types.deploy import ExecutionInfo_Transfer


def _encode_module_bytes(entity: ExecutionInfo_ModuleBytes) -> dict:
    return {
        "ModuleBytes": {
            "args": [encode_execution_arg(i) for i in entity.args]
        }
    }


def _encode_transfer(entity: ExecutionInfo_Transfer) -> dict:
    return {
        "Transfer": {
            "args": [encode_execution_arg(i) for i in entity.args]            
        }
    }


# Map: domain type <-> encoder.
_ENCODERS = {
    ExecutionInfo_ModuleBytes: _encode_module_bytes,
    ExecutionInfo_Transfer: _encode_transfer,
}


def encode(entity: ExecutionInfo) -> str:
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return _ENCODERS[type(entity)](entity)
