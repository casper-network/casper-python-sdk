import pathlib
import typing

from pycspr import crypto
from pycspr.types import PrivateKey
from pycspr.types import PublicKey



def create_private_key(algo: crypto.KeyAlgorithm, pvk: bytes, pbk: bytes) -> PrivateKey:
    """Returns an account holder's private key.
    
    :param algo: ECC key algorithm identifier.
    :param pvk: ECC private key.
    :param pbk: ECC public key.

    """
    if isinstance(algo, str):
        algo = crypto.KeyAlgorithm[algo]
    
    return PrivateKey(pvk, pbk, algo)   


def create_public_key(algo: crypto.KeyAlgorithm, pbk: bytes) -> PublicKey:
    """Returns an account holder's public key.
    
    :param algo: ECC key algorithm identifier.
    :param pbk: ECC public key raw bytes.

    """
    return PublicKey(algo, pbk)


def parse_private_key(fpath: pathlib.Path, algo: typing.Union[str, crypto.KeyAlgorithm]) -> PrivateKey:
    """Returns on-chain account information deserialised froma a secret key held on file system.
    
    :param fpath: Path to secret key pem file associated with the account.
    :param algo: ECC key algorithm identifier.
    :returns: On-chain account information wrapper.

    """
    algo = crypto.KeyAlgorithm[algo] if isinstance(algo, str) else algo
    (pvk, pbk) = crypto.get_key_pair_from_pem_file(fpath)

    return create_private_key(algo, pvk, pbk)


def parse_public_key(fpath: pathlib.Path) -> PublicKey:
    """Returns an account holder's public key.
    
    :param fpath: Path to public key hex file associated with the account.
    :returns: An account holder's public key.

    """
    with open(fpath) as fstream:
        account_key = bytes.fromhex(fstream.read())

    return create_public_key(
        crypto.KeyAlgorithm(account_key[0]),
        account_key[1:]
        )
