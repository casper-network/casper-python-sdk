import datetime
import operator
import random



def test_create_deploy_parameters(TYPES, FACTORY, a_test_account, a_test_chain_id):
    assert isinstance(
        FACTORY.create_deploy_parameters(
            account=FACTORY.create_public_key(
                a_test_account.algo,
                a_test_account.pbk
            ),
            chain_name=a_test_chain_id,
            dependencies=[],
            gas_price=random.randint(0, 65),
            timestamp=datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            ttl="1day",
        ),
        TYPES.DeployParameters
        )


def test_create_standard_payment(TYPES, FACTORY):
    assert isinstance(
        FACTORY.create_standard_payment(
            amount = random.randint(0, 1e5),
        ),
        TYPES.ExecutableDeployItem_ModuleBytes
        )


    def test_create_native_transfer_session(TYPES, FACTORY):
        assert isinstance(
            FACTORY.create_native_transfer_session(
                amount = random.randint(0, 1e9),
                correlation_id = random.randint(0, 1e9),
                target = bytes([]),
                ),
            TYPES.ExecutableDeployItem_Transfer
            )


def test_create_native_transfer_body(TYPES, FACTORY, deploy_params):
    payment = FACTORY.create_standard_payment(
        amount = random.randint(0, 1e5),
        )
    session = FACTORY.create_native_transfer_session(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    body = FACTORY.create_deploy_body(payment, session)
    assert isinstance(body, TYPES.DeployBody)
    assert isinstance(body.hash, bytes)
    assert len(body.hash) == 32


def test_create_native_transfer_header(TYPES, FACTORY, deploy_params):
    payment = FACTORY.create_standard_payment(
        amount = random.randint(0, 1e5),
        )
    session = FACTORY.create_native_transfer_session(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = bytes([]),
        )
    body = FACTORY.create_deploy_body(payment, session)
    header = FACTORY.create_deploy_header(body, deploy_params)
    assert isinstance(header, TYPES.DeployHeader)
    assert isinstance(header.body_hash, bytes)
    assert len(header.body_hash) == 32


def test_create_native_transfer_deploy(TYPES, FACTORY, deploy_params, cp2):
    session = FACTORY.create_native_transfer_session(
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = cp2.account_hash,
        )
    payment = FACTORY.create_standard_payment(
        amount = random.randint(0, 1e5),
        )
    deploy = FACTORY.create_deploy(deploy_params, payment, session)
    assert isinstance(deploy, TYPES.Deploy)
    assert isinstance(deploy.hash, bytes)
    assert len(deploy.hash) == 32
