from pycspr import NodeRpcClient
from pycspr.types.node import AuctionState
from pycspr.types.node import EraSummary


async def test_get_auction_info_1(SIDECAR_RPC_CLIENT: NodeRpcClient):
    data = await SIDECAR_RPC_CLIENT.get_auction_info()
    assert isinstance(data, AuctionState)


async def test_get_auction_info_2(SIDECAR_RPC_CLIENT: NodeRpcClient):
    data = await SIDECAR_RPC_CLIENT.get_auction_info(decode=False)
    assert isinstance(data, dict)


async def test_get_era_info_by_switch_block_1(SIDECAR_RPC_CLIENT: NodeRpcClient, switch_block_hash: str):
    data = await SIDECAR_RPC_CLIENT.get_era_info_by_switch_block(switch_block_hash)
    assert isinstance(data, EraSummary)


async def test_get_era_info_by_switch_block_2(SIDECAR_RPC_CLIENT: NodeRpcClient, switch_block_hash: str):
    data = await SIDECAR_RPC_CLIENT.get_era_info_by_switch_block(switch_block_hash, decode=False)
    assert isinstance(data, dict)


async def test_get_era_summary_1(SIDECAR_RPC_CLIENT: NodeRpcClient, block_hash: str):
    data = await SIDECAR_RPC_CLIENT.get_era_summary(block_hash)
    assert isinstance(data, EraSummary)


async def test_get_era_summary_2(SIDECAR_RPC_CLIENT: NodeRpcClient, block_hash: str):
    data = await SIDECAR_RPC_CLIENT.get_era_summary(block_hash, decode=False)
    assert isinstance(data, dict)
