import hashlib


def get_hash(data: bytes, size: int) -> bytes:
    """Maps input to a blake2b hash.

    :param data: Data to be hashed.
    :param size: Desired hashing output length.

    :returns: Blake2b hash of input data.

    """
    h = hashlib.blake2b(digest_size=size)
    h.update(data)

    return h.digest()
