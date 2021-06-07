
from pycspr.codec._bytearray import cl
from pycspr.codec._bytearray import deploy_named_arg
from pycspr.types import CLType
from pycspr.types import DeployExecutable
from pycspr.types import DeployExecutable_ModuleBytes
from pycspr.types import DeployExecutable_StoredContractByHash
from pycspr.types import DeployExecutable_StoredContractByHashVersioned
from pycspr.types import DeployExecutable_StoredContractByName
from pycspr.types import DeployExecutable_StoredContractByNameVersioned
from pycspr.types import DeployExecutable_Transfer



def _encode_module_bytes(instance: DeployExecutable_ModuleBytes) -> bytearray:
    return cl.encode(CLType.BYTE_ARRAY, instance.module_bytes) + \
           cl.encode(CLType.LIST, instance.args, deploy_named_arg.encode)


def _encode_stored_contract_by_hash(instance: DeployExecutable_StoredContractByHash) -> bytearray:
    return cl.encode(CLType.BYTE_ARRAY, instance.hash) + \
           cl.encode(CLType.STRING, instance.entry_point) + \
           cl.encode(CLType.LIST, instance.args, deploy_named_arg.encode)


def _encode_stored_contract_by_hash_versioned(instance: DeployExecutable_StoredContractByHashVersioned) -> bytearray:
    return cl.encode(CLType.BYTE_ARRAY, instance.hash) + \
           cl.encode(CLType.OPTION, instance.version, CLType.U32) + \
           cl.encode(CLType.STRING, instance.entry_point) + \
           cl.encode(CLType.LIST, instance.args, deploy_named_arg.encode)


def _encode_stored_contract_by_name(instance: DeployExecutable_StoredContractByName) -> bytearray:
    return cl.encode(CLType.STRING, instance.name) + \
           cl.encode(CLType.STRING, instance.entry_point) + \
           cl.encode(CLType.LIST, instance.args, deploy_named_arg.encode)


def _encode_stored_contract_by_name_versioned(instance: DeployExecutable_StoredContractByNameVersioned) -> bytearray:
    return cl.encode(CLType.STRING, instance.name) + \
           cl.encode(CLType.OPTION, instance.version, CLType.U32) + \
           cl.encode(CLType.STRING, instance.entry_point) + \
           cl.encode(CLType.LIST, instance.args, deploy_named_arg.encode)


def _encode_transfer(instance: DeployExecutable_Transfer) -> dict:
    return {
        "Transfer": {
            "args": [i for i in instance.args]
        }
    }


# Map: deploy executable type <-> type tag.
_TYPE_TAGS = {
    DeployExecutable_ModuleBytes: 0,
    DeployExecutable_StoredContractByHash: 1,
    DeployExecutable_StoredContractByHashVersioned: 3,
    DeployExecutable_StoredContractByName: 2,
    DeployExecutable_StoredContractByNameVersioned: 4,
    DeployExecutable_Transfer: 5,
}


# Map: deploy executable type <-> encoding function.
_ENCODERS = {
    DeployExecutable_ModuleBytes: _encode_module_bytes,
    DeployExecutable_StoredContractByHash: _encode_stored_contract_by_hash,
    DeployExecutable_StoredContractByHashVersioned: _encode_stored_contract_by_hash_versioned,
    DeployExecutable_StoredContractByName: _encode_stored_contract_by_name,
    DeployExecutable_StoredContractByNameVersioned: _encode_stored_contract_by_name_versioned,
    DeployExecutable_Transfer: _encode_transfer,
}


def to_json(instance: DeployExecutable) -> bytearray:
    """Maps deploy executable to a bytearray for interpretation by a CSPR node.
    
    :param DeployExecutable instance: Deploy executable information related to a value interpretable by a CSPR node.

    """
    obj = {}

    _ENCODERS[type(instance)](instance, obj)

    return obj
