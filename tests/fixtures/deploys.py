import datetime
import random

import pytest

import pycspr
from pycspr.types import Deploy
from pycspr.types import DeployApproval
from pycspr.types import DeployParameters
from pycspr.types.deploys import DeployBody, DeployHeader
from tests.fixtures.accounts import create_account


_A_KNOWN_ISO_TIMESTAMP = "2021-06-28T15:55:25.335+00:00"
_A_KNOWN_DEPLOY_TIMESTAMP = datetime.datetime.fromisoformat(_A_KNOWN_ISO_TIMESTAMP).timestamp()
_A_KNOWN_DEPLOY_HUMANIZED_TTL = "1day"


@pytest.fixture(scope="session")
def a_test_chain_id() -> str:
    return create_chain_id()


@pytest.fixture(scope="session")
def a_test_timestamp() -> int:
    return create_timestamp()


@pytest.fixture(scope="session")
def a_test_ttl_humanized() -> str:
    return create_ttl_humanized()


@pytest.fixture(scope="session")
def a_test_uref() -> str:
    return create_uref()


@pytest.fixture(scope="function")
def deploy_params(a_test_chain_id, a_test_ttl_humanized, cp1):
    return create_deploy_params(
        account=cp1,
        chain_id=a_test_chain_id,
        ttl_humanized=a_test_ttl_humanized
        )


@pytest.fixture(scope="function")
def deploy_params_static(a_test_chain_id, test_account_1):
    return pycspr.create_deploy_parameters(
            account=pycspr.factory.create_public_key(
                test_account_1.algo,
                test_account_1.pbk
            ),
            chain_name=a_test_chain_id,
            dependencies=[],
            gas_price=10,
            timestamp=_A_KNOWN_DEPLOY_TIMESTAMP,
            ttl=pycspr.create_deploy_ttl(_A_KNOWN_DEPLOY_HUMANIZED_TTL),
        )


@pytest.fixture(scope="function")
def a_deploy(deploy_params, cp1, cp2):
    deploy = pycspr.create_transfer(
        deploy_params,
        amount=2500000000,
        correlation_id=1,
        target=cp2.account_key,
        )
    deploy.set_approval(pycspr.create_deploy_approval(deploy, cp1))

    return deploy


def create_chain_id() -> str:
    return "casper-net-1"


def create_deploy() -> Deploy:
    return create_transfer()


def create_transfer() -> Deploy:
    cp1 = create_account()
    cp2 = create_account()
    params=create_deploy_params(account=cp1)

    deploy = pycspr.create_transfer(
        params=params,
        amount=2500000000,
        correlation_id=1,
        target=cp2.account_key,
        )
    deploy.set_approval(pycspr.create_deploy_approval(deploy, cp1))

    return deploy


def create_deploy_approval() -> DeployApproval:
    return create_deploy().approvals[0]


def create_deploy_body() -> DeployBody:
    return create_deploy().get_body()


def create_deploy_header() -> DeployHeader:
    return create_deploy().header


def create_deploy_params(account=None, chain_id=None, timestamp=None, ttl_humanized=None) -> DeployParameters:
    account = account or create_account()
    chain_id = chain_id or create_chain_id()
    timestamp = timestamp or create_timestamp()
    ttl_humanized = ttl_humanized or create_ttl_humanized()

    return pycspr.create_deploy_parameters(
            account=pycspr.factory.create_public_key(
                account.algo,
                account.pbk
            ),
            chain_name=chain_id or create_chain_id(),
            dependencies=[],
            gas_price=10,
            timestamp=timestamp or create_timestamp(),
            ttl=ttl_humanized
        )


def create_timestamp() -> str:
    return datetime.datetime.now(tz=datetime.timezone.utc).timestamp()


def create_ttl_humanized() -> str:
    (unit, quantity) = random.choice((
        ("ms", random.randint(1, 1000 * 60 * 60 * 24)),
        ("s", random.randint(1, 60)),
        ("m", random.randint(1, 60)),
        ("h", random.randint(1, 24)),
        ("day", 1)
        ))

    return f"{quantity}{unit}"


def create_uref() -> str:
    return "uref-827d5984270fed5aaaf076e1801733414a307ed8c5d85cad8ebe6265ba887b3a-007"
