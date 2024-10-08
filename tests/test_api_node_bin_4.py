import pycctl
from pycspr.api.node.bin import codec
from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.chain import BlockHeader, ConsensusReward
from pycspr.api.node.bin.types.crypto import PublicKey
from pycspr.api.node.bin.types.transport import Response



async def test_get_information_reward(
    NODE_BINARY_CLIENT: Client,
    REQUEST_ID: int,
    BLOCK_HEADER: BlockHeader
):
    _, validator_id = codec.decode(PublicKey, pycctl.accounts.get_validator_public_key_bytes())

    data = await NODE_BINARY_CLIENT.get_information_reward(
        REQUEST_ID,
        era_id=BLOCK_HEADER.era_id,
        validator_id=validator_id,
        delegator_id=None,
    )
    assert isinstance(data, Response)
    assert isinstance(data.payload, ConsensusReward)
