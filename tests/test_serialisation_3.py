import pycspr
from pycspr import serialisation


def test_serialisation_of_transfer_to_json(deploy_params_static, deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_transfer(
            params=deploy_params_static,
            amount=vector["session"]["amount"],
            target=vector["session"]["target"],
            correlation_id=vector["session"]["correlation_id"]
        )
        as_dict: dict = serialisation.deploy_to_json(entity)
        assert isinstance(as_dict, dict)
        print(as_dict)
        assert entity == serialisation.deploy_from_json(type(entity), as_dict)
