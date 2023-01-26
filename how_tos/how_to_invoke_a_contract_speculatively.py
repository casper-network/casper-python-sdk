import argparse
import os
import pathlib
import typing

import pycspr
from pycspr import NodeClient
from pycspr import NodeConnection
from pycspr.crypto import KeyAlgorithm
from pycspr.types import CL_ByteArray
from pycspr.types import CL_U256
from pycspr.types import Deploy
from pycspr.types import DeployParameters
from pycspr.types import ModuleBytes
from pycspr.types import PrivateKey
from pycspr.types import PublicKey
from pycspr.types import StoredContractByHash


# Path to NCTL network assets.
_PATH_TO_NCTL_ASSETS = pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to speculatively invoke an ERC-20 smart contract.")

# CLI argument: path to contract operator secret key - defaults to NCTL faucet.
_ARGS.add_argument(
    "--operator-secret-key-path",
    default=_PATH_TO_NCTL_ASSETS / "faucet" / "secret_key.pem",
    dest="path_to_operator_secret_key",
    help="Path to operator's secret_key.pem file.",
    type=str,
    )

# CLI argument: type of contract operator secret key - defaults to ED25519.
_ARGS.add_argument(
    "--operator-secret-key-type",
    default=KeyAlgorithm.ED25519.name,
    dest="type_of_operator_secret_key",
    help="Type of operator's secret key.",
    type=str,
    )

# CLI argument: path to user to whom tokens will be transferred - defaults to NCTL user 1.
_ARGS.add_argument(
    "--user-public-key-path",
    default=_PATH_TO_NCTL_ASSETS / "users" / "user-1" / "public_key_hex",
    dest="path_to_user_public_key",
    help="Path to user's public_key_hex file.",
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

# CLI argument: amount in motes to be offered as payment.
_ARGS.add_argument(
    "--payment",
    default=int(1e9),
    dest="deploy_payment",
    help="Amount in motes to be offered as payment.",
    type=int,
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

# CLI argument: amount of ERC-20 tokens to be transferred to user.
_ARGS.add_argument(
    "--amount",
    default=int(2e9),
    dest="amount",
    help="Amount of ERC-20 tokens to be transferred to user.",
    type=int,
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Set node client.
    client: NodeClient = _get_client(args)

    # Set contract operator / user.
    operator, user = _get_operator_and_user_keys(args)

    # Set contract hash.
    contract_hash: bytes = _get_contract_hash(args, client, operator)

    # Set deploy.
    deploy: Deploy = _get_deploy(args, contract_hash, operator, user)

    # Approve deploy.
    deploy.approve(operator)

    # Dispatch deploy to a node for speculative execution.
    response = client.speculative_exec(deploy)

    print(response)

    print("-" * 72)
    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")
    print("-" * 72)


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))


def _get_operator_and_user_keys(args: argparse.Namespace) -> typing.Tuple[PrivateKey, PublicKey]:
    """Returns the smart contract operator's private key.

    """
    operator = pycspr.parse_private_key(
        args.path_to_operator_secret_key,
        args.type_of_operator_secret_key,
        )
    user = pycspr.parse_public_key(
        args.path_to_user_public_key,
        )

    return operator, user


def _get_contract_hash(
    args: argparse.Namespace,
    client: NodeClient,
    operator: PrivateKey
) -> bytes:
    """Returns on-chain contract identifier.

    """
    # Query operator account for a named key == ERC20 & return parsed named key value.
    account_info = client.get_account_info(operator.account_key)
    for named_key in account_info["named_keys"]:
        if named_key["name"] == "ERC20":
            return bytes.fromhex(named_key["key"][5:])

    raise ValueError("ERC-20 uninstalled ... see how_tos/how_to_install_a_contract.py")


def _get_deploy(
    args: argparse.Namespace,
    contract_hash: bytes,
    operator: PrivateKey,
    user: PublicKey
) -> Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    params: DeployParameters = pycspr.create_deploy_parameters(
        account=operator,
        chain_name=args.chain_name
        )

    # Set payment logic.
    payment: ModuleBytes = pycspr.create_standard_payment(args.deploy_payment)

    # Set session logic.
    session: StoredContractByHash = StoredContractByHash(
        entry_point="transfer",
        hash=contract_hash,
        args={
            "amount": CL_U256(args.amount),
            "recipient": CL_ByteArray(user.account_hash)
        }
    )

    return pycspr.create_deploy(params, payment, session)


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
