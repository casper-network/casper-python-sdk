import argparse
import typing

import pycspr
from pycspr.crypto import KeyAlgorithm


# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to obtain a checksummed account key.")


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Create new key pair & destructure raw public key.
    key_pair: typing.Tuple[bytes, bytes] = pycspr.crypto.get_key_pair(algo=KeyAlgorithm.ED25519)
    pbk: bytes = key_pair[1]

    # Map raw public key to account key.
    account_key: bytes = pycspr.crypto.get_account_key(KeyAlgorithm.ED25519, pbk)

    # Map account key to checksummed hexadecimal.
    account_key_checksum: str = pycspr.crypto.cl_checksum.encode_account_key(account_key)

    print("Account Key Hexadecimal:")
    print(f" ... raw:         {account_key.hex()}")
    print(f" ... checksummed: {account_key_checksum}")


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
