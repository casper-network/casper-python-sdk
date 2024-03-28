import typing

import pytest

import pycspr
from pycspr import types
from pycspr.types.node.rpc import DeployApproval
from pycspr.types.node.rpc import DeployArgument
from pycspr.types.node.rpc import DeployOfModuleBytes
from pycspr.types.node.rpc import DeployOfStoredContractByHash
from pycspr.types.node.rpc import DeployOfStoredContractByHashVersioned
from pycspr.types.node.rpc import DeployOfStoredContractByName
from pycspr.types.node.rpc import DeployOfStoredContractByNameVersioned
from pycspr.types.node.rpc import DeployOfTransfer
from tests.fixtures.deploys import create_deploy
from tests.fixtures.deploys import create_deploy_body
from tests.fixtures.deploys import create_deploy_header


_TEST_ACCOUNT_KEY = \
    bytes.fromhex("011e0ee16a28b65e3cfa74d003eea4811b06173438e920fa38961ce60eb23548f4")
_TEST_BYTES = _TEST_ACCOUNT_KEY[1:]
_TEST_SIG = \
    bytes.fromhex("01f43d8300bbd683b90bd2474d35da7cca664df5a505c47f4d35bf93531dc359bdf50b5e9493a2484306cc5eb41933b9fb118cf7954cf04d6c28441fcb1ee42f02")


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
    return DeployArgument("test-arg", types.cl.CLV_U64(1000000))


def _create_deploy_argument_set() -> typing.List[DeployArgument]:
    return [
        DeployArgument("test-arg-1", types.cl.CLV_U64(1000001)),
        DeployArgument("test-arg-2", types.cl.CLV_U64(1000002)),
        DeployArgument("test-arg-3", types.cl.CLV_U64(1000003)),
    ]


def _create_deploy_approval() -> DeployApproval:
    return DeployApproval(
        signer=pycspr.factory.create_public_key_from_account_key(_TEST_ACCOUNT_KEY),
        signature=_TEST_SIG
    )


def _create_module_bytes() -> DeployOfModuleBytes:
    return DeployOfModuleBytes(
        args=_create_deploy_argument_set(),
        module_bytes=_TEST_BYTES
    )


def _create_stored_contract_by_hash() -> DeployOfStoredContractByHash:
    return DeployOfStoredContractByHash(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        hash=_TEST_BYTES
    )


def _create_stored_contract_by_hash_versioned() -> DeployOfStoredContractByHashVersioned:
    return DeployOfStoredContractByHashVersioned(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        hash=_TEST_BYTES,
        version=123
    )


def _create_stored_contract_by_name() -> DeployOfStoredContractByName:
    return DeployOfStoredContractByName(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        name="hello-dolly"
    )


def _create_stored_contract_by_name_versioned() -> DeployOfStoredContractByNameVersioned:
    return DeployOfStoredContractByNameVersioned(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        name="hello-dolly",
        version=321
    )


def _create_transfer() -> DeployOfTransfer:
    return pycspr.factory.create_transfer_session(
        amount=int(1e14),
        correlation_id=123456,
        target=_TEST_ACCOUNT_KEY,
    )
