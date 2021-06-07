import dataclasses

from pycspr import crypto



@dataclasses.dataclass
class AccountKeyInfo:
    """Encapsulates information associated with an external account.
    
    """
    # Private key as bytes - sensitive material !
    pvk: bytes

    # Public key as bytes.
    pbk: bytes

    # Algorithm used to generate ECC key pair.
    algo: crypto.KeyAlgorithm = crypto.KeyAlgorithm.ED25519


    @property
    def private_key(self):
        """Property synonym."""
        return self.pvk


    @property
    def public_key(self):
        """Property synonym."""
        return self.pbk


    @property
    def account_key(self):
        """Returns on-chain account key.

        """ 
        return crypto.get_account_key(self.algo, self.pbk.hex())


    @property
    def address(self):
        """Returns on-chain account address.

        """ 
        return crypto.get_account_hash(self.account_key)


    def get_signature(self, data: bytes) -> bytes:
        """Get signature over payload.
        
        """
        return crypto.get_signature(data, self.pvk, self.algo)
