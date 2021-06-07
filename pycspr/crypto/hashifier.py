import typing

from pycspr.crypto import hashifier_blake2b as blake2b
from pycspr.crypto.enums import HashAlgorithm
from pycspr.crypto.enums import HashEncoding



# Map: Hash Algo Type -> Hash Algo Implementation.
ALGOS = {
    HashAlgorithm.BLAKE2B: blake2b,
}

# Map: Hash encoding <-> encoder.
ENCODERS = {
    HashEncoding.BYTES: lambda x: x,
    HashEncoding.HEX: lambda x: x.hex(),
}

# Default length of a hash digest.
_DIGEST_LENGTH = 32


def get_hash(
    data: bytes,
    size: int = _DIGEST_LENGTH,
    algo: HashAlgorithm = HashAlgorithm.BLAKE2B,
    encoding: HashEncoding = HashEncoding.BYTES,
    ) -> typing.Union[bytes, str]:
    """Maps input to a blake2b hash.
    
    :param data: Data to be hashed.
    :param size: Desired hashing output length.
    :param algo: Type of hashing algo to apply.
    :param encoding: Hash output encoding type.

    :returns: Encoded hash of input data.

    """ 
    return ENCODERS[encoding](ALGOS[algo].get_hash(data, size))
