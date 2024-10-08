import pycctl
from pycspr.api.node.bin import codec
from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.chain import BlockHeader
from pycspr.api.node.bin.types.crypto import PublicKey



async def test_get_information_reward(
    NODE_BINARY_CLIENT: Client,
    REQUEST_ID: int,
    BLOCK_HEADER: BlockHeader
):

    print(BLOCK_HEADER.era_id)
    print(BLOCK_HEADER.height)

    _, validator_id = codec.decode(PublicKey, pycctl.accounts.get_validator_public_key_bytes())
    data = await NODE_BINARY_CLIENT.get_information_reward(
        REQUEST_ID,
        BLOCK_HEADER.era_id,
        validator_id,
        None,
    )
    assert data is not None

    raise ValueError()
