import datetime
import operator
import random



def test_create_approval(FACTORY, TYPES, vector_cl_data_1, vector_crypto_2):
    _bytes = vector_cl_data_1.get_value_as_bytes(TYPES.CLTypeKey.BYTE_ARRAY)
    for algo, pbk, pvk in [operator.itemgetter("algo", "pbk", "pvk")(i) for i in vector_crypto_2]:
        account_info = FACTORY.accounts.create_account_info(algo, pvk, pbk)
        approval = FACTORY.deploys.create_approval(account_info, _bytes)
        assert isinstance(approval, TYPES.Approval)


def test_create_standard_parameters(FACTORY, TYPES, a_test_account, a_test_chain_id):
    assert isinstance(
        FACTORY.deploys.create_standard_parameters(
            account=FACTORY.accounts.create_public_key(
                a_test_account.algo,
                a_test_account.pbk
            ),
            account=a_test_account,
            chain_name=a_test_chain_id,
            dependencies=[],
            gas_price=random.randint(0, 65),
            timestamp=datetime.datetime.utcnow(),
            ttl="1day",
        ),
        TYPES.DeployStandardParameters
        )


def test_create_transfer_session(FACTORY, TYPES):
    assert isinstance(
        FACTORY.deploys.create_session_for_transfer(
            amount = random.randint(0, 1e9),
            correlation_id = random.randint(0, 1e9),
            target = bytes([]),
            ),
        TYPES.ExecutionInfo_Transfer
        )


def test_create_transfer_payment(FACTORY, TYPES):
    assert isinstance(
        FACTORY.deploys.create_payment_for_transfer(
            amount = random.randint(0, 1e5),
        ),
        TYPES.ExecutionInfo_ModuleBytes
        )


def test_create_transfer_body(FACTORY, TYPES, deploy_params):
    payment = FACTORY.deploys.create_payment_for_transfer(
        amount = random.randint(0, 1e5),
        )
    session = FACTORY.deploys.create_session_for_transfer(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    body = FACTORY.deploys.create_body(payment, session)
    assert isinstance(body, TYPES.DeployBody)
    assert len(body.hash) == 32


def test_create_transfer_header(FACTORY, TYPES, deploy_params):
    payment = FACTORY.deploys.create_payment_for_transfer(
        amount = random.randint(0, 1e5),
        )
    session = FACTORY.deploys.create_session_for_transfer(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    body = FACTORY.deploys.create_body(payment, session)
    header = FACTORY.deploys.create_header(body, deploy_params)
    assert isinstance(header, TYPES.DeployHeader)
    assert len(header.hash) == 32


def test_create_transfer_deploy(FACTORY, TYPES, deploy_params):
    session = FACTORY.deploys.create_session_for_transfer(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    payment = FACTORY.deploys.create_payment_for_transfer(
        amount = random.randint(0, 1e5),
        )
    deploy = FACTORY.deploys.create_deploy(deploy_params, payment, session)
    assert isinstance(deploy, TYPES.Deploy)
    assert len(deploy.hash) == 32
