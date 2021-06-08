import typing

from pycspr import crypto
from pycspr.types.account import AccountInfo



def create_account_info(
    algo: typing.Union[str, crypto.KeyAlgorithm],
    pvk: typing.Union[str, bytes],
    pbk: typing.Union[str, bytes],
    ):
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
