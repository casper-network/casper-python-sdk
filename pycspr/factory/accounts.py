from pycspr import crypto
from pycspr.types import AccountInfo
from pycspr.types import PublicKey



def create_account_info(algo: crypto.KeyAlgorithm, pvk: bytes, pbk: bytes) -> AccountInfo:
    """Returns on-chain account information.
    
    :param algo: ECC key algorithm identifier.
    :param pvk: ECC private key.
    :param pbk: ECC public key.

    """
    if isinstance(algo, str):
        algo = crypto.KeyAlgorithm[algo]
    
    return AccountInfo(pvk, pbk, algo)    


def create_public_key(algo: crypto.KeyAlgorithm, pbk: bytes) -> PublicKey:
    """Returns an account holder's public key.
    
    :param algo: ECC key algorithm identifier.
    :param pbk: ECC public key raw bytes.

    """
    return PublicKey(algo, pbk)
