
import pycspr


def test_that_a_transfer_can_be_encoded_as_json(deploy_params_static, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_deploy(
            deploy_params_static,
            pycspr.factory.create_standard_payment(
                vector["payment"]["amount"]
            ),
            pycspr.factory.create_native_transfer_session(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["correlation_id"]
            )
        )
        as_json = pycspr.serialisation.to_json(entity)
        # TODO: assert against a known JSON file
        assert isinstance(as_json, str)
