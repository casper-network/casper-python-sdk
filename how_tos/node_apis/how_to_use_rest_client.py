import argparse
import typing

from pycspr import NodeRestClient as NodeClient
from pycspr import NodeRestConnectionInfo as NodeConnectionInfo


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


def _main(args: argparse.Namespace):
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
        _get_node_status,
        _get_rpc_schema,
        _get_validator_changes
    ]:
        func(ctx)
        print("-" * 74)


def _get_chainspec(ctx: _Context):
    # get_chainspec.
    chainspec: dict = ctx.client.get_chainspec()
    assert isinstance(chainspec, dict)
    print("SUCCESS :: get_chainspec")


def _get_node_metrics(ctx: _Context):
    # get_node_metrics.
    node_metrics: typing.List[str] = ctx.client.get_node_metrics()
    assert isinstance(node_metrics, list)
    print("SUCCESS :: get_node_metrics")

    # ext -> get_node_metric.
    node_metric: typing.List[str] = ctx.client.ext.get_node_metric("mem_deploy_gossiper")
    assert isinstance(node_metric, list)
    print("SUCCESS :: get_node_metric")


def _get_node_status(ctx: _Context):
    # get_node_status.
    node_status: dict = ctx.client.get_node_status()
    assert isinstance(node_status, dict)
    print("SUCCESS :: get_node_status")


def _get_rpc_schema(ctx: _Context):
    # _get_rpc_schema.
    rpc_schema: dict = ctx.client.get_node_rpc_schema()
    assert isinstance(rpc_schema, dict)
    print("SUCCESS :: get_node_rpc_schema")


def _get_validator_changes(ctx: _Context):
    # _get_validator_changes.
    validator_changes: dict = ctx.client.get_validator_changes()
    assert isinstance(validator_changes, dict)
    print("SUCCESS :: get_validator_changes")


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
