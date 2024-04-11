from pycspr.types.crypto import KeyAlgorithm
from pycspr.types.crypto import PublicKey
from pycspr.types.crypto import PublicKeyBytes
from pycspr.types.crypto import PublicKeyHex
from pycspr.types.crypto import TYPESET


def decode(typedef: object, encoded: dict) -> object:
    """Decoder: Domain entity <- JSON blob.

    :param encoded: A JSON compatible dictionary.
    :param typedef: Deploy related type definition.
    :returns: A deploy related type.

    """
    if typedef not in TYPESET:
        raise ValueError("Unsupported type")

    try:
        decoder = _DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json")
    else:
        return decoder(encoded)


def _decode_public_key(encoded: PublicKeyHex) -> PublicKey:
    as_bytes: PublicKeyBytes = bytes.fromhex(encoded)

    return PublicKey(
        algo=KeyAlgorithm(as_bytes[0]),
        pbk=as_bytes[1:]
    )


_DECODERS = {
    PublicKey: _decode_public_key,
}
