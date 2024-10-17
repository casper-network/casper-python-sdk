import argparse
import asyncio
import os
import pathlib
import typing

import pycspr
from pycspr import NodeRpcClient as NodeClient
from pycspr import NodeRpcConnectionInfo as NodeConnectionInfo
from pycspr.type_defs.cl_values import CLV_URef
from pycspr.types.node import AccountInfo
from pycspr.types.node import AuctionState
from pycspr.types.node import Block
from pycspr.types.node import BlockTransfers
from pycspr.types.node import EraSummary
from pycspr.types.node import GlobalStateID
from pycspr.types.node import GlobalStateIDType
from pycspr.types.node import NodePeer
from pycspr.types.node import NodeStatus
from pycspr.types.node import PurseID
from pycspr.types.node import PurseIDType
from pycspr.types.node import URef
from pycspr.types.node import ValidatorChanges


# Path to CCTL assets.
_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to invoke a node's JSON-RPC API.")

# CLI argument: path to cp2 account key - defaults to CCTL user 2.
_ARGS.add_argument(
    "--account-key-path",
    default=_PATH_TO_CCTL_ASSETS / "users" / "user-1" / "public_key_hex",
    dest="path_to_account_key",
    help="Path to a test user's public_key_hex file.",
    type=str,
    )

# CLI argument: host address of target node - defaults to CCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API REST port - defaults to 14101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rest",
    default=14101,
    dest="node_port_rest",
    help="Node API REST port.  Typically 8888 on most nodes.",
    type=int,
    )

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )

# CLI argument: Node API SSE port - defaults to 18101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-sse",
    default=18101,
    dest="node_port_sse",
    help="Node API SSE port.  Typically 9999 on most nodes.",
    type=int,
    )


class _Context():
    def __init__(self, args: argparse.Namespace):
        self.client = NodeClient(NodeConnectionInfo(args.node_host, args.node_port_rpc))
        self.user_public_key = pycspr.parse_public_key(args.path_to_account_key)


async def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Use Node RPC Client")
    print("-" * 74)

    ctx = _Context(args)
    for func in [
        _get_node_rpc,
        _get_node_peers_1,
        _get_node_peers_2,
        _get_node_status_1,
        _get_node_status_2,
        _get_block_1,
        _get_block_2,
        _get_block_3,
        _get_block_4,
        # _get_block_at_era_switch,
        _get_block_transfers,
        _get_era_info_1,
        _get_era_info_2,
        _get_era_info_3,
        _get_era_summary_1,
        _get_era_summary_2,
        _get_era_summary_3,
        _get_auction_state_1,
        _get_auction_state_2,
        _get_auction_state_3,
        _get_validator_changes_1,
        _get_validator_changes_2,
        _get_specification,
        _get_state_root_hash,
        _get_account_info,
    ]:
        await func(ctx)

    print("-" * 74)


async def _get_account_info(ctx: _Context):
    state_root_hash: bytes = await ctx.client.get_state_root_hash()

    # Query: get_account_info.
    account_info: AccountInfo = await ctx.client.get_account_info(ctx.user_public_key.account_key)
    assert isinstance(account_info, AccountInfo)
    print("SUCCESS :: get_account_info")

    # Query: get_account_main_purse_uref.
    account_main_purse: URef = \
        await ctx.client.get_account_main_purse_uref(ctx.user_public_key.account_key)
    assert isinstance(account_main_purse, URef)
    print("SUCCESS :: get_account_main_purse_uref")

    # Query: get_account_balance.
    global_state_id = GlobalStateID(state_root_hash, GlobalStateIDType.STATE_ROOT_HASH)
    purse_id = PurseID(account_main_purse, PurseIDType.UREF)
    account_balance: int = await ctx.client.get_account_balance(purse_id, global_state_id)
    assert isinstance(account_balance, int)
    print("SUCCESS :: get_account_balance")


async def _get_auction_state_1(ctx: _Context):
    block: Block = await ctx.client.get_block()
    for block_id in {
        None,
        block.hash,
        block.header.height
    }:
        obj: dict = await ctx.client.get_auction_state(block_id, decode=False)
        assert isinstance(obj, dict)
        print(f"SUCCESS :: get_auction_state (raw) :: block-id={block_id}")


