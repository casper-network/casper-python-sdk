import random


def test_encode_transfer(LIB, FACTORY, TYPES, deploy_params, cp1, cp2):
    deploy=FACTORY.deploys.create_deploy(
        deploy_params,
        FACTORY.deploys.create_session_for_transfer(
            amount=1e9,
            target=cp2.account_hash,
            correlation_id=random.randint(0, 124)
            ),
        FACTORY.deploys.create_payment_for_transfer(
            1e6
            ),
        )
    as_json = LIB.encode_1(deploy, 'json')

    print(as_json)

    raise NotImplementedError()
