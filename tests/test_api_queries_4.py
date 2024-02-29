import pycspr
from pycspr.api.rpc import types as rpc_types


def test_get_auction_info_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient):
    assert isinstance(
        RPC_CLIENT.get_auction_info(),
        rpc_types.AuctionState
        )
    assert isinstance(
        RPC_CLIENT.get_auction_info(decode=False),
        dict
        )


def test_get_era_info_by_switch_block_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient, switch_block_hash: str):
    assert isinstance(
        RPC_CLIENT.get_era_info_by_switch_block(switch_block_hash),
        dict
        )


def test_get_era_summary_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient, block_hash: str):
    assert isinstance(
        RPC_CLIENT.get_era_summary(block_hash),
        rpc_types.EraSummary
        )
    assert isinstance(
        RPC_CLIENT.get_era_summary(block_hash, decode=False),
        dict
        )
