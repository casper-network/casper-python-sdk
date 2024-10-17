import typing

import pytest

import pycspr
from pycspr.type_defs.cl_values import CLV_U64
from pycspr.type_defs.crypto import PublicKey
from pycspr.type_defs.crypto import Signature
from pycspr.types.node import DeployApproval
from pycspr.types.node import DeployArgument
from pycspr.types.node import DeployOfModuleBytes
from pycspr.types.node import DeployOfStoredContractByHash
from pycspr.types.node import DeployOfStoredContractByHashVersioned
from pycspr.types.node import DeployOfStoredContractByName
from pycspr.types.node import DeployOfStoredContractByNameVersioned
from pycspr.types.node import DeployOfTransfer
from tests.fixtures.deploys import create_deploy
from tests.fixtures.deploys import create_deploy_body
from tests.fixtures.deploys import create_deploy_header


@pytest.fixture(scope="session")
def yield_entities(
    test_account_key: bytes,
    test_bytes: bytes,
    test_signature: bytes
) -> typing.Iterator[object]:
    def _inner():
        yield create_deploy()
        yield _create_deploy_argument()
        yield _create_deploy_approval(test_account_key, test_signature)
        yield create_deploy_body()
        yield create_deploy_header()
        yield _create_module_bytes(test_bytes)
        yield _create_stored_contract_by_hash(test_bytes)
        yield _create_stored_contract_by_hash_versioned(test_bytes)
        yield _create_stored_contract_by_name()
        yield _create_stored_contract_by_name_versioned()
        yield _create_transfer(test_account_key)

    return _inner


def _create_deploy_argument() -> DeployArgument:
    return DeployArgument("test-arg", CLV_U64(1000000))


def _create_deploy_argument_set() -> typing.List[DeployArgument]:
    return [
        DeployArgument("test-arg-1", CLV_U64(1000001)),
        DeployArgument("test-arg-2", CLV_U64(1000002)),
        DeployArgument("test-arg-3", CLV_U64(1000003)),
    ]


def _create_deploy_approval(account_key: bytes, signature: bytes) -> DeployApproval:
    return DeployApproval(
        signer=PublicKey.from_bytes(account_key),
        signature=Signature.from_bytes(signature)
    )


def _create_module_bytes(some_bytes: bytes) -> DeployOfModuleBytes:
    return DeployOfModuleBytes(
        args=_create_deploy_argument_set(),
        module_bytes=some_bytes
    )


def _create_stored_contract_by_hash(some_bytes: bytes) -> DeployOfStoredContractByHash:
    return DeployOfStoredContractByHash(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        hash=some_bytes
    )


def _create_stored_contract_by_hash_versioned(
    some_bytes: bytes
) -> DeployOfStoredContractByHashVersioned:
    return DeployOfStoredContractByHashVersioned(
        args=_create_deploy_argument_set(),
        entry_point="an-entry-point",
        hash=some_bytes,
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


def _create_transfer(account_key: bytes) -> DeployOfTransfer:
    return pycspr.factory.create_transfer_session(
        amount=int(1e14),
        correlation_id=123456,
        target=PublicKey.from_bytes(account_key),
    )
