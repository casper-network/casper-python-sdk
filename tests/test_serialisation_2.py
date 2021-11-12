import pycspr


def test_serialisation_of_standard_payment_to_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert pycspr.to_bytes(entity) == vector["bytes"]["payment"]


def test_serialisation_of_standard_payment_to_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert entity == pycspr.from_json(type(entity), pycspr.to_json(entity))


def test_serialisation_of_transfer_session_to_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        assert pycspr.to_bytes(entity) == vector["bytes"]["session"]
        # assert entity == pycspr.from_bytes(pycspr.to_bytes(entity))


def test_serialisation_of_transfer_session_to_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        assert entity == pycspr.from_json(type(entity), pycspr.to_json(entity))
