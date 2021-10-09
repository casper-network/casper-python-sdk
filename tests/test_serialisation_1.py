import pycspr



def test_that_a_standard_payment_can_be_encoded_as_bytes(vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert pycspr.serialisation.to_bytes(entity) == vector["bytes"]["payment"]


def test_that_a_standard_transfer_session_can_be_encoded_as_bytes(vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_native_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        print(vector["bytes"]["session"].hex())
        print(pycspr.serialisation.to_bytes(entity).hex())
        assert pycspr.serialisation.to_bytes(entity) == vector["bytes"]["session"]


def test_that_a_deploy_body_can_be_encoded_as_bytes(vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_deploy_body(
            pycspr.factory.create_standard_payment(
                vector["payment"]["amount"]
                ),
            pycspr.factory.create_native_transfer_session(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["correlation_id"]
                )
        )
        print(entity.hash.hex())
        assert entity.hash == vector["hashes"]["body"]


def test_that_a_deploy_can_be_encoded_as_bytes(deploy_params_static, vector_deploy_1):
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
        assert entity.hash == vector["hashes"]["deploy"]
