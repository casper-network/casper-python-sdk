from pycspr.crypto.hashifier_blake2b import get_hash as blake2b
from pycspr.crypto.enums import HashAlgorithm


# Map: Hash Algo Type -> Hash Algo Implementation.
ALGOS = {
    HashAlgorithm.BLAKE2B: blake2b,
}

# Default length of a hash digest.
DIGEST_LENGTH = 32


def get_hash(
    data: bytes,
    size: int = DIGEST_LENGTH,
    algo: HashAlgorithm = HashAlgorithm.BLAKE2B
) -> bytes:
    """Maps input to a blake2b hash.

    :param data: Data to be hashed.
    :param size: Desired hashing output length.
    :param algo: Type of hashing algo to apply.
    :returns: Hash of input data.

    """
    return ALGOS[algo](data, size)
