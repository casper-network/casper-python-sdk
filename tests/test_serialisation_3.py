import pycspr

# from pycspr.factory.deploys import create_deploy
# from pycspr.factory.deploys import create_deploy_approval
# from pycspr.factory.deploys import create_deploy_arg
# from pycspr.factory.deploys import create_deploy_body
# from pycspr.factory.deploys import create_deploy_header
# from pycspr.factory.deploys import create_deploy_parameters
# from pycspr.factory.deploys import create_deploy_ttl
# from pycspr.factory.deploys import create_native_transfer
# from pycspr.factory.deploys import create_native_transfer_session
# from pycspr.factory.deploys import create_standard_payment
# from pycspr.factory.deploys import create_validator_auction_bid
# from pycspr.factory.deploys import create_validator_auction_bid_withdrawal
# from pycspr.factory.deploys import create_validator_delegation
# from pycspr.factory.deploys import create_validator_delegation_withdrawal
# from pycspr.factory.digests import create_digest_of_deploy
# from pycspr.factory.digests import create_digest_of_deploy_body


def test_that_standard_payment_serialises_to_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert pycspr.to_bytes(entity) == vector["bytes"]["payment"]
        # assert entity == pycspr.from_bytes(pycspr.to_bytes(entity))


def test_that_standard_payment_serialises_to_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_standard_payment(
            vector["payment"]["amount"]
        )
        assert entity == pycspr.from_json(type(entity), pycspr.to_json(entity))


def test_that_a_standard_transfer_session_serialises_to_bytes(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_native_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        assert pycspr.to_bytes(entity) == vector["bytes"]["session"]
        # assert entity == pycspr.from_bytes(pycspr.to_bytes(entity))


def test_that_a_standard_transfer_session_serialises_to_json(deploys_1):
    for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
        entity = pycspr.factory.create_native_transfer_session(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["correlation_id"]
            )
        assert entity == pycspr.from_json(type(entity), pycspr.to_json(entity))


# def test_that_a_deploy_body_can_be_encoded_as_bytes(deploys_1):
#     for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
#         entity = pycspr.factory.create_deploy_body(
#             pycspr.factory.create_standard_payment(
#                 vector["payment"]["amount"]
#                 ),
#             pycspr.factory.create_native_transfer_session(
#                 vector["session"]["amount"],
#                 vector["session"]["target"],
#                 vector["session"]["correlation_id"]
#                 )
#         )
#         assert entity.hash == vector["hashes"]["body"]


# def test_that_a_deploy_can_be_encoded_as_bytes(deploy_params_static, deploys_1):
#     for vector in [v for v in deploys_1 if v["typeof"] == "transfer"]:
#         entity = pycspr.factory.create_deploy(
#             deploy_params_static,
#             pycspr.factory.create_standard_payment(
#                 vector["payment"]["amount"]
#             ),
#             pycspr.factory.create_native_transfer_session(
#                 vector["session"]["amount"],
#                 vector["session"]["target"],
#                 vector["session"]["correlation_id"]
#             )
#         )
#         assert entity.hash == vector["hashes"]["deploy"]
