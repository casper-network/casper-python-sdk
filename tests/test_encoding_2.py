
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
        print(LIB.to_json(entity))

        assert entity.hash == True
