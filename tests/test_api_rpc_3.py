from pycspr import NodeRpcClient
from pycspr.types.node.rpc import AuctionState
from pycspr.types.node.rpc import EraSummary


async def test_get_auction_info(RPC_CLIENT: NodeRpcClient):
    data = await RPC_CLIENT.get_auction_info()
    assert isinstance(data, AuctionState)

    data = await RPC_CLIENT.get_auction_info(decode=False)
    assert isinstance(data, dict)


async def test_get_era_info_by_switch_block(RPC_CLIENT: NodeRpcClient, switch_block_hash: str):
    data = await RPC_CLIENT.get_era_info_by_switch_block(switch_block_hash)
    assert isinstance(data, dict)


async def test_get_era_summary(RPC_CLIENT: NodeRpcClient, block_hash: str):
    data = await RPC_CLIENT.get_era_summary(block_hash)
    assert isinstance(data, EraSummary)

    data = await RPC_CLIENT.get_era_summary(block_hash, decode=False)
    assert isinstance(data, dict)
