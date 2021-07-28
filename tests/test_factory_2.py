import datetime
import operator
import random

import pycspr



def test_create_deploy_parameters(TYPES, a_test_account, a_test_chain_id):
    assert isinstance(
        pycspr.factory.create_deploy_parameters(
            account=pycspr.factory.create_public_key(
                a_test_account.algo,
                a_test_account.pbk
            ),
            chain_name=a_test_chain_id,
            dependencies=[],
            gas_price=random.randint(0, 65),
            timestamp=datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            ttl="1day",
        ),
        TYPES.DeployParameters
        )


def test_create_standard_payment(TYPES):
    assert isinstance(
        pycspr.factory.create_standard_payment(
            amount = random.randint(0, 1e5),
        ),
        TYPES.ExecutableDeployItem_ModuleBytes
        )


    def test_create_native_transfer_session(TYPES):
        assert isinstance(
            pycspr.factory.create_native_transfer_session(
                amount = random.randint(0, 1e9),
                correlation_id = random.randint(0, 1e9),
                target = bytes([]),
                ),
            TYPES.ExecutableDeployItem_Transfer
            )


def test_create_native_transfer_body(TYPES, deploy_params):
    payment = pycspr.factory.create_standard_payment(
        amount = random.randint(0, 1e5),
        )
    session = pycspr.factory.create_native_transfer_session(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    body = pycspr.factory.create_deploy_body(payment, session)
    assert isinstance(body, TYPES.DeployBody)
    assert isinstance(body.hash, bytes)
    assert len(body.hash) == 32


def test_create_native_transfer_header(TYPES, deploy_params):
    payment = pycspr.factory.create_standard_payment(
        amount = random.randint(0, 1e5),
        )
    session = pycspr.factory.create_native_transfer_session(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    body = pycspr.factory.create_deploy_body(payment, session)
    header = pycspr.factory.create_deploy_header(body, deploy_params)
    assert isinstance(header, TYPES.DeployHeader)
    assert isinstance(header.body_hash, bytes)
    assert len(header.body_hash) == 32


def test_create_native_transfer_deploy(TYPES, deploy_params, cp2):
    session = pycspr.factory.create_native_transfer_session(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = cp2.account_hash,
        )
    payment = pycspr.factory.create_standard_payment(
        amount = random.randint(0, 1e5),
        )
    deploy = pycspr.factory.create_deploy(deploy_params, payment, session)
    assert isinstance(deploy, TYPES.Deploy)
    assert isinstance(deploy.hash, bytes)
    assert len(deploy.hash) == 32
