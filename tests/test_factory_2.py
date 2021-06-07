import datetime
import operator
import random



def test_create_deploy_approval(FACTORY, TYPES, vectors_1, vectors_3):
    _bytes = vectors_1.get_value_as_bytes(TYPES.CLType.BYTE_ARRAY)
    for algo, pbk, pvk in [operator.itemgetter("algo", "pbk", "pvk")(i) for i in vectors_3]:
        account_info = FACTORY.accounts.create_account_info(pbk, pvk, algo)
        approval = FACTORY.deploys.create_approval(account_info, _bytes)
        assert isinstance(approval, TYPES.DeployApproval)


def test_create_deploy_header_1(FACTORY, TYPES, a_test_account, a_test_chain_id):
    assert isinstance(
        FACTORY.deploys.create_header(
            account_key_info=a_test_account,
            body_hash=None,
            chain_name=a_test_chain_id,
            dependencies=[],
            timestamp=datetime.datetime.utcnow(),
            ttl="1day",
        ), 
        TYPES.DeployHeader
        )


def test_create_deploy_header_2(FACTORY, TYPES, a_test_account, a_test_chain_id):
    assert isinstance(
        FACTORY.deploys.create_header(
            account_key_info=a_test_account,
            body_hash=None,
            chain_name=a_test_chain_id
        ), 
        TYPES.DeployHeader
        )


def test_create_deploy_session_for_transfer(FACTORY, TYPES):
    assert isinstance(
        FACTORY.deploys.create_session_for_transfer(
            amount = 1e9,
            correlation_id = random.randint(0, 124),
            target = bytes([]),
            ),
        TYPES.DeployExecutable_Transfer
        )


# def test_create_deploy_payment_for_transfer(LIB):
#     assert isinstance(
#         LIB.factory.create_payment_for_transfer(
#             amount = 1e5,
#         ),
#         LIB.types.DeployExecutable_ModuleBytes
#         )
