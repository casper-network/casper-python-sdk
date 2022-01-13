import typing

import pytest

import pycspr
from pycspr import types
from pycspr.types.deploys import Deploy
from pycspr.types.deploys import DeployApproval
from pycspr.types.deploys import DeployArgument
from pycspr.types.deploys import DeployBody
from pycspr.types.deploys import DeployHeader
from pycspr.types.deploys import ModuleBytes
from pycspr.types.deploys import StoredContractByHash
from pycspr.types.deploys import StoredContractByHashVersioned
from pycspr.types.deploys import StoredContractByName
from pycspr.types.deploys import StoredContractByNameVersioned
from pycspr.types.deploys import Transfer
from tests.fixtures.deploys import create_deploy
from tests.fixtures.deploys import create_deploy_body
from tests.fixtures.deploys import create_deploy_header

_TEST_ACCOUNT_KEY = bytes.fromhex("011e0ee16a28b65e3cfa74d003eea4811b06173438e920fa38961ce60eb23548f4")
_TEST_BYTES = _TEST_ACCOUNT_KEY[1:]
_TEST_SIG = bytes.fromhex("01f43d8300bbd683b90bd2474d35da7cca664df5a505c47f4d35bf93531dc359bdf50b5e9493a2484306cc5eb41933b9fb118cf7954cf04d6c28441fcb1ee42f02")


@pytest.fixture(scope="session")
def yield_entities() -> typing.Iterator[object]:
    def _inner():
        for func in (
            create_deploy,
            _create_deploy_argument,
            _create_deploy_approval,
            create_deploy_body,
            create_deploy_header,
            _create_module_bytes,
            _create_stored_contract_by_hash,
            _create_stored_contract_by_hash_versioned,
            _create_stored_contract_by_name,
            _create_stored_contract_by_name_versioned,
            _create_transfer,
            ):
            yield func()

    return _inner


def _create_deploy_argument() -> DeployArgument:
    return DeployArgument("test-arg", types.CL_U64(1000000))


def _create_deploy_argument_set() -> typing.List[DeployArgument]:
    return [
        DeployArgument("test-arg-1", types.CL_U64(1000001)),
        DeployArgument("test-arg-2", types.CL_U64(1000002)),
        DeployArgument("test-arg-3", types.CL_U64(1000003)),
    ]


def _create_deploy_approval() -> DeployApproval:
    return DeployApproval(
        signer=pycspr.factory.create_public_key_from_account_key(_TEST_ACCOUNT_KEY),
        signature=_TEST_SIG
    )


def _create_module_bytes() -> ModuleBytes:
    return ModuleBytes(
        args=_create_deploy_argument_set(),
        module_bytes=_TEST_BYTES
    )


def _create_stored_contract_by_hash() -> StoredContractByHash:
    return StoredContractByHash(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        hash=_TEST_BYTES
    )


def _create_stored_contract_by_hash_versioned() -> StoredContractByHashVersioned:
    return StoredContractByHashVersioned(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        hash=_TEST_BYTES,
        version=123
    )


def _create_stored_contract_by_name() -> StoredContractByName:
    return StoredContractByName(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        name="hello-dolly"
    )


def _create_stored_contract_by_name_versioned() -> StoredContractByNameVersioned:
    return StoredContractByNameVersioned(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        name="hello-dolly",
        version=321
    )


def _create_transfer() -> Transfer:
    return pycspr.factory.create_transfer_session(
        amount=int(1e14),
        correlation_id=123456,
        target=_TEST_ACCOUNT_KEY,
    )


# _ENCODERS = {
#     Deploy: _encode_deploy,
#     DeployApproval: _encode_deploy_approval,
#     DeployArgument: _encode_deploy_argument,
#     DeployBody: _encode_deploy_body,
#     DeployHeader: _encode_deploy_header,
#     ModuleBytes: _encode_module_bytes,
#     StoredContractByHash: _encode_stored_contract_by_hash,
#     StoredContractByHashVersioned: _encode_stored_contract_by_hash_versioned,
#     StoredContractByName: _encode_stored_contract_by_name,
#     StoredContractByNameVersioned: _encode_stored_contract_by_name_versioned,
#     Transfer: _encode_transfer,
# }
