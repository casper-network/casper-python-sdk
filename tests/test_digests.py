import pycspr
from pycspr.type_defs.crypto import PublicKey


def test_derivation_of_a_deploy_body_hash(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_deploy_body(
            pycspr.factory.create_standard_payment(
                vector["payment"]["amount"]
                ),
            pycspr.factory.create_transfer_session(
                vector["session"]["amount"],
                PublicKey.from_bytes(vector["session"]["target"]),
                vector["session"]["correlation_id"]
                )
        )
        assert entity.hash == vector["hashes"]["body"]


def test_derivation_of_a_deploy_hash(deploy_params_static, deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_deploy(
            deploy_params_static,
            pycspr.factory.create_standard_payment(
                vector["payment"]["amount"]
                ),
            pycspr.factory.create_transfer_session(
                vector["session"]["amount"],
                PublicKey.from_bytes(vector["session"]["target"]),
                vector["session"]["correlation_id"]
                )
        )

        assert entity.hash == vector["hashes"]["deploy"]
