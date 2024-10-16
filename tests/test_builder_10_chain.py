from pycspr.api.node.bin.builders import chain as builders
from pycspr.type_defs.crypto import KeyAlgorithm, PublicKey, PublicKeyBytes
from tests.utils import assert_entity


async def test_build_account_hash():
    assert_entity(
        builders.AccountHash_Builder()
            .set_algo(KeyAlgorithm.ED25519)
            .set_key(bytes.fromhex("cd62f1c5cca51fa3c25f4c76a46dd5f6b0988c95da6ea835ec4441d68dcea393"))
            .build(),
        PublicKey
    )
