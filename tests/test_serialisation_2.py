import random
import pycspr

def test_that_standard_payment_serialises_to_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert pycspr.to_bytes(entity) == vector["bytes"]["payment"]


def test_that_standard_payment_serialises_to_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert entity == pycspr.from_json(type(entity), pycspr.to_json(entity))


def test_that_a_transfer_session_serialises_to_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        assert pycspr.to_bytes(entity) == vector["bytes"]["session"]
        # assert entity == pycspr.from_bytes(pycspr.to_bytes(entity))


def test_that_a_transfer_session_serialises_to_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        assert entity == pycspr.from_json(type(entity), pycspr.to_json(entity))


def test_that_a_deploy_body_can_be_encoded_as_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_deploy_body(
            pycspr.create_standard_payment(
                vector["payment"]["amount"]
                ),
            pycspr.create_transfer_session(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["correlation_id"]
                )
        )
        assert entity.hash == vector["hashes"]["body"]


def test_that_a_deploy_can_be_encoded_as_bytes(deploy_params_static, deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_deploy(
            deploy_params_static,
            pycspr.factory.create_standard_payment(
                vector["payment"]["amount"]
            ),
            pycspr.factory.create_transfer_session(
                amount=vector["session"]["amount"],
                correlation_id=["session"]["correlation_id"],
                target=vector["session"]["target"]
            )
        )
        assert entity.hash == vector["hashes"]["deploy"]
