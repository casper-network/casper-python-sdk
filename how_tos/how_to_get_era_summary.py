import argparse
import json

from pycspr import NodeClient
from pycspr import NodeConnection

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to pull era summary information.")

# CLI argument: host address of target node - defaults to NCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ NCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client = _get_client(args)

    data: dict = client.get_era_summary()

    print("-" * 74)
    print(json.dumps(data, indent=4))
    print("-" * 74)


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
