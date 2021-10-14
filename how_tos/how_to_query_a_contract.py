import argparse
import os
import pathlib
import random
import typing

import pycspr
from pycspr import NodeClient
from pycspr import NodeConnection
from pycspr.types import Deploy
from pycspr.types import DeployParameters
from pycspr.types import ModuleBytes
from pycspr.types import PrivateKey
from pycspr.types import PublicKey
from pycspr.types import StoredContractByHash



# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to qeury an ERC-20 smart contract.")

# CLI argument: path to contract operator public key - defaults to NCTL faucet.
_ARGS.add_argument(
    "--operator-public-key-path",
    default=pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1" / "faucet" / "public_key_hex",
    dest="path_to_operator_public_key",
    help="Path to operator's public_key_hex file.",
    type=str,
    )

# CLI argument: name of target chain - defaults to NCTL chain.
_ARGS.add_argument(
    "--chain",
    default="casper-net-1",
    dest="chain_name",
    help="Name of target chain.",
    type=str,
    )

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
    client: NodeClient = _get_client(args)

    # Set contract operator key.
    operator = _get_operator_key(args)

    # Set contract hash.
    contract_hash: bytes = _get_contract_hash(args, client, operator)

    # Issue queries.
    token_decimals = _get_contract_data(client, contract_hash, "decimals")
    token_name = _get_contract_data(client, contract_hash, "name")
    token_symbol = _get_contract_data(client, contract_hash, "symbol")
    token_supply = _get_contract_data(client, contract_hash, "total_supply")

    print("-------------------------------------------------------------------------------------------------------")
    print(f"Token Decimals: {token_decimals}")
    print(f"Token Name: {token_name}")
    print(f"Token Symbol: {token_symbol}")
    print(f"Token Supply: {token_supply}")
    print("-------------------------------------------------------------------------------------------------------")


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))


def _get_contract_data(client: NodeClient, contract_hash: bytes, key: str) -> bytes:
    """Queries chain for data associated with a contract.

    """
    value = client.get_state_item(f"hash-{contract_hash.hex()}", key)
    
    return value["CLValue"]["parsed"]


def _get_operator_key(args: argparse.Namespace) -> PublicKey:
    """Returns the smart contract operator's public key.

    """
    return pycspr.parse_public_key(
        args.path_to_operator_public_key,
        )


def _get_contract_hash(args: argparse.Namespace, client: NodeClient, operator: PrivateKey) -> bytes:
    """Returns on-chain contract identifier.

    """
    # We query operator account for a named key == ERC20, we then return the parsed named key value.  
    account_info = client.get_account_info(operator.account_key)
    for named_key in account_info["named_keys"]:
        if named_key["name"] == "ERC20":
            return bytes.fromhex(named_key["key"][5:])
    
    raise ValueError("ERC-20 has not been installed ... see how_tos/how_to_install_a_contract.py")


def _get_deploy(args: argparse.Namespace, contract_hash: bytes, operator: PrivateKey, user: PublicKey) -> Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=operator,
            chain_name=args.chain_name
            )

    # Set payment logic.
    payment: ModuleBytes = \
        pycspr.create_standard_payment(args.deploy_payment)

    # Set session logic.
    session: StoredContractByHash = StoredContractByHash(
        entry_point="transfer",
        hash=contract_hash,
        args = [
            pycspr.create_deploy_arg(
                "amount",
                pycspr.cl_value.u256(args.amount)
                ),
            pycspr.create_deploy_arg(
                "recipient",
                pycspr.cl_value.public_key(user)
                ),
        ]
    )

    return pycspr.create_deploy(params, payment, session)


# Entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())
