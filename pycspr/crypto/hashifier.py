from pycspr.crypto.hashifier_blake2b import get_hash as blake2b
from pycspr.crypto.hashifier_blake3 import get_hash as blake3
from pycspr.type_defs.crypto import DigestBytes
from pycspr.type_defs.crypto import HashAlgorithm


# Map: Hash Algo Type -> Hash Algo Implementation.
ALGOS = {
    HashAlgorithm.BLAKE2B: blake2b,
    HashAlgorithm.BLAKE3: blake3,
}

# Default length of a hash digest.
DEFAULT_DIGEST_LENGTH = 32

# Default hash algo.
DEFAULT_HASH_ALGO = HashAlgorithm.BLAKE2B


def get_hash(
    data: bytes,
    size: int = DEFAULT_DIGEST_LENGTH,
    algo: HashAlgorithm = DEFAULT_HASH_ALGO
) -> DigestBytes:
    """Maps input to a hash function output.

    :param data: Data to be hashed.
    :param size: Desired hashing output length.
    :param algo: Type of hashing algo to apply.
    :returns: Digest of input data.

    """
    return ALGOS[algo](data, size)
