import argparse
import asyncio
import os
import pathlib
import typing

import pycspr
from pycspr import NodeRpcClient as NodeClient
from pycspr import NodeRpcConnectionInfo as NodeConnectionInfo
from pycspr.type_defs.crypto import \
    KeyAlgorithm, \
    PrivateKey, \
    PublicKey
from pycspr.type_defs.cl_values import CLV_ByteArray, CLV_U256
from pycspr.types.node import \
    Deploy, \
    DeployParameters, \
    DeployOfModuleBytes, \
    DeployOfStoredContractByHash


# Path to CCTL network assets.
_PATH_TO_CCTL_ASSETS = pathlib.Path(os.getenv("CCTL")) / "assets"

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to invoke an ERC-20 smart contract.")

# CLI argument: path to contract operator secret key - defaults to CCTL faucet.
_ARGS.add_argument(
    "--operator-secret-key-path",
    default=_PATH_TO_CCTL_ASSETS / "faucet" / "secret_key.pem",
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

# CLI argument: path to user to whom tokens will be transferred - defaults to CCTL user 1.
_ARGS.add_argument(
    "--user-public-key-path",
    default=_PATH_TO_CCTL_ASSETS / "users" / "user-1" / "public_key_hex",
    dest="path_to_user_public_key",
    help="Path to user's public_key_hex file.",
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

# CLI argument: amount in motes to be offered as payment.
_ARGS.add_argument(
    "--payment",
    default=int(1e9),
    dest="deploy_payment",
    help="Amount in motes to be offered as payment.",
    type=int,
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

# CLI argument: amount of ERC-20 tokens to be transferred to user.
_ARGS.add_argument(
    "--amount",
    default=int(2e9),
    dest="amount",
    help="Amount of ERC-20 tokens to be transferred to user.",
    type=int,
    )


async def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Invoke A Smart Contract By Address")
    print("-" * 74)

    # Set node client.
    client: NodeClient = _get_client(args)

    # Set contract operator / user.
    operator, user = _get_operator_and_user_keys(args)

    # Set contract hash.
    contract_hash: bytes = await _get_contract_hash(args, client, operator)

    # Set deploy.
    deploy: Deploy = _get_deploy(args, contract_hash, operator, user)

    # Approve deploy.
    deploy.approve(operator)

    # Dispatch deploy to a node.
    await client.send_deploy(deploy)

    print("-" * 72)
    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")
    print("-" * 72)


def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.

    """
    return NodeClient(NodeConnectionInfo(args.node_host, args.node_port_rpc))


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


async def _get_contract_hash(
    args: argparse.Namespace,
    client: NodeClient,
    operator: PrivateKey
) -> bytes:
    """Returns on-chain contract identifier.

    """
    # Query operator account for a named key == ERC20 & return parsed named key value.
    account_info = await client.get_account_info(operator.account_key)
    for named_key in account_info["named_keys"]:
        if named_key["name"] == "ERC20":
            return bytes.fromhex(named_key["key"][5:])

    raise ValueError("ERC-20 uninstalled ... see how_tos/how_to_install_a_contract.py")


def _get_deploy(
    args: argparse.Namespace,
    contract_hash: bytes,
    key_of_operator: PrivateKey,
    key_of_user: PublicKey
) -> Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    # Set standard deploy parameters.
    params: DeployParameters = pycspr.create_deploy_parameters(
        account=key_of_operator,
        chain_name=args.chain_name
        )

    # Set payment logic.
    payment: DeployOfModuleBytes = pycspr.create_standard_payment(args.deploy_payment)

    # Set session logic.
    session: DeployOfStoredContractByHash = DeployOfStoredContractByHash(
        entry_point="transfer",
        hash=contract_hash,
        args={
            "amount": CLV_U256(args.amount),
            "recipient": CLV_ByteArray(pycspr.get_account_hash(key_of_user.account_key))
        }
    )

    return pycspr.create_deploy(params, payment, session)


# Entry point.
if __name__ == "__main__":
    asyncio.run(_main(_ARGS.parse_args()))
