def test_encode_transfer_payment(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.deploys.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert LIB.to_hex(entity) == vector["payment"]["as_hex"]


def test_encode_transfer_session(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.deploys.create_session_for_transfer(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["transfer_id"]
            )
        assert LIB.to_hex(entity) == vector["session"]["as_hex"]


def test_encode_transfer_body(FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.deploys.create_deploy_body(
            FACTORY.deploys.create_standard_payment(
                vector["payment"]["amount"]
            ),
            FACTORY.deploys.create_session_for_transfer(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["transfer_id"]
            )
        )
        assert entity.hash == vector["hash_of_body"]


def test_encode_transfer(LIB, FACTORY, deploy_params_static, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.deploys.create_deploy(
            deploy_params_static,
            FACTORY.deploys.create_standard_payment(
                vector["payment"]["amount"]
            ),
            FACTORY.deploys.create_session_for_transfer(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["transfer_id"]
            )
        )
        assert entity.hash == vector["hash"]
