import pycspr
from pycspr import serializer


def test_that_node_standard_transfer_serialises_to_and_from_json(
    deploy_params_static,
    deploys_1
):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_transfer(
            params=deploy_params_static,
            amount=vector["session"]["amount"],
            target=vector["session"]["target"],
            correlation_id=vector["session"]["correlation_id"]
        )
        encoded = serializer.to_json(entity)
        decoded = serializer.from_json(encoded, type(entity))
        assert entity == decoded
