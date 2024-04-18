import argparse
import asyncio

from pycspr import NodeRpcClient as NodeClient
from pycspr import NodeRpcConnectionInfo as NodeConnectionInfo
from pycspr.types.node import DictionaryID_ContractNamedKey


# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to query a dictionary item.")


# CLI argument: name of target chain - defaults to CCTL chain.
_ARGS.add_argument(
    "--chain",
    default="casper-test",
    dest="chain_name",
    help="Name of target chain.",
    type=str,
    )

# CLI argument: host address of target node - defaults to CCTL node 1.
_ARGS.add_argument(
    "--node-host",
    default="3.208.91.63",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=7777,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )

# CLI argument: On-chain address of target smart contract.
_ARGS.add_argument(
    "--contract",
    default="75143aa704675b7dead20ac2ee06c1c3eccff4ffcf1eb9aebb8cce7c35648041",
    dest="contract_hash",
    help="On-chain address of target smart contract.",
    type=str,
    )

# CLI argument: The dictionary item key.
_ARGS.add_argument(
    "--dict-item-key",
    default="c95da35f6a727f7af69da9e7cc0f37e5edd9aee89f7b2f2b1507c5f68aa81859",
    dest="dictionary_item_key",
    help="The dictionary item key.",
    type=str,
    )

# CLI argument: # The named key under which the dictionary seed URef is stored..
_ARGS.add_argument(
    "--dict-name",
    default="highscore_dictionary",
    dest="dictionary_name",
    help="# The named key under which the dictionary seed URef is stored..",
    type=str,
    )


async def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Query For A Smart Contract's Named Keys")
    print("-" * 74)

    # Set node client.
    client: NodeClient = _get_client(args)

    # Set dictionary item identifier.
    dictionary_id = DictionaryID_ContractNamedKey(
        dictionary_name=args.dictionary_name,
        dictionary_item_key=args.dictionary_item_key,
        contract_key=args.contract_hash
    )

    # Set node JSON-RPC query response.
    response = await client.get_dictionary_item(dictionary_id)

    print(response)


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnectionInfo(args.node_host, args.node_port_rpc))


# Entry point.
if __name__ == "__main__":
    asyncio.run(_main(_ARGS.parse_args()))
