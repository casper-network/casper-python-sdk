import datetime
import typing

from pycspr import crypto
from pycspr.types.account import AccountKeyInfo



def create_account_info(
    pbk: typing.Union[str, bytes],
    pvk: typing.Union[str, bytes],
    algo: typing.Union[str, crypto.KeyAlgorithm],
):
    if isinstance(pbk, str):
        pbk = bytes.fromhex(pbk)
    if isinstance(pvk, str):
        pvk = bytes.fromhex(pvk)
    if isinstance(algo, str):
        algo = crypto.KeyAlgorithm[algo]
    
    return AccountKeyInfo(pvk, pbk, algo)    
