import argparse

import pycspr


# CLI argument parser.
_ARGS = argparse.ArgumentParser("Demo illustrating how to sign data using pycspr.")

# CLI argument: data to be signed.
_ARGS.add_argument(
    "--data",
    default="أبو يوسف يعقوب بن إسحاق الصبّاح الكندي".encode("utf-8"),
    dest="data",
    help="Data to be signed.",
    type=str,
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    print("-" * 74)
    print("PYCSPR :: How To Sign Data")
    print("")
    print("Illustrates usage of pycspr.get_signature function.")
    print("-" * 74)
    print(f"Data to be signed: {args.data.decode()}")
    print("-" * 74)

    # Create a digest - algo = default, size = 32 = default.
    digest: bytes = pycspr.get_hash(args.data)
    print("Hash of data")
    print(f"  Algo:  {pycspr.DEFAULT_HASH_ALGO.name}")
    print(f"  Hash:  {digest.hex()}")

    # Iterate supported algos:
    for algo in pycspr.KeyAlgorithm:
        # Sign over digest with a private key.
        pvk, _ = pycspr.get_key_pair(algo)
        sig: bytes = pycspr.get_signature(digest, algo, pvk)

        print("Signature over hash of data")
        print(f"  Algo:  {algo.name}")
        print(f"  Sig :  {sig.hex()}")


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
