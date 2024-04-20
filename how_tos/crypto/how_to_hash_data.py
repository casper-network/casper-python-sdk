import argparse

import pycspr


# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to hash data using pycspr.")

# CLI argument: data to be hashed.
_ARGS.add_argument(
    "--data",
    default="أبو يوسف يعقوب بن إسحاق الصبّاح الكندي".encode("utf-8"),
    dest="data",
    help="Data to be hashed as a hexadecimal string.",
    type=str,
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Get Cryptographic Hash")
    print("")
    print("Illustrates usage of pycspr.get_hash function.")
    print("-" * 74)
    print(f"Data to be hashed: {args.data.decode()}")
    print("-" * 74)

    # Create a digest - algo = default, default size = 32.
    digest: bytes = pycspr.get_hash(args.data)
    assert isinstance(digest, bytes) and len(digest) == 32

    # Iterate supported algos:
    for algo in pycspr.HashAlgorithm:
        # Create a digest - default size = 32.
        digest: bytes = pycspr.get_hash(args.data, algo=algo, size=32)
        assert isinstance(digest, bytes) and len(digest) == 32
        print("Hash of data")
        print(f"    Algo:  {algo.name}")
        print(f"    Hash -> 32 bytes :: {algo.name} = {digest.hex()}")

        # Create a digest - size = 64.
        digest: bytes = pycspr.get_hash(args.data, algo=algo, size=64)
        assert isinstance(digest, bytes) and len(digest) == 64
        print(f"    Hash -> 64 bytes :: {algo.name} = {digest.hex()}")


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
