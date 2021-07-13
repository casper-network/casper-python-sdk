def test_encode_transfer_payment(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert LIB.to_hex(entity) == vector["hashes"]["payment"]


def test_encode_transfer_session(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.create_standard_transfer_session(
            vector["session"]["amount"],
            bytes.fromhex(vector["session"]["target"]),
            vector["session"]["transfer_id"]
            )
        assert LIB.to_hex(entity) == vector["hashes"]["session"]


def test_encode_transfer_body(FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.create_deploy_body(
            FACTORY.create_standard_payment(
                vector["payment"]["amount"]
                ),
            FACTORY.create_standard_transfer_session(
                vector["session"]["amount"],
                bytes.fromhex(vector["session"]["target"]),
                vector["session"]["transfer_id"]
                )
        )
        assert entity.hash == bytes.fromhex(vector["hashes"]["body"])


def test_encode_transfer(LIB, FACTORY, deploy_params_static, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.create_deploy(
            deploy_params_static,
            FACTORY.create_standard_payment(
                vector["payment"]["amount"]
            ),
            FACTORY.create_standard_transfer_session(
                vector["session"]["amount"],
                bytes.fromhex(vector["session"]["target"]),
                vector["session"]["transfer_id"]
            )
        )
        assert entity.hash == bytes.fromhex(vector["hashes"]["deploy"])
