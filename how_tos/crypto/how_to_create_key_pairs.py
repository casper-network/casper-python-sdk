import argparse
import base64
import typing

import pycspr
from pycspr.types.crypto import KeyAlgorithm


# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to create key pairs using pycspr.")

# CLI argument: key algorithm.
_ARGS.add_argument(
    "--algo",
    default=KeyAlgorithm.ED25519.name,
    dest="algo",
    help="Key algorithm to be used - defaults to ed25519.",
    type=str,
    choices=[i.name for i in KeyAlgorithm],
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Create Key Pairs")
    print("")
    print("Illustrates usage of get_key_pair & get_key_pair_from_* functions.")
    print("-" * 74)

    # Parse args.
    algo = KeyAlgorithm[args.algo]

    # Create new key pair.
    key_pair: typing.Union[bytes, bytes] = pycspr.crypto.get_key_pair(algo=algo)
    assert len(key_pair) == 2

    # Destructure key pair.
    pvk, pbk = key_pair
    assert isinstance(pvk, bytes) and isinstance(pbk, bytes)

    # Create key pair from private key as bytes.
    key_pair_1 = pycspr.crypto.get_key_pair_from_bytes(pvk, algo=algo)
    assert key_pair_1 == key_pair

    # Create key pair from private key as hex.
    pvk_as_hex = pvk.hex()
    key_pair_2 = pycspr.crypto.get_key_pair_from_hex_string(pvk_as_hex, algo=algo)
    assert key_pair_2 == key_pair

    # Create key pair from private key as base64.
    pvk_as_base64 = base64.b64encode(pvk)
    key_pair_3 = pycspr.crypto.get_key_pair_from_base64(pvk_as_base64, algo=algo)
    assert key_pair_3 == key_pair

    # Create key pair from private key as pem file.
    pvk_as_pem_file = pycspr.crypto.get_pvk_pem_file_from_bytes(pvk, algo)
    key_pair_4 = pycspr.crypto.get_key_pair_from_pem_file(pvk_as_pem_file, algo=algo)
    assert key_pair_4 == key_pair


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
