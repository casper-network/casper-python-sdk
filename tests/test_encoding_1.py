import json
import random


def test_encode_transfer(LIB, FACTORY, TYPES, deploy_params, cp1, cp2):
    print(cp2.account_hash)
    deploy=FACTORY.deploys.create_deploy(
        deploy_params,
        FACTORY.deploys.create_session_for_transfer(
            amount=2500000000,
            target=cp2.account_hash,
            correlation_id=1
            ),
        FACTORY.deploys.create_payment_for_transfer(10000000000),
        )
    as_json = LIB.encode_1(deploy, 'json')

    print(json.dumps(as_json, indent=4))


    raise NotImplementedError()


def test_create_execution_arg_simple(LIB, FACTORY, TYPES, vectors_1):
    for type_key in TYPES.CL_TYPES_SIMPLE:
        vector = vectors_1.get_vector(type_key)
        cl_type = FACTORY.cl_types.create_simple(type_key)
        cl_value = FACTORY.cl_types.create_value(cl_type, vector["value"])
        as_bytes = LIB.encode_1(cl_value, "byte-array")
        print(f"{cl_value} :: {bytes(as_bytes).hex()}")
    raise NotImplementedError()
