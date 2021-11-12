import pycspr


def test_serialisation_of_transfer_to_json(deploy_params_static, deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_transfer(
            params=deploy_params_static,
            amount=vector["session"]["amount"],
            target=vector["session"]["target"],
            correlation_id=vector["session"]["correlation_id"]
        )
        assert isinstance(pycspr.to_json(entity), str)
