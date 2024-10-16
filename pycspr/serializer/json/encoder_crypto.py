from pycspr.type_defs.crypto import PublicKey
from pycspr.type_defs.crypto import PublicKeyHex
from pycspr.type_defs.crypto import Signature


def encode(entity: object) -> dict:
    """Encodes a domain entity instance to a JSON encodeable dictionary.

    :param entity: A node related type instance to be encoded.
    :returns: A JSON encodeable dictionary.

    """
    typedef = type(entity)
    try:
        encoder = ENCODERS[typedef]
    except KeyError:
        raise ValueError(f"Unknown entity type: {typedef} :: {entity}")
    else:
        return encoder(entity)


def _encode_public_key(entity: PublicKey) -> PublicKeyHex:
    return entity.to_hex()


def _encode_signature(entity: Signature) -> str:
    return entity.to_hex()


ENCODERS = {
    PublicKey: _encode_public_key,
    Signature: _encode_signature,
}
