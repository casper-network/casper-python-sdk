
import pycspr


def test_that_a_transfer_can_be_encoded_as_json(deploy_params_static, deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.create_transfer(
            params=deploy_params_static,
            amount=vector["session"]["amount"],
            target=vector["session"]["target"],
            correlation_id=vector["session"]["correlation_id"]
        )
        # entity = pycspr.factory.create_deploy(
        #     deploy_params_static,
        #     pycspr.factory.create_standard_payment(
        #         vector["payment"]["amount"]
        #     ),
        #     pycspr.factory.create_transfer_session(
        #         vector["session"]["amount"],
        #         vector["session"]["target"],
        #         vector["session"]["correlation_id"]
        #     )
        # )
        assert isinstance(pycspr.to_json(entity), str)
