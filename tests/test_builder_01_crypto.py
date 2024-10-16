import pathlib

import pycspr
from pycspr.type_builders import crypto as builders
from pycspr.type_defs.crypto import \
    KeyAlgorithm, \
    PrivateKey, \
    PrivateKeyBytes, \
    PublicKey, \
    PublicKeyBytes
from tests.utils import assert_entity


# async def test_build_account_hash():
#     assert_entity(
#         builders.AccountHash_Builder()
#             .set_algo(KeyAlgorithm.ED25519)
#             .set_key(bytes.fromhex("cd62f1c5cca51fa3c25f4c76a46dd5f6b0988c95da6ea835ec4441d68dcea393"))
#             .build(),
#         PublicKey
#     )


async def test_build_public_key():
    assert_entity(
        builders.PublicKey_Builder()
            .set_algo(KeyAlgorithm.ED25519)
            .set_key(bytes.fromhex("cd62f1c5cca51fa3c25f4c76a46dd5f6b0988c95da6ea835ec4441d68dcea393"))
            .build(),
        PublicKey
    )


async def test_build_private_key_from_pem_file(crypto_key_pair_specs):
    for algo, _, _ in crypto_key_pair_specs:
        pvk, pbk = pycspr.get_key_pair(algo)
        path_to_pvk_pem_file = pycspr.get_pvk_pem_file_from_bytes(pvk, algo)
        assert pathlib.Path(path_to_pvk_pem_file).is_file()

        print(algo)
        builders.PrivateKey_Builder() \
            .set_algo(KeyAlgorithm.ED25519) \
            .parse_pem_file(path_to_pvk_pem_file) \
            .build()


    raise NotImplementedError()
