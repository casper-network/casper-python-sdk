from pycspr import serialization
from pycspr.domain.types import CLType, CLTypeInfo, PublicKey
from pycspr.domain.types import CLTypeInfo
from pycspr.types.cl import CLTypeInfo
from pycspr.domain.types import CLTypeInfo
from pycspr.domain.types import CLTypeInfo
from pycspr.domain.types import CLTypeInfo
from pycspr.domain.types import CLTypeInfo
from pycspr.domain.types import CLTypeInfo
from pycspr.domain.types import CLValue

from pycspr.domain.types import Deploy
from pycspr.domain.types import DeployApproval
from pycspr.domain.types import DeployExecutable_ModuleBytes
from pycspr.domain.types import DeployExecutable_StoredContractByHash
from pycspr.domain.types import DeployExecutable_StoredContractByHashVersioned
from pycspr.domain.types import DeployExecutable_StoredContractByName
from pycspr.domain.types import DeployExecutable_StoredContractByNameVersioned
from pycspr.domain.types import DeployExecutable_Transfer
from pycspr.domain.types import DeployHeader
from pycspr.domain.types import DeployNamedArg



def _encode_cl_value(instance: CLValue) ->  bytes:
    pass


def _encode_deploy(instance: Deploy) -> bytes:
    pass


def _encode_deploy_approval(instance: DeployApproval) -> bytes:
    pass


def _encode_deploy_executable_module_bytes(instance: DeployExecutable_ModuleBytes) -> bytes:
    pass


def _encode_deploy_executable_stored_contract_by_hash(instance: DeployExecutable_StoredContractByHash) -> bytes:
    pass


def _encode_deploy_executable_stored_contract_by_hash_versioned(instance: DeployExecutable_StoredContractByHashVersioned) -> bytes:
    pass


def _encode_deploy_executable_stored_contract_by_name(instance: DeployExecutable_StoredContractByName) -> bytes:
    pass


def _encode_deploy_executable_stored_contract_by_name_versioned(instance: DeployExecutable_StoredContractByNameVersioned) -> bytes:
    pass


def _encode_deploy_executable_transfer(instance: DeployExecutable_Transfer) -> bytes:
    pass


def _encode_deploy_header(instance: DeployHeader) -> bytes:
    pass


def _encode_deploy_named_arg(instance: DeployNamedArg) -> bytes:
    return \
        serialization.encode(CLType.STRING, instance.name) + \
        encode(instance.value)


_ENCODERS = {
    CLValue: _encode_cl_value,
    Deploy: _encode_deploy,
    DeployApproval: _encode_deploy_approval,
    DeployExecutable_ModuleBytes: _encode_deploy_executable_module_bytes,
    DeployExecutable_StoredContractByHash: _encode_deploy_executable_stored_contract_by_hash,
    DeployExecutable_StoredContractByHashVersioned: _encode_deploy_executable_stored_contract_by_hash_versioned,
    DeployExecutable_StoredContractByName: _encode_deploy_executable_stored_contract_by_name,
    DeployExecutable_StoredContractByNameVersioned: _encode_deploy_executable_stored_contract_by_name_versioned,
    DeployExecutable_Transfer: _encode_deploy_executable_transfer,
    DeployHeader: _encode_deploy_header,
    DeployNamedArg: _encode_deploy_named_arg,
}

def to_bytes(instance: Deploy) -> bytes:
    pass

