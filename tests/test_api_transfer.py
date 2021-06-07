import random



def test_exec_transfer(LIB, a_test_chain_id, cp1, cp2):
    # Raw parameters.
    correlation_id = random.randint(0, 124)
    payment_amount = 1000
    target_address = cp2.address
    transfer_amount = 2500000000

    # Construct deploy 
    payment = LIB.factory.create_payment_for_transfer(
        payment_amount
        )
    session = LIB.factory.create_session_for_transfer(
        amount=transfer_amount,
        target=target_address,
        correlation_id=correlation_id
        )
    header=LIB.factory.create_deploy_header(
        account_key=cp1.account_key,
        body_hash="todo-derive-body-hash",
        chain_name=a_test_chain_id
    )
    approvals = [
        LIB.factory.create_deploy_approval(cp1, b'todo-get-deploy-data-for-signature')
    ]

    deploy=LIB.factory.create_deploy(
        approvals,
        payment,
        session,
        header
    )

    print(deploy)
    

    raise NotImplementedError()
