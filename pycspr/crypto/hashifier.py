from pycspr.crypto.hashifier_blake2b import get_hash as blake2b
from pycspr.crypto.hashifier_blake3 import get_hash as blake3
from pycspr.crypto.defaults import DEFAULT_HASH_ALGO
from pycspr.crypto.enums import HashAlgorithm


# Map: Hash Algo Type -> Hash Algo Implementation.
ALGOS = {
    HashAlgorithm.BLAKE2B: blake2b,
    HashAlgorithm.BLAKE3: blake3,
}

# Default length of a hash digest.
DIGEST_LENGTH = 32


def get_hash(
    data: bytes,
    size: int = DIGEST_LENGTH,
    algo: HashAlgorithm = DEFAULT_HASH_ALGO
) -> bytes:
    """Maps input to a hash function output.

    :param data: Data to be hashed.
    :param size: Desired hashing output length.
    :param algo: Type of hashing algo to apply.
    :returns: Hash of input data.

    """
    return ALGOS[algo](data, size)
