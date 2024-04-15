from pycspr.types.crypto import KeyAlgorithm
from pycspr.types.crypto import DigestBytes
from pycspr.types.crypto import DigestHex
from pycspr.types.crypto import MerkleProofBytes
from pycspr.types.crypto import MerkleProofHex
from pycspr.types.crypto import PublicKey
from pycspr.types.crypto import PublicKeyBytes
from pycspr.types.crypto import PublicKeyHex
from pycspr.types.crypto import PrivateKey
from pycspr.types.crypto import PrivateKeyBytes
from pycspr.types.crypto import PrivateKeyHex
from pycspr.types.crypto import SignatureBytes
from pycspr.types.crypto import SignatureHex
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
        decoder = DECODERS[typedef]
    except KeyError:
        raise ValueError(f"Cannot decode {typedef} from json")
    else:
        return decoder(encoded)


def _decode_public_key(encoded: PublicKeyBytes) -> PublicKey:
    return PublicKey(
        algo=KeyAlgorithm(encoded[0]),
        pbk=encoded[1:]
    )


def _decode_private_key(encoded: PrivateKeyBytes) -> PrivateKey:
    raise NotImplementedError("_decode_private_key")


DECODERS = {
    DigestBytes: lambda x: x,
    DigestHex: lambda x: decode(DigestBytes, bytes.fromhex(x)),
    MerkleProofBytes: lambda x: x,
    MerkleProofHex: lambda x: decode(MerkleProofBytes, bytes.fromhex(x)),
    PublicKey: _decode_public_key,
    PublicKeyBytes: lambda x: decode(PublicKey, x),
    PublicKeyHex: lambda x: decode(PublicKeyBytes, bytes.fromhex(x)),
    PrivateKey: _decode_private_key,
    PrivateKeyBytes: lambda x: decode(PrivateKey, x),
    PrivateKeyHex: lambda x: decode(PrivateKeyBytes, bytes.fromhex(x)),
    SignatureBytes: lambda x: x,
    SignatureHex: lambda x: decode(SignatureBytes, bytes.fromhex(x)),
}
