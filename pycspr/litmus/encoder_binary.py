from __future__ import annotations

from pycspr.litmus.types import SemanticVersion


_ENCODERS = {
    SemanticVersion: encode_semantic_version,
}


def encode(entity: object) -> bytes:
    """Encodes a deploy related type instance as an array of bytes.

    :param entity: A deploy related type instance to be encoded.
    :returns: An array of bytes.

    """
    try:
        encoder = _ENCODERS[type(entity)]
    except KeyError:
        raise ValueError(f"Unknown deploy type: {entity}")
    else:
        return encoder(entity)


def encode_semantic_version(entity: SemanticVersion) -> bytes:
    pass

