import json
import random


def test_encode_transfer_payment(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.deploys.create_payment_for_transfer(
            vector["payment"]["amount"]
        )
        assert LIB.encode(entity, 'hex-string') == vector["payment"]["as_hex"]


def test_encode_transfer_session(LIB, FACTORY, vector_deploy_1):
    for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
        entity = FACTORY.deploys.create_session_for_transfer(
            vector["session"]["amount"],
            vector["session"]["target"],
            vector["session"]["transfer_id"]
            )
        print(LIB.encode(entity, 'hex-string'))
        assert LIB.encode(entity, 'hex-string') == vector["session"]["as_hex"]

        raise NotImplementedError()


# def test_encode_transfer_body(FACTORY, vector_deploy_1):
#     for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
#         entity = FACTORY.deploys.create_body(
#             FACTORY.deploys.create_payment_for_transfer(
#                 vector["payment"]["amount"]
#             ),
#             FACTORY.deploys.create_session_for_transfer(
#                 vector["session"]["amount"],
#                 vector["session"]["target"],
#                 vector["session"]["transfer_id"]
#             )
#         )
#         assert entity.hash == vector["hash_of_body"]

# 00 tag
# 00000000 empty module bytes
# 0100000006000000616d6f756e74060000000500e40b540208 args

# 00 00000000 0100000006000000616d6f756e740 60000000500e40b540208
# 00 00000000 0100000006000000616d6f756e740 800e40b5402

# def test_encode_transfer(LIB, FACTORY, deploy_params_static, vector_deploy_1):
#     for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
#         entity = FACTORY.deploys.create_deploy(
#             deploy_params_static,
#             FACTORY.deploys.create_payment_for_transfer(
#                 vector["payment"]["amount"]
#             ),
#             FACTORY.deploys.create_session_for_transfer(
#                 vector["session"]["amount"],
#                 vector["session"]["target"],
#                 vector["session"]["transfer_id"]
#             )
#         )
#         assert entity.hash == vector["hash"]


# def test_encode_payment_standard(LIB, FACTORY, TYPES, cp2, vector_deploy_1):
#     for vector in [v for v in vector_deploy_1 if v["typeof"] == "transfer"]:
#         entity = FACTORY.deploys.create_session_for_transfer(
#             amount=vector["amount"],
#             target=vector["target"],
#             correlation_id=vector["transfer_id"]
#             )
#         assert LIB.encode(entity, 'hex-string') == vector["as_hex"]


# def test_encode_transfer_1(LIB, FACTORY, TYPES, deploy_params, cp1, cp2):
#     print(cp2.account_hash)
#     deploy=FACTORY.deploys.create_deploy(
#         deploy_params,
#         FACTORY.deploys.create_session_for_transfer(
#             amount=2500000000,
#             target=cp2.account_hash,
#             correlation_id=1
#             ),
#         FACTORY.deploys.create_payment_for_transfer(10000000000),
#         )
    
#     as_json = LIB.encode(deploy, 'json')
#     as_bytes = LIB.encode(deploy.session, 'byte-array')


#     print(json.dumps(as_json, indent=4))

#     print(as_bytes)

#     raise NotImplementedError()


# def test_encode_transfer_2(LIB, FACTORY, TYPES, deploy_params, cp1, cp2):
#     deploy=FACTORY.deploys.create_deploy(
#         deploy_params,
#         FACTORY.deploys.create_session_for_transfer(
#             amount=2500000000,
#             target=cp2.account_hash,
#             correlation_id=1
#             ),
#         FACTORY.deploys.create_payment_for_transfer(10000000000),
#         )
    
#     as_byte_array = deploy_encoder(deploy.session)

#     print(deploy_encoder(deploy.payment))
#     print(deploy_encoder(deploy.session))

#     raise NotImplementedError()

# def test_create_execution_arg_simple(LIB, FACTORY, TYPES, vector_cl_data_1):
#     for type_key in TYPES.CL_TYPES_SIMPLE:
#         vector = vector_cl_data_1.get_vector(type_key)
#         cl_type = FACTORY.cl.create_simple(type_key)
#         cl_value = FACTORY.cl.create_value(cl_type, vector["value"])
#         as_bytes = LIB.encode(cl_value, "byte-array")
#         print(f"{cl_value} :: {bytes(as_bytes).hex()}")
#     raise NotImplementedError()
