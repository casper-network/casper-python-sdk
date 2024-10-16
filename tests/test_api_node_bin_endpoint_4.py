import pycctl
from pycspr.api.node.bin import codec
from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.chain import BlockHeader, ConsensusReward
from pycspr.crypto.types import PublicKey
from pycspr.api.node.bin.types.transport import Response


async def test_tx_try_accept_v2(
    NODE_BINARY_CLIENT: Client,
    REQUEST_ID: int,
    BLOCK_HEADER: BlockHeader
):
    _, validator_id = codec.decode(PublicKey, pycctl.accounts.get_validator_public_key_bytes())

    data = await NODE_BINARY_CLIENT.tx.try_accept(
        REQUEST_ID,
        transaction=None,
    )

    assert isinstance(data, Response)
    assert isinstance(data.payload, (ConsensusReward, type(None)))
