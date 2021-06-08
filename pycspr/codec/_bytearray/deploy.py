from pycspr import serialization
from pycspr.domain.types import CLTypeKey, CLType, PublicKey
from pycspr.domain.types import CLType
from pycspr.types.cl import CLType
from pycspr.domain.types import CLType
from pycspr.domain.types import CLType
from pycspr.domain.types import CLType
from pycspr.domain.types import CLType
from pycspr.domain.types import CLType
from pycspr.domain.types import CLValue

from pycspr.domain.types import Deploy
from pycspr.domain.types import Approval
from pycspr.domain.types import ExecutionInfo_ModuleBytes
from pycspr.domain.types import ExecutionInfo_StoredContractByHash
from pycspr.domain.types import ExecutionInfo_StoredContractByHashVersioned
from pycspr.domain.types import ExecutionInfo_StoredContractByName
from pycspr.domain.types import ExecutionInfo_StoredContractByNameVersioned
from pycspr.domain.types import ExecutionInfo_Transfer
from pycspr.domain.types import DeployHeader
from pycspr.domain.types import ExecutionArgument



def _encode_cl_value(instance: CLValue) ->  bytes:
    pass


def _encode_deploy(instance: Deploy) -> bytes:
    pass


def _encode_deploy_approval(instance: Approval) -> bytes:
    pass


def _encode_deploy_executable_module_bytes(instance: ExecutionInfo_ModuleBytes) -> bytes:
    pass


def _encode_deploy_executable_stored_contract_by_hash(instance: ExecutionInfo_StoredContractByHash) -> bytes:
    pass


def _encode_deploy_executable_stored_contract_by_hash_versioned(instance: ExecutionInfo_StoredContractByHashVersioned) -> bytes:
    pass


def _encode_deploy_executable_stored_contract_by_name(instance: ExecutionInfo_StoredContractByName) -> bytes:
    pass


def _encode_deploy_executable_stored_contract_by_name_versioned(instance: ExecutionInfo_StoredContractByNameVersioned) -> bytes:
    pass


def _encode_deploy_executable_transfer(instance: ExecutionInfo_Transfer) -> bytes:
    pass


def _encode_deploy_header(instance: DeployHeader) -> bytes:
    pass


def _encode_deploy_named_arg(instance: ExecutionArgument) -> bytes:
    return \
        serialization.encode(CLTypeKey.STRING, instance.name) + \
        encode(instance.value)


_ENCODERS = {
    CLValue: _encode_cl_value,
    Deploy: _encode_deploy,
    Approval: _encode_deploy_approval,
    ExecutionInfo_ModuleBytes: _encode_deploy_executable_module_bytes,
    ExecutionInfo_StoredContractByHash: _encode_deploy_executable_stored_contract_by_hash,
    ExecutionInfo_StoredContractByHashVersioned: _encode_deploy_executable_stored_contract_by_hash_versioned,
    ExecutionInfo_StoredContractByName: _encode_deploy_executable_stored_contract_by_name,
    ExecutionInfo_StoredContractByNameVersioned: _encode_deploy_executable_stored_contract_by_name_versioned,
    ExecutionInfo_Transfer: _encode_deploy_executable_transfer,
    DeployHeader: _encode_deploy_header,
    ExecutionArgument: _encode_deploy_named_arg,
}

def to_bytes(instance: Deploy) -> bytes:
    pass

