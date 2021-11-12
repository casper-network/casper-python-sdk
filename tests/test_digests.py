import pycspr


def test_derivation_of_a_deploy_body_hash(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_deploy_body(
            pycspr.create_standard_payment(
                vector["payment"]["amount"]
                ),
            pycspr.factory.create_transfer_session(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["correlation_id"]
                )
        )
        assert entity.hash == vector["hashes"]["body"]


def test_derivation_of_a_deploy_hash(deploy_params_static, deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_deploy(
            deploy_params_static,
            pycspr.create_standard_payment(
                vector["payment"]["amount"]
                ),
            pycspr.factory.create_transfer_session(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["correlation_id"]
                )
        )
        assert entity.hash == vector["hashes"]["deploy"]
