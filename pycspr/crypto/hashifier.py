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
    HashEncoding.BYTE_ARRAY: lambda x: [int(i) for i in x],
    HashEncoding.HEX: lambda x: x.hex(),
}

# Default length of a hash digest.
DIGEST_LENGTH = 32


def get_hash(
    data: typing.Union[bytes, typing.List[int], str],
    size: int = DIGEST_LENGTH,
    algo: HashAlgorithm = HashAlgorithm.BLAKE2B,
    encoding: HashEncoding = HashEncoding.BYTES,
    ) -> typing.Union[bytes, typing.List[int], str]:
    """Maps input to a blake2b hash.
    
    :param data: Data to be hashed.
    :param size: Desired hashing output length.
    :param algo: Type of hashing algo to apply.
    :param encoding: Hash output encoding type.

    :returns: Encoded hash of input data.

    """ 
    encoder = ENCODERS[encoding]
    algo = ALGOS[algo]

    return encoder(algo.get_hash(_get_data(data), size))


def _get_data(data: typing.Union[bytes, typing.List[int], str]) -> bytes:
    """Maps input data to bytes in readiness for hashing.
    
    """
    if isinstance(data, str):
        return bytes.fromhex(data)
    elif isinstance(data, list):
        return bytes(data)
    else:
        return data
