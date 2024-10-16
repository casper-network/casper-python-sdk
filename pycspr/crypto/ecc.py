import base64
import tempfile
import typing

from pycspr.crypto import ecc_ed25519 as ed25519
from pycspr.crypto import ecc_secp256k1 as secp256k1
from pycspr.type_defs.crypto import DigestBytes
from pycspr.type_defs.crypto import KeyAlgorithm
from pycspr.type_defs.crypto import PrivateKeyBase64
from pycspr.type_defs.crypto import PrivateKeyBytes
from pycspr.type_defs.crypto import PrivateKeyHex
from pycspr.type_defs.crypto import PrivateKeyPem
from pycspr.type_defs.crypto import PublicKeyBytes
from pycspr.type_defs.crypto import SignatureBytes


# Map: Key algo Type -> Key algo Implementation.
ALGOS = {
    KeyAlgorithm.ED25519: ed25519,
    KeyAlgorithm.SECP256K1: secp256k1,
}

# Default key algorithm.
DEFAULT_KEY_ALGO = KeyAlgorithm.ED25519


def get_key_pair(
    algo: KeyAlgorithm = DEFAULT_KEY_ALGO
) -> typing.Tuple[PrivateKeyBytes, PublicKeyBytes]:
    """Returns an ECC key pair, each key is a 32 byte array.

    :param algo: Type of ECC algo to be used when generating key pair.
    :returns : 2 member tuple: (private key, public key)

    """
    pvk, pbk = ALGOS[algo].get_key_pair()

    return (pvk, pbk)


def get_key_pair_from_bytes(
    pvk: PrivateKeyBytes,
    algo: KeyAlgorithm = DEFAULT_KEY_ALGO
) -> typing.Tuple[PrivateKeyBytes, PublicKeyBytes]:
    """Returns a key pair mapped from a byte array representation of a private key.

    :param pvk: A private key.
    :param algo: Type of ECC algo used to generate private key.
    :returns : 2 member tuple: (private key, public key)

    """
    pvk, pbk = ALGOS[algo].get_key_pair(pvk)

    return (pvk, pbk)


def get_key_pair_from_base64(
    pvk_b64: PrivateKeyBase64,
    algo: KeyAlgorithm = DEFAULT_KEY_ALGO
) -> typing.Tuple[PrivateKeyBytes, PublicKeyBytes]:
    """Returns a key pair mapped from a base 64 representation of a private key.

    :param pvk_b64: Base64 encoded private key.
    :param algo: Type of ECC algo used to generate private key.
    :returns : 2 member tuple: (private key, public key)

    """
    return get_key_pair_from_bytes(base64.b64decode(pvk_b64), algo)


def get_key_pair_from_hex_string(
    pvk_hex: PrivateKeyHex,
    algo: KeyAlgorithm = DEFAULT_KEY_ALGO
) -> typing.Tuple[PrivateKeyBytes, PublicKeyBytes]:
    """Returns an ECC key pair derived from a hexadecimal string encoded private key.

    :param pvk_hex: Hexadecimal string encoded private key.
    :param algo: Type of ECC algo used to generate private key.
    :returns : 2 member tuple: (private key, public key)

    """
    return get_key_pair_from_bytes(bytes.fromhex(pvk_hex), algo)


def get_key_pair_from_pem_file(
    fpath: str,
    algo: KeyAlgorithm = DEFAULT_KEY_ALGO
) -> typing.Tuple[PrivateKeyBytes, PublicKeyBytes]:
    """Returns an ECC key pair derived from a previously persisted PEM file.

    :param fpath: PEM file path.
    :param algo: Type of ECC algo used to generate private key.
    :returns : 2 member tuple: (private key, public key)

    """
    pvk, pbk = ALGOS[algo].get_key_pair_from_pem_file(fpath)

    return (pvk, pbk)


def get_pvk_pem_from_bytes(
    pvk: PrivateKeyBytes,
    algo: KeyAlgorithm = DEFAULT_KEY_ALGO
) -> PrivateKeyPem:
    """Returns an ECC private key in PEM format.

    :param pvk: Private key.
    :param algo: Type of ECC algo used to generate private key.
    :returns : Private key in PEM format.

    """
    return ALGOS[algo].get_pvk_pem_from_bytes(pvk)


def get_pvk_pem_from_hex_string(
    pvk: PrivateKeyHex,
    algo: KeyAlgorithm = DEFAULT_KEY_ALGO
) -> PrivateKeyPem:
    """Returns an ECC private key mapped from a private key encoded as a hexadecial string.

    :param pvk: Private key.
    :param algo: Type of ECC algo used to generate private key.
    :returns : Private key in PEM format.

    """
    return ALGOS[algo].get_pvk_pem_from_bytes(pvk)


def get_pvk_pem_file_from_bytes(
    pvk: PrivateKeyBytes,
    algo: KeyAlgorithm = DEFAULT_KEY_ALGO
) -> PrivateKeyPem:
    """Returns path to a file containing an ECC private key in PEM format.

    :param pvk: Private key.
    :param algo: Type of ECC algo used to generate private key.

    :returns : Private key in PEM format.

    """
    with tempfile.NamedTemporaryFile("wb", delete=False) as temp_file:
        with open(temp_file.name, "wb") as fstream:
            fstream.write(get_pvk_pem_from_bytes(pvk, algo))

        return temp_file.name


def get_signature(
    msg_hash: DigestBytes,
    algo: KeyAlgorithm,
    pvk: PrivateKeyBytes,
) -> SignatureBytes:
    """Returns digital signature of data signed by a private key.

    :param msg_hash: Message hash to be signed.
    :param pvk: Secret key.
    :param algo: Type of ECC algo used to generate secret key.
    :returns: Digital signature of massage hash.

    """
    return ALGOS[algo].get_signature(msg_hash, pvk)


def get_signature_from_pem_file(
    msg_hash: DigestBytes,
    fpath: str,
    algo: KeyAlgorithm = DEFAULT_KEY_ALGO
) -> SignatureBytes:
    """Returns an ED25519 digital signature of data signed from a private key PEM file.

    :param msg_hash: Message hash to be signed.
    :param fpath: Path to a PEM file representation of a signing key.
    :param algo: Type of ECC algo used to generate secret key.
    :returns: Digital signature of massage hash.

    """
    pvk, _ = get_key_pair_from_pem_file(fpath, algo)

    return get_signature(msg_hash, algo, pvk)


def is_signature_valid(
    msg_hash: DigestBytes,
    algo: KeyAlgorithm,
    sig: SignatureBytes,
    vk: PublicKeyBytes
) -> bool:
    """Returns a flag indicating whether a signature was signed by a signing key.

    :param msg_hash: Previously signed message hash.
    :param sig: A digital signature.
    :param vk: Verifying key.
    :param algo: Type of ECC algo used to generate signing key.
    :returns: A flag indicating whether a signature was signed by a signing key.

    """
    return ALGOS[algo].is_signature_valid(msg_hash, sig, vk)


# Synonym.
get_key_pair_from_seed = get_key_pair_from_bytes
