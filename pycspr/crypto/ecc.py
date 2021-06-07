import base64
import tempfile
import typing

from pycspr.crypto import ecc_ed25519 as ed25519
from pycspr.crypto import ecc_secp256k1 as secp256k1
from pycspr.crypto.enums import KeyAlgorithm
from pycspr.crypto.enums import KeyEncoding
from pycspr.crypto.enums import SignatureEncoding



# Map: ECC Algo Type -> ECC Algo Implementation.
ALGOS = {
    KeyAlgorithm.ED25519: ed25519,
    KeyAlgorithm.SECP256K1: secp256k1,
}


def get_key_pair(
    algo: KeyAlgorithm = KeyAlgorithm.ED25519,
    encoding: KeyEncoding = KeyEncoding.BYTES
    ) -> typing.Union[typing.Tuple[bytes, bytes], typing.Tuple[str, str]]:
    """Returns an ECC key pair, each key is a 32 byte array.

    :param algo: Type of ECC algo to be used when generating key pair.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    pvk, pbk = ALGOS[algo].get_key_pair()

    return (pvk.hex(), pbk.hex()) if encoding == KeyEncoding.HEX else (pvk, pbk)


def get_key_pair_from_bytes(
    pvk: bytes,
    algo: KeyAlgorithm = KeyAlgorithm.ED25519,
    encoding: KeyEncoding = KeyEncoding.BYTES
    ) -> typing.Union[typing.Tuple[bytes, bytes], typing.Tuple[str, str]]:
    """Returns a key pair mapped from a byte array representation of a private key.

    :param pvk_b64: Base64 encoded private key.
    :param algo: Type of ECC algo used to generate private key.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    pvk, pbk = ALGOS[algo].get_key_pair(pvk)

    return (pvk.hex(), pbk.hex()) if encoding == KeyEncoding.HEX else (pvk, pbk)


def get_key_pair_from_base64(
    pvk_b64: str,
    algo: KeyAlgorithm = KeyAlgorithm.ED25519,
    encoding: KeyEncoding = KeyEncoding.BYTES
    ) -> typing.Union[typing.Tuple[bytes, bytes], typing.Tuple[str, str]]:
    """Returns a key pair mapped from a base 64 representation of a private key.

    :param pvk_b64: Base64 encoded private key.
    :param algo: Type of ECC algo used to generate private key.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    return get_key_pair_from_bytes(base64.b64decode(pvk_b64), algo, encoding)


def get_key_pair_from_hex_string(
    pvk_hex: str,
    algo: KeyAlgorithm = KeyAlgorithm.ED25519,
    encoding: KeyEncoding = KeyEncoding.BYTES
    ) -> typing.Union[typing.Tuple[bytes, bytes], typing.Tuple[str, str]]:
    """Returns an ECC key pair derived from a hexadecimal string encoded private key.

    :param pvk_hex: Hexadecimal string encoded private key.
    :param algo: Type of ECC algo used to generate private key.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    return get_key_pair_from_bytes(bytes.fromhex(pvk_hex), algo, encoding)


def get_key_pair_from_pem_file(
    fpath: str,
    algo: KeyAlgorithm = KeyAlgorithm.ED25519,
    encoding: KeyEncoding = KeyEncoding.BYTES
    ) -> typing.Union[typing.Tuple[bytes, bytes], typing.Tuple[str, str]]:
    """Returns an ECC key pair derived from a previously persisted PEM file.

    :param fpath: PEM file path.
    :param algo: Type of ECC algo used to generate private key.
    :param encoding: Key pair encoding type.

    :returns : 2 member tuple: (private key, public key)
    
    """
    pvk, pbk = ALGOS[algo].get_key_pair_from_pem_file(fpath)

    return (pvk.hex(), pbk.hex()) if encoding == KeyEncoding.HEX else (pvk, pbk)


def get_pvk_pem_from_bytes(pvk: bytes, algo: KeyAlgorithm = KeyAlgorithm.ED25519) -> bytes:
    """Returns an ECC private key in PEM format.

    :param pvk: Private key.
    :param algo: Type of ECC algo used to generate private key.

    :returns : Private key in PEM format.
    
    """
    return ALGOS[algo].get_pvk_pem_from_bytes(pvk)


def get_pvk_pem_from_hex_string(pvk: str, algo: KeyAlgorithm = KeyAlgorithm.ED25519) -> bytes:
    """Returns an ECC private key mapped from a private key encoded as a hexadecial string.

    :param pvk: Private key.
    :param algo: Type of ECC algo used to generate private key.

    :returns : Private key in PEM format.
    
    """
    return ALGOS[algo].get_pvk_pem_from_bytes(pvk)


def get_pvk_pem_file_from_bytes(pvk: bytes, algo: KeyAlgorithm = KeyAlgorithm.ED25519) -> bytes:
    """Returns path to a file containing an ECC private key in PEM format.

    :param pvk: Private key.
    :param algo: Type of ECC algo used to generate private key.

    :returns : Private key in PEM format.
    
    """
    with tempfile.NamedTemporaryFile("wb", delete=False) as temp_file:
        with open(temp_file.name, "wb") as fstream:
            fstream.write(get_pvk_pem_from_bytes(pvk, algo))

        return temp_file.name


# Map: signature encoding <-> encoder.
_SIGNATURE_ENCODERS = {
    SignatureEncoding.BYTES: lambda x: x,
    SignatureEncoding.HEX: lambda x: x.hex(),
}


def get_signature(
    data: bytes,
    pvk: bytes,
    algo: KeyAlgorithm = KeyAlgorithm.ED25519,
    encoding: SignatureEncoding = SignatureEncoding.BYTES
    ) -> bytes:
    """Returns an ED25519 digital signature of data signed from a PEM file representation of a private key.

    :param data: Data to be signed.
    :param pvk: Secret key.
    :param algo: Type of ECC algo used to generate secret key.
    :param encoding: Signature encoding type.

    :returns: Digital signature of input data.
    
    """
    return _SIGNATURE_ENCODERS[encoding](
        ALGOS[algo].get_signature(data, pvk)
        )


def get_signature_from_pem_file(
    data: bytes,
    fpath: str,
    algo: KeyAlgorithm = KeyAlgorithm.ED25519,
    encoding: SignatureEncoding = SignatureEncoding.BYTES
    ) -> bytes:
    """Returns an ED25519 digital signature of data signed from a PEM file representation of a private key.
    
    """
    pvk, _ = get_key_pair_from_pem_file(fpath, algo)

    return get_signature(data, pvk, algo, encoding)
