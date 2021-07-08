import datetime
import json

from pycspr.codec.byte_array import encode as byte_array_encoder
from pycspr.types.cl import CLValue
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType_ByteArray
from pycspr.types.cl import CLType_List
from pycspr.types.cl import CLType_Map
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLType_Simple
from pycspr.types.cl import CLType_Tuple1
from pycspr.types.cl import CLType_Tuple2
from pycspr.types.cl import CLType_Tuple3
from pycspr.types.deploy import Deploy
from pycspr.types.deploy import DeployApproval
from pycspr.types.deploy import DeployHeader
from pycspr.types.deploy import Digest
from pycspr.types.deploy import ExecutionArgument
from pycspr.types.deploy import ExecutionInfo
from pycspr.types.deploy import ExecutionInfo_ModuleBytes
from pycspr.types.deploy import ExecutionInfo_Transfer
from pycspr.types.deploy import Signature
from pycspr.types.deploy import Timestamp



def encode_approval(entity: DeployApproval):
    return {
        "signer": entity.signer.hex(),
        "signature": entity.signature.hex(),
    }


def encode_cl_type(entity: CLType):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    _ENCODERS = {
        # Byte array.
        CLType_ByteArray: lambda: {
            "ByteArray": entity.size
        },

        # List.
        CLType_List: lambda: {
            "List": encode_cl_type(entity.inner_type)
        },

        # Map.
        CLType_Map: lambda: {
            "Map": encode_cl_type(entity.inner_type)
        },

        # Optional.
        CLType_Option: lambda: {
            "Option": encode_cl_type(entity.inner_type)
        },

        # Simple type.
        CLType_Simple: lambda: entity.typeof.name,

        # 1-ary tuple.
        CLType_Tuple1: lambda: {
            "Tuple1": encode_cl_type(entity.t0_type)
        },

        # 2-ary tuple.
        CLType_Tuple2: lambda: {
            "Tuple2": [encode_cl_type(entity.t0_type), encode_cl_type(entity.t1_type)]
        },

        # 3-ary tuple.
        CLType_Tuple3: lambda: {
            "Tuple3": [encode_cl_type(entity.t0_type), encode_cl_type(entity.t1_type), encode_cl_type(entity.t2_type)]
        },
    }

    return _ENCODERS[type(entity)]()


def encode_cl_value(entity: CLValue):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return {
        "bytes": bytes(byte_array_encoder(entity)).hex(),
        "cl_type": encode_cl_type(entity.cl_type),
        "parsed": str(entity.parsed),
    }


def encode_deploy(entity: Deploy):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return {
        "approvals": [encode_approval(i) for i in entity.approvals],
        "hash": encode_digest(entity.hash),
        "header": encode_deploy_header(entity.header),
        "payment": encode_execution_info(entity.payment),
        "session": encode_execution_info(entity.session)
    }


def encode_deploy_header(entity: DeployHeader):
    return {
        "account": entity.accountPublicKey.account_key,
        "body_hash": encode_digest(entity.body_hash),
        "chain_name": entity.chain_name,
        "dependencies": entity.dependencies,
        "gas_price": entity.gas_price,
        "timestamp": encode_timestamp(entity.timestamp),
        "ttl": entity.ttl.humanized
    }


def encode_digest(entity: Digest) -> str:
    if isinstance(entity, bytes):
        return entity.hex()
    elif isinstance(entity, list):
        return bytes(entity).hex()
    return entity


def encode_execution_argument(entity: ExecutionArgument):
    return [
        entity.name,
        encode_cl_value(entity.value)
    ]


def encode_execution_info(entity: ExecutionInfo) -> str:
    def _encode_module_bytes() -> dict:
        return {
            "ModuleBytes": {
                "args": [encode_execution_argument(i) for i in entity.args],
                "module_bytes": entity.module_bytes.hex()
            }
        }


    def _encode_transfer() -> dict:
        return {
            "Transfer": {
                "args": [encode_execution_argument(i) for i in entity.args]            
            }
        }

    _ENCODERS = {
        ExecutionInfo_ModuleBytes: _encode_module_bytes,
        ExecutionInfo_Transfer: _encode_transfer,
    }

    return _ENCODERS[type(entity)]()


def encode_timestamp(entity: Timestamp) -> str:
    # NOTE: assume timestamp is UTC millisecond precise.
    timestamp_ms = round(entity, 3)
    timestamp_iso = datetime.datetime.utcfromtimestamp(timestamp_ms).isoformat()

    return f"{timestamp_iso[:-3]}Z"


# Map: entity type <-> encoder.
_ENCODERS = {
    Deploy: encode_deploy,
}


def encode(entity: object) -> str:
    """Maps domain entity to it's JSON representation.
    
    :param entity: A domain entity.
    :returns: JSON encoded representation.

    """
    as_dict = _ENCODERS[type(entity)](entity)

    return json.dumps(as_dict, indent=4)
