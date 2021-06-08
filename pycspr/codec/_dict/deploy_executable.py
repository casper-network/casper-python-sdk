
from pycspr.codec._bytearray import cl
from pycspr.codec._bytearray import deploy_named_arg
from pycspr.types.cl import CLTypeKey
from pycspr.types import ExecutionInfo
from pycspr.types import ExecutionInfo_ModuleBytes
from pycspr.types import ExecutionInfo_StoredContractByHash
from pycspr.types import ExecutionInfo_StoredContractByHashVersioned
from pycspr.types import ExecutionInfo_StoredContractByName
from pycspr.types import ExecutionInfo_StoredContractByNameVersioned
from pycspr.types import ExecutionInfo_Transfer



def _encode_module_bytes(instance: ExecutionInfo_ModuleBytes) -> bytearray:
    return cl.encode(CLTypeKey.BYTE_ARRAY, instance.module_bytes) + \
           cl.encode(CLTypeKey.LIST, instance.args, deploy_named_arg.encode)


def _encode_stored_contract_by_hash(instance: ExecutionInfo_StoredContractByHash) -> bytearray:
    return cl.encode(CLTypeKey.BYTE_ARRAY, instance.hash) + \
           cl.encode(CLTypeKey.STRING, instance.entry_point) + \
           cl.encode(CLTypeKey.LIST, instance.args, deploy_named_arg.encode)


def _encode_stored_contract_by_hash_versioned(instance: ExecutionInfo_StoredContractByHashVersioned) -> bytearray:
    return cl.encode(CLTypeKey.BYTE_ARRAY, instance.hash) + \
           cl.encode(CLTypeKey.OPTION, instance.version, CLTypeKey.U32) + \
           cl.encode(CLTypeKey.STRING, instance.entry_point) + \
           cl.encode(CLTypeKey.LIST, instance.args, deploy_named_arg.encode)


def _encode_stored_contract_by_name(instance: ExecutionInfo_StoredContractByName) -> bytearray:
    return cl.encode(CLTypeKey.STRING, instance.name) + \
           cl.encode(CLTypeKey.STRING, instance.entry_point) + \
           cl.encode(CLTypeKey.LIST, instance.args, deploy_named_arg.encode)


def _encode_stored_contract_by_name_versioned(instance: ExecutionInfo_StoredContractByNameVersioned) -> bytearray:
    return cl.encode(CLTypeKey.STRING, instance.name) + \
           cl.encode(CLTypeKey.OPTION, instance.version, CLTypeKey.U32) + \
           cl.encode(CLTypeKey.STRING, instance.entry_point) + \
           cl.encode(CLTypeKey.LIST, instance.args, deploy_named_arg.encode)


def _encode_transfer(instance: ExecutionInfo_Transfer) -> dict:
    return {
        "Transfer": {
            "args": [i for i in instance.args]
        }
    }


# Map: deploy executable type <-> type tag.
_TYPE_TAGS = {
    ExecutionInfo_ModuleBytes: 0,
    ExecutionInfo_StoredContractByHash: 1,
    ExecutionInfo_StoredContractByHashVersioned: 3,
    ExecutionInfo_StoredContractByName: 2,
    ExecutionInfo_StoredContractByNameVersioned: 4,
    ExecutionInfo_Transfer: 5,
}


# Map: deploy executable type <-> encoding function.
_ENCODERS = {
    ExecutionInfo_ModuleBytes: _encode_module_bytes,
    ExecutionInfo_StoredContractByHash: _encode_stored_contract_by_hash,
    ExecutionInfo_StoredContractByHashVersioned: _encode_stored_contract_by_hash_versioned,
    ExecutionInfo_StoredContractByName: _encode_stored_contract_by_name,
    ExecutionInfo_StoredContractByNameVersioned: _encode_stored_contract_by_name_versioned,
    ExecutionInfo_Transfer: _encode_transfer,
}


def to_json(instance: ExecutionInfo) -> bytearray:
    """Maps deploy executable to a bytearray for interpretation by a CSPR node.
    
    :param ExecutionInfo instance: Deploy executable information related to a value interpretable by a CSPR node.

    """
    obj = {}

    _ENCODERS[type(instance)](instance, obj)

    return obj
