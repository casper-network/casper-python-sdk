import argparse
import asyncio
import os
import pathlib

import pycspr
from pycspr import NodeRpcClient as NodeClient
from pycspr import NodeRpcConnectionInfo as NodeConnectionInfo
from pycspr.type_defs.crypto import PrivateKey
from pycspr.type_defs.crypto import PublicKey
from pycspr.type_defs.cl_values import CLV_Key


# Path to CCTL assets.
_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to qeury an ERC-20 smart contract.")

# CLI argument: path to contract operator public key - defaults to CCTL faucet.
_ARGS.add_argument(
    "--operator-public-key-path",
    default=_PATH_TO_CCTL_ASSETS / "faucet" / "public_key_hex",
    dest="path_to_operator_public_key",
    help="Path to operator's public_key_hex file.",
    type=str,
    )

# CLI argument: name of target chain - defaults to CCTL chain.
_ARGS.add_argument(
    "--chain",
    default="cspr-dev-cctl",
    dest="chain_name",
    help="Name of target chain.",
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

# CLI argument: Node API JSON-RPC port - defaults to 11101 @ CCTL node 1.
_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )


async def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Query For A Smart Contract Named Key")
    print("-" * 74)

    # Set node client.
    client: NodeClient = _get_client(args)

    # Set contract operator key.
    operator = _get_operator_key(args)

    # Set contract hash.
    contract_hash: CLV_Key = await _get_contract_hash(client, operator)

    # Issue queries.
    token_decimals = await _get_contract_data(client, contract_hash, "decimals")
    token_name = await _get_contract_data(client, contract_hash, "name")
    token_symbol = await _get_contract_data(client, contract_hash, "symbol")
    token_supply = await _get_contract_data(client, contract_hash, "total_supply")

    print("-" * 72)
    print(f"Token Decimals: {token_decimals}")
    print(f"Token Name: {token_name}")
    print(f"Token Symbol: {token_symbol}")
    print(f"Token Supply: {token_supply}")
    print("-" * 72)


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnectionInfo(args.node_host, args.node_port_rpc))


async def _get_contract_data(client: NodeClient, contract_hash: CLV_Key, key: str) -> bytes:
    """Queries chain for data associated with a contract.

    """
    state_key = f"hash-{contract_hash.identifier.hex()}"
    value = await client.get_state_item(state_key, key)

    return value["CLValue"]["parsed"]


async def _get_contract_hash(client: NodeClient, operator: PrivateKey) -> CLV_Key:
    """Returns on-chain contract identifier.

    """
    named_key = await client.get_account_named_key(operator.account_key, "ERC20")
    if named_key is None:
        raise ValueError("ERC-20 uninstalled ... see how_tos/how_to_install_a_contract.py")

    return named_key


def _get_operator_key(args: argparse.Namespace) -> PublicKey:
    """Returns the smart contract operator's public key.

    """
    return pycspr.parse_public_key(
        args.path_to_operator_public_key,
        )


# Entry point.
if __name__ == "__main__":
    asyncio.run(_main(_ARGS.parse_args()))
