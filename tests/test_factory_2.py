import datetime
import operator
import random



def test_create_approval(CL_TYPES, DEPLOY_TYPES, DEPLOY_FACTORY, FACTORY, vector_cl_data_1, vector_crypto_2):
    _bytes = vector_cl_data_1.get_value_as_bytes(CL_TYPES.CLTypeKey.BYTE_ARRAY)
    for algo, pbk, pvk in [operator.itemgetter("algo", "pbk", "pvk")(i) for i in vector_crypto_2]:
        account_info = FACTORY.accounts.create_account_info(algo, pvk, pbk)
        approval = DEPLOY_FACTORY.create_approval(account_info, _bytes)
        assert isinstance(approval, DEPLOY_TYPES.Approval)


def test_create_standard_parameters(CL_TYPES, DEPLOY_TYPES, DEPLOY_FACTORY, FACTORY, a_test_account, a_test_chain_id):
    assert isinstance(
        DEPLOY_FACTORY.create_standard_parameters(
            account=FACTORY.accounts.create_public_key(
                a_test_account.algo,
                a_test_account.pbk
            ),
            chain_name=a_test_chain_id,
            dependencies=[],
            gas_price=random.randint(0, 65),
            timestamp=datetime.datetime.utcnow(),
            ttl="1day",
        ),
        DEPLOY_TYPES.DeployStandardParameters
        )


def test_create_transfer_session(DEPLOY_TYPES, DEPLOY_FACTORY):
    assert isinstance(
        DEPLOY_FACTORY.create_session_for_transfer(
            amount = random.randint(0, 1e9),
            correlation_id = random.randint(0, 1e9),
            target = bytes([]),
            ),
        DEPLOY_TYPES.ExecutionInfo_Transfer
        )


def test_create_transfer_payment(DEPLOY_TYPES, DEPLOY_FACTORY):
    assert isinstance(
        DEPLOY_FACTORY.create_payment_for_transfer(
            amount = random.randint(0, 1e5),
        ),
        DEPLOY_TYPES.ExecutionInfo_ModuleBytes
        )


def test_create_transfer_body(DEPLOY_TYPES, DEPLOY_FACTORY, deploy_params):
    payment = DEPLOY_FACTORY.create_payment_for_transfer(
        amount = random.randint(0, 1e5),
        )
    session = DEPLOY_FACTORY.create_session_for_transfer(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    body = DEPLOY_FACTORY.create_body(payment, session)
    assert isinstance(body, DEPLOY_TYPES.DeployBody)
    assert isinstance(body.hash, str)
    assert len(body.hash) == 64


def test_create_transfer_header(DEPLOY_TYPES, DEPLOY_FACTORY, deploy_params):
    payment = DEPLOY_FACTORY.create_payment_for_transfer(
        amount = random.randint(0, 1e5),
        )
    session = DEPLOY_FACTORY.create_session_for_transfer(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    body = DEPLOY_FACTORY.create_body(payment, session)
    header = DEPLOY_FACTORY.create_header(body, deploy_params)
    assert isinstance(header, DEPLOY_TYPES.DeployHeader)
    assert isinstance(header.body_hash, str)
    assert len(header.body_hash) == 64


def test_create_transfer_deploy(DEPLOY_TYPES, DEPLOY_FACTORY, deploy_params):
    session = DEPLOY_FACTORY.create_session_for_transfer(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    payment = DEPLOY_FACTORY.create_payment_for_transfer(
        amount = random.randint(0, 1e5),
        )
    deploy = DEPLOY_FACTORY.create_deploy(deploy_params, payment, session)
    assert isinstance(deploy, DEPLOY_TYPES.Deploy)
    assert isinstance(deploy.hash, str)
    assert len(deploy.hash) == 64
