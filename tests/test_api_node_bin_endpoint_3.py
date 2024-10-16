import pycctl
from pycspr.api.node.bin import codec
from pycspr.api.node.bin import Client
from pycspr.type_defs.chain import BlockHeader, ConsensusReward
from pycspr.type_defs.crypto import PublicKey
from pycspr.api.node.bin.type_defs import Response



async def test_get_information_reward_by_block_hash(
    NODE_BINARY_CLIENT: Client,
    REQUEST_ID: int,
    BLOCK_HEADER: BlockHeader
):
    _, validator_id = codec.decode(PublicKey, pycctl.accounts.get_validator_public_key_bytes())

    data = await NODE_BINARY_CLIENT.information.get_reward_by_block(
        REQUEST_ID,
        block_id=BLOCK_HEADER.parent_hash,
        validator_id=validator_id,
        delegator_id=None,
    )

    assert isinstance(data, Response)
    assert isinstance(data.payload, (ConsensusReward, type(None)))


async def test_get_information_reward_by_block_height(
    NODE_BINARY_CLIENT: Client,
    REQUEST_ID: int,
    BLOCK_HEADER: BlockHeader
):
    _, validator_id = codec.decode(PublicKey, pycctl.accounts.get_validator_public_key_bytes())

    data = await NODE_BINARY_CLIENT.information.get_reward_by_block(
        REQUEST_ID,
        block_id=BLOCK_HEADER.height,
        validator_id=validator_id,
        delegator_id=None,
    )

    assert isinstance(data, Response)
    assert isinstance(data.payload, (ConsensusReward, type(None)))


async def test_get_information_reward_by_era(
    NODE_BINARY_CLIENT: Client,
    REQUEST_ID: int,
    BLOCK_HEADER: BlockHeader
):
    _, validator_id = codec.decode(PublicKey, pycctl.accounts.get_validator_public_key_bytes())
    _, delegator_id = codec.decode(PublicKey, pycctl.accounts.get_delegator_public_key_bytes())

    data = await NODE_BINARY_CLIENT.information.get_reward_by_era(
        REQUEST_ID,
        era_id=1662,
        # era_id=BLOCK_HEADER.era_id,
        validator_id=validator_id,
        delegator_id=None,
    )
    assert isinstance(data, Response)
    assert isinstance(data.payload, ConsensusReward)