async def _get_auction_state_2(ctx: _Context):
    block: Block = await ctx.client.get_block()
    for block_id in {
        None,
        block.hash,
        block.header.height
    }:
        obj: AuctionState = await ctx.client.get_auction_state(block_id)
        assert isinstance(obj, AuctionState)
        print(f"SUCCESS :: get_auction_state :: block-id={block_id}")


async def _get_auction_state_3(ctx: _Context):
    block: Block = await ctx.client.get_block()
    assert await ctx.client.get_auction_state(block.hash) == \
           await ctx.client.get_auction_state(block.header.height)
    print("SUCCESS :: get_auction_state - by equivalent block height & hash")


async def _get_block_1(ctx: _Context):
    block: Block = await ctx.client.get_block()
    assert isinstance(block, Block)
    print("SUCCESS :: get_block :: block-id=None")


async def _get_block_2(ctx: _Context):
    block: Block = await ctx.client.get_block()
    for block_id in {
        block.hash,
        block.header.height
    }:
        block: dict = await ctx.client.get_block(block_id, decode=False)
        assert isinstance(block, dict)
        print(f"SUCCESS :: get_block (raw) :: block-id={block_id}")


async def _get_block_3(ctx: _Context):
    block: Block = await ctx.client.get_block()
    for block_id in {
        block.hash,
        block.header.height
    }:
        block: Block = await ctx.client.get_block(block_id)
        assert isinstance(block, Block)
        print(f"SUCCESS :: get_block :: block-id={block_id}")


async def _get_block_4(ctx: _Context):
    block: Block = await ctx.client.get_block()
    assert await ctx.client.get_block(block.hash) == \
           await ctx.client.get_block(block.header.height)
    print("SUCCESS :: get_block - by equivalent height & hash")


async def _get_block_at_era_switch(ctx: _Context):
    print("POLLING :: get_block_at_era_switch - may take some time")
    block: Block = await ctx.client.get_block_at_era_switch()
    assert isinstance(block, Block)
    print("SUCCESS :: get_block_at_era_switch")


async def _get_block_transfers(ctx: _Context):
    block: Block = await ctx.client.get_block()

    # Query: by hash.
    entity: BlockTransfers = await ctx.client.get_block_transfers(block.hash)
    assert isinstance(entity, BlockTransfers)
    print("SUCCESS :: invoked get_block_transfers - by block hash")

    # Query: by height.
    assert entity == await ctx.client.get_block_transfers(block.header.height)
    print("SUCCESS :: invoked get_block_transfers - by block height")


async def _get_era_info_1(ctx: _Context):
    print("POLLING :: get_block_at_era_switch (raw) - may take some time")
    block: Block = await ctx.client.get_block_at_era_switch()
    for block_id in {
        None,
        block.hash,
        block.header.height
    }:
        era_info: dict = await ctx.client.get_era_info(block_id, decode=False)
        assert isinstance(era_info, dict)
        print(f"SUCCESS :: get_era_info (raw) :: block-id={block_id}")
        assert era_info == await ctx.client.get_era_info_by_switch_block(block_id, decode=False)


async def _get_era_info_2(ctx: _Context):
    print("POLLING :: get_block_at_era_switch - may take some time")
    block: Block = await ctx.client.get_block_at_era_switch()
    for block_id in {
        None,
        block.hash,
        block.header.height
    }:
        era_info: EraSummary = await ctx.client.get_era_info(block_id)
        assert isinstance(era_info, EraSummary)
        print(f"SUCCESS :: get_era_info :: block-id={block_id}")
        assert era_info == await ctx.client.get_era_info_by_switch_block(block_id)


async def _get_era_info_3(ctx: _Context):
    print("POLLING :: get_block_at_era_switch - may take some time")
    block: Block = await ctx.client.get_block_at_era_switch()
    assert await ctx.client.get_era_info(block.hash) == \
           await ctx.client.get_era_info(block.header.height)
    print("SUCCESS :: get_era_info - by equivalent block height & hash")


async def _get_era_summary_1(ctx: _Context):
    block: Block = await ctx.client.get_block()

    for block_id in {
        None,
        block.hash,
        block.header.height
    }:
        entity: dict = await ctx.client.get_era_summary(block_id, decode=False)
        assert isinstance(entity, dict)
        print(f"SUCCESS :: get_era_summary (raw) :: block-id={block_id}")


