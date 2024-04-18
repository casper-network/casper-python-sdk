from pycspr import serializer
from pycspr.types.node import DeployBody


def test_that_node_entities_serialisation_to_and_from_bytes(deploy_entities_iterator):
    for entity in deploy_entities_iterator():
        print(type(entity))

        encoded = serializer.to_bytes(entity)
        _, decoded = serializer.from_bytes(type(entity), encoded)
        assert entity == decoded


def test_that_node_entities_serialisation_to_and_from_json(deploy_entities_iterator):
    for entity in deploy_entities_iterator():
        if type(entity) not in (DeployBody, ):
            encoded = serializer.to_json(entity)
            decoded = serializer.from_json(type(entity), encoded)
            assert entity == decoded
