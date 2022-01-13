import random

import pytest

import pycspr
from pycspr import serialisation
from pycspr.types import DeployApproval
from pycspr.types import DeployArgument
from pycspr.types import DeployParameters


def test_create_deploy_arguments_1(cl_values_vector):
    for cl_value in cl_values_vector:
        arg = DeployArgument("an-argument", cl_value)
        assert isinstance(arg, DeployArgument)


def test_create_deploy_arguments_2(cl_values_vector):
    for cl_value in cl_values_vector:
        arg = DeployArgument("an-argument", cl_value)
        arg_json = serialisation.deploy_to_json(arg)
        assert arg == serialisation.deploy_from_json(DeployArgument, arg_json)


def test_create_deploy_arguments_3(cl_values_vector):
    for cl_value in cl_values_vector:
        entity = DeployArgument("an-argument", cl_value)
        encoded = serialisation.deploy_to_bytes(entity)
        _, decoded = serialisation.deploy_from_bytes(encoded, DeployArgument)
        assert entity == decoded


def test_create_deploy_approval_1(a_deploy, a_test_account):
    approval = pycspr.create_deploy_approval(a_deploy, a_test_account)

    assert isinstance(approval, DeployApproval)


def test_create_deploy_approval_2(a_deploy, a_test_account):
    approvals = len(a_deploy.approvals)
    a_deploy.approve(a_test_account)
    assert len(a_deploy.approvals) == approvals + 1
    a_deploy.approve(a_test_account)
    assert len(a_deploy.approvals) == approvals + 1


def test_create_deploy_parameters(a_test_account, a_test_chain_id, a_test_timestamp):
    assert isinstance(
        pycspr.create_deploy_parameters(
            account=pycspr.factory.create_public_key(
                a_test_account.algo,
                a_test_account.pbk
            ),
            chain_name=a_test_chain_id,
            dependencies=[],
            gas_price=random.randint(0, 65),
            timestamp=a_test_timestamp,
            ttl="1day",
        ),
        DeployParameters
        )


def test_create_standard_payment():
    assert isinstance(
        pycspr.create_standard_payment(
            amount=random.randint(0, 1e5),
        ),
        pycspr.types.ModuleBytes
        )


def test_create_transfer_session(a_test_account):
    assert isinstance(
        pycspr.factory.create_transfer_session(
            amount=random.randint(0, 1e9),
            correlation_id=random.randint(0, 1e9),
            target=a_test_account.account_key,
            ),
        pycspr.types.Transfer
        )


def test_create_transfer_body(a_test_account):
    body = pycspr.factory.create_deploy_body(
        pycspr.factory.create_standard_payment(
            amount=random.randint(0, 1e5),
        ),
        pycspr.factory.create_transfer_session(
            amount=random.randint(0, 1e9),
            correlation_id=random.randint(0, 1e9),
            target=a_test_account.account_key,
        )
    )
    assert isinstance(body, pycspr.types.DeployBody)
    assert isinstance(body.hash, bytes)
    assert len(body.hash) == 32


def test_create_transfer_header(deploy_params, a_test_account):
    body = pycspr.factory.create_deploy_body(
        pycspr.create_standard_payment(
            amount=random.randint(0, 1e5),
        ),
        pycspr.factory.create_transfer_session(
            amount=random.randint(0, 1e9),
            correlation_id=random.randint(0, 1e9),
            target=a_test_account.account_key,
        )
    )
    header = pycspr.factory.create_deploy_header(
        body,
        deploy_params
        )
    assert isinstance(header, pycspr.types.DeployHeader)
    assert isinstance(header.body_hash, bytes)
    assert len(header.body_hash) == 32


def test_create_transfer(deploy_params, a_test_account):
    deploy = pycspr.create_transfer(
        params=deploy_params,
        amount=random.randint(0, 1e5),
        target=a_test_account.account_key,
        correlation_id=random.randint(0, 1e9)
    )
    assert isinstance(deploy, pycspr.types.Deploy)
    assert isinstance(deploy.hash, bytes) and len(deploy.hash) == 32
