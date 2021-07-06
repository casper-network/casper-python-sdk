def test_encode_transfer_payment(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.deploys.create_payment_for_transfer(
            vector["payment"]["amount"]
        )
        assert LIB.encode(entity, 'hex-string') == vector["payment"]["as_hex"]


def test_encode_transfer_session(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.deploys.create_session_for_transfer(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["transfer_id"]
            )
        assert LIB.encode(entity, 'hex-string') == vector["session"]["as_hex"]


def test_encode_transfer_body(FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.deploys.create_body(
            FACTORY.deploys.create_payment_for_transfer(
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
            FACTORY.deploys.create_payment_for_transfer(
                vector["payment"]["amount"]
            ),
            FACTORY.deploys.create_session_for_transfer(
                vector["session"]["amount"],
                vector["session"]["target"],
                vector["session"]["transfer_id"]
            )
        )

        print(entity.header)
        print(LIB.to_json(entity))

        assert entity.hash == vector["hash"]
