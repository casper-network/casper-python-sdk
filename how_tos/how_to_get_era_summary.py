import argparse
import json

from pycspr import NodeRpcClient as NodeClient
from pycspr import NodeConnectionInfo

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to pull era summary information.")

# CLI argument: host address of target node - defaults to CCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ CCTL node 1.
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
    print("-" * 74)
    print("PYCSPR :: How To Get Chain Era Summary")
    print("")
    print("Illustrates usage of NodeClient.get_era_summary function.")
    print("-" * 74)

    # Set node client.
    client = _get_client(args)

    data: dict = client.get_era_summary()

    print("-" * 74)
    print(json.dumps(data, indent=4))
    print("-" * 74)


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnectionInfo(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
