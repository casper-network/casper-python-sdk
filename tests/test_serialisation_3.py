from pycspr import serialisation1
from pycspr.types import DeployBody


def test_that_deploy_entities_serialisation_to_and_from_bytes(deploy_entities_iterator):
    for entity in deploy_entities_iterator():
        encoded = serialisation1.to_bytes(entity)
        _, decoded = serialisation1.from_bytes(encoded, type(entity))
        assert entity == decoded


def test_that_deploy_entities_serialisation_to_and_from_json(deploy_entities_iterator):
    for entity in deploy_entities_iterator():
        if type(entity) in (DeployBody, ):
            continue
        encoded = serialisation1.to_json(entity)
        decoded = serialisation1.from_json(encoded, type(entity))
        assert entity == decoded
