import pycspr
from pycspr import serializer
from pycspr.type_defs.crypto import PublicKey


def test_that_node_standard_payment_serialises_to_and_from_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        encoded = serializer.to_bytes(entity)
        assert encoded == vector["bytes"]["payment"]
        _, decoded = serializer.from_bytes(type(entity), encoded)
        assert entity == decoded


def test_that_node_standard_payment_serialises_to_and_from_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_standard_payment(
            vector["payment"]["amount"]
        )
        encoded = serializer.to_json(entity)
        decoded = serializer.from_json(type(entity), encoded)
        assert entity == decoded


def test_that_node_standard_transfer_session_serialises_to_and_from_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        amount: int = vector["session"]["amount"]
        correlation_id: int = vector["session"]["correlation_id"]
        target: PublicKey = PublicKey.from_bytes(vector["session"]["target"])
        entity = pycspr.factory.create_transfer_session(amount, target, correlation_id)

        encoded = serializer.to_bytes(entity)
        assert encoded == vector["bytes"]["session"]

        _, decoded = serializer.from_bytes(type(entity), encoded)
        assert entity == decoded


def test_that_node_standard_transfer_session_serialises_to_and_from_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        amount: int = vector["session"]["amount"]
        correlation_id: int = vector["session"]["correlation_id"]
        target: PublicKey = PublicKey.from_bytes(vector["session"]["target"])
        entity = pycspr.factory.create_transfer_session(amount, target, correlation_id)

        encoded = serializer.to_json(entity)
        decoded = serializer.from_json(type(entity), encoded)
        assert entity == decoded