async def _get_era_summary_2(ctx: _Context):
    block: Block = await ctx.client.get_block()
    for block_id in {
        None,
        block.hash,
        block.header.height
    }:
        entity: EraSummary = await ctx.client.get_era_summary(block_id)
        assert isinstance(entity, EraSummary)
        print(f"SUCCESS :: get_era_summary :: block-id={block_id}")


async def _get_era_summary_3(ctx: _Context):
    block: Block = await ctx.client.get_block()
    assert await ctx.client.get_era_summary(block.hash) == \
           await ctx.client.get_era_summary(block.header.height)
    print("SUCCESS :: get_era_summary :: by equivalent block height & hash")


async def _get_specification(ctx: _Context):
    chainspec: dict = await ctx.client.get_chainspec()
    assert isinstance(chainspec, dict)


async def _get_state_root_hash(ctx: _Context):
    block: Block = await ctx.client.get_block()

    for block_id in {
        None,
        block.hash,
        block.header.height
    }:
        state_root_hash: bytes = await ctx.client.get_state_root_hash(block_id)
        assert isinstance(state_root_hash, bytes)
        print(f"SUCCESS :: get_state_root_hash :: block-id={block_id}")

    assert await ctx.client.get_state_root_hash(block.hash) == \
           await ctx.client.get_state_root_hash(block.header.height)
    print("SUCCESS :: get_state_root_hash :: by equivalent switch block height & hash")


async def _get_node_peers_1(ctx: _Context):
    node_peers: typing.List[dict] = await ctx.client.get_node_peers(decode=False)
    assert isinstance(node_peers, list)
    for item in node_peers:
        assert isinstance(item, dict)
    print("SUCCESS :: get_node_peers (raw)")


async def _get_node_peers_2(ctx: _Context):
    node_peers: typing.List[NodePeer] = await ctx.client.get_node_peers()
    assert isinstance(node_peers, list)
    for item in node_peers:
        assert isinstance(item, NodePeer)
    print("SUCCESS :: get_node_peers")


async def _get_node_status_1(ctx: _Context):
    node_status: NodeStatus = await ctx.client.get_node_status(decode=False)
    assert isinstance(node_status, dict)
    print("SUCCESS :: get_node_status (raw)")


async def _get_node_status_2(ctx: _Context):
    node_status: NodeStatus = await ctx.client.get_node_status()
    assert isinstance(node_status, NodeStatus)
    print("SUCCESS :: get_node_status")


async def _get_node_rpc(ctx: _Context):
    # get_rpc_schema.
    rpc_schema: dict = await ctx.client.get_rpc_schema()
    assert isinstance(rpc_schema, dict)
    print("SUCCESS :: get_rpc_schema")

    # get_rpc_endpoints.
    rpc_endpoints: typing.List[str] = await ctx.client.get_rpc_endpoints()
    assert isinstance(rpc_endpoints, list)
    print("SUCCESS :: get_rpc_endpoints")

    # get_rpc_endpoint.
    for rpc_endpoint in rpc_endpoints:
        rpc_endpoint_schema: dict = await ctx.client.get_rpc_endpoint("account_put_deploy")
        assert isinstance(rpc_endpoint_schema, dict)
    print("SUCCESS :: get_rpc_endpoint")


async def _get_validator_changes_1(ctx: _Context):
    validator_changes: typing.List[ValidatorChanges] = \
        await ctx.client.get_validator_changes(decode=False)
    assert isinstance(validator_changes, list)
    for item in validator_changes:
        assert isinstance(item, dict)
    print("SUCCESS :: get_validator_changes (raw)")


async def _get_validator_changes_2(ctx: _Context):
    validator_changes: typing.List[ValidatorChanges] = \
        await ctx.client.get_validator_changes()
    assert isinstance(validator_changes, list)
    for item in validator_changes:
        assert isinstance(item, ValidatorChanges)
    print("SUCCESS :: get_validator_changes")


# Entry point.
if __name__ == "__main__":
    asyncio.run(_main(_ARGS.parse_args()))
