import argparse

from pycspr import NodeClient
from pycspr import NodeConnection

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to pull chainspec.")

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
    # Set node client.
    client = _get_client(args)

    data: dict = client.get_chain_spec()

    print("-" * 74)
    print("Chain specification as pure bytes")
    print("-" * 74)
    print(data["chainspec_bytes"])

    if data.get("maybe_genesis_accounts_bytes"):
        print("-" * 74)
        print("Genesis accounts as pure bytes")
        print("-" * 74)
        print(data["maybe_genesis_accounts_bytes"])

    if data.get("maybe_global_state_bytes"):
        print("-" * 74)
        print("Global state as pure bytes")
        print("-" * 74)
        print(data["maybe_global_state_bytes"])


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
