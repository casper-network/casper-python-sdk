import random



def test_exec_transfer(FACTORY, TYPES, deploy_params, cp1, cp2):
    
    # Raw parameters.
    amount = 2500000000
    correlation_id = random.randint(0, 124)
    target = cp2.account_hash
    payment_amount = 1000000

    deploy=FACTORY.deploys.create_deploy(
        deploy_params,
        FACTORY.deploys.create_payment_for_transfer(
            payment_amount
            ),
        FACTORY.deploys.create_session_for_transfer(
            amount=amount,
            target=target,
            correlation_id=correlation_id
            )
        )
    assert isinstance(deploy, TYPES.Deploy)
