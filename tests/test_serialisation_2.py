import pycspr
from pycspr import serialisation


def test_serialisation_of_standard_payment_to_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        as_bytes: bytes = serialisation.deploy_to_bytes(entity)
        assert as_bytes.hex() == vector["bytes"]["payment"].hex()
        # assert entity == serialisation.deploy_from_bytes(type(entity), as_bytes)


def test_serialisation_of_standard_payment_to_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        as_dict: dict = serialisation.deploy_to_json(entity)
        assert entity == serialisation.deploy_from_json(type(entity), as_dict)


def test_serialisation_of_transfer_session_to_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        as_bytes: bytes = serialisation.deploy_to_bytes(entity)
        assert as_bytes == vector["bytes"]["session"]
        # assert entity == serialisation.deploy_from_bytes(type(entity), as_bytes)


def test_serialisation_of_transfer_session_to_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        as_dict: dict = serialisation.deploy_to_json(entity)
        assert entity == serialisation.deploy_from_json(type(entity), as_dict)
