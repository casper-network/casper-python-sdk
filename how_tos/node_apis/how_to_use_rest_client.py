import argparse
import asyncio
import typing

from pycspr import NodeRestClient as NodeClient
from pycspr import NodeRestConnectionInfo as NodeConnectionInfo
from pycspr.types.node.rpc import NodeStatus


# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to invoke a node's REST API.")

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


class _Context():
    def __init__(self, args: argparse.Namespace):
        self.client = NodeClient(NodeConnectionInfo(args.node_host, args.node_port_rest))


async def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Invoke A Node's REST API")
    print("-" * 74)

    ctx = _Context(args)
    for func in [
        _get_chainspec,
        _get_node_metrics,
        _get_node_metric,
        _get_node_status_1,
        _get_node_status_2,
        _get_validator_changes
    ]:
        await func(ctx)


async def _get_chainspec(ctx: _Context):
    chainspec: dict = await ctx.client.get_chainspec()
    assert isinstance(chainspec, dict)
    print("SUCCESS :: get_chainspec")


async def _get_node_metrics(ctx: _Context):
    node_metrics: typing.List[str] = await ctx.client.get_node_metrics()
    assert isinstance(node_metrics, list)
    print("SUCCESS :: get_node_metrics")


async def _get_node_metric(ctx: _Context):
    node_metric: typing.List[str] = await ctx.client.get_node_metric("mem_deploy_gossiper")
    assert isinstance(node_metric, list)
    print("SUCCESS :: get_node_metric")


async def _get_node_status_1(ctx: _Context):
    node_status: dict = await ctx.client.get_node_status(decode=False)
    assert isinstance(node_status, dict)
    print("SUCCESS :: get_node_status_1")


async def _get_node_status_2(ctx: _Context):
    node_status: NodeStatus = await ctx.client.get_node_status()
    assert isinstance(node_status, NodeStatus)
    print("SUCCESS :: get_node_status_2")


async def _get_validator_changes(ctx: _Context):
    validator_changes: dict = await ctx.client.get_validator_changes()
    assert isinstance(validator_changes, list)
    print("SUCCESS :: get_validator_changes")


# Entry point.
if __name__ == "__main__":
    asyncio.run(_main(_ARGS.parse_args()))
