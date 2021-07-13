def test_that_a_standard_payment_can_be_encoded_as_bytes(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert LIB.to_bytes(entity) == vector["bytes"]["payment"]


def test_that_a_standard_transfer_session_can_be_encoded_as_bytes(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.create_standard_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["transfer_id"]
            )
        assert LIB.to_bytes(entity) == vector["bytes"]["session"]


def test_that_a_deploy_body_can_be_encoded_as_bytes(FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.create_deploy_body(
            FACTORY.create_standard_payment(
                vector["payment"]["amount"]
                ),
            FACTORY.create_standard_transfer_session(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["transfer_id"]
                )
        )
        assert entity.hash == vector["hashes"]["body"]


def test_that_a_deploy_can_be_encoded_as_bytes(LIB, FACTORY, deploy_params_static, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.create_deploy(
            deploy_params_static,
            FACTORY.create_standard_payment(
                vector["payment"]["amount"]
            ),
            FACTORY.create_standard_transfer_session(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["transfer_id"]
            )
        )
        assert entity.hash == vector["hashes"]["deploy"]
