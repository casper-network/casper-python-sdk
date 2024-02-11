import blake3 as _hashlib


def get_hash(data: bytes, size: int) -> bytes:
    """Maps input to a blake2b hash.

    :param data: Data to be hashed.
    :param size: Desired hashing output length.

    :returns: Blake2b hash of input data.

    """
    return _hashlib.blake3(data).digest(length=size)
