import argparse

from pycspr.crypto import HashAlgorithm
from pycspr.crypto import get_hash


# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to hash data using pycspr.")

# CLI argument: hashing algorithm.
_ARGS.add_argument(
    "--algo",
    default=HashAlgorithm.BLAKE2B.name,
    dest="algo",
    help="Hashing algorithm to be used - defaults to blake2b.",
    type=str,
    choices=[i.name for i in HashAlgorithm],
    )

# CLI argument: data to be hashed.
_ARGS.add_argument(
    "--data",
    default="أبو يوسف يعقوب بن إسحاق الصبّاح الكندي‎".encode("utf-8"),
    dest="data",
    help="Data to be hashed as a hexadecimal string.",
    type=str,
    )

def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    # Parse args.
    algo=HashAlgorithm[args.algo]

    # Create a digest. 
    digest: bytes = get_hash(args.data, size=32, algo=algo)

    # Create a digest - defaults to blake2b. 
    digest: bytes = get_hash(args.data)


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
