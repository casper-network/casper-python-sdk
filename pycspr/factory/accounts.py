import typing

from pycspr import crypto
from pycspr.types import AccountInfo
from pycspr.types import PublicKey



def create_account_info(
    algo: typing.Union[str, crypto.KeyAlgorithm],
    pvk: typing.Union[str, bytes],
    pbk: typing.Union[str, bytes],
    ) -> AccountInfo:
    """Returns an approval by an account to the effect of authorizing deploy processing.
    
    :param algo: ECC key algorithm identifier.
    :param pvk: ECC private key.
    :param pbk: ECC public key.

    """
    if isinstance(pbk, str):
        pbk = bytes.fromhex(pbk)
    if isinstance(pvk, str):
        pvk = bytes.fromhex(pvk)
    if isinstance(algo, str):
        algo = crypto.KeyAlgorithm[algo]
    
    return AccountInfo(pvk, pbk, algo)    


def create_public_key(
    algo: typing.Union[str, crypto.KeyAlgorithm],
    bytes_raw: typing.Union[str, bytes],
    ) -> PublicKey:
    """Returns an account holder's public key.
    
    :param algo: ECC key algorithm identifier.
    :param bytes_raw: ECC public key raw bytes.

    """
    if isinstance(bytes_raw, str):
        bytes_raw = bytes.fromhex(bytes_raw)
    if isinstance(algo, str):
        algo = crypto.KeyAlgorithm[algo]
    
    return PublicKey(algo, bytes_raw)
