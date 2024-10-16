from pycspr.crypto.hashifier import get_hash
from pycspr.crypto.cl_operations import get_account_address, get_account_key
from pycspr.type_builders.crypto import PublicKey_Builder
from pycspr.type_defs.chain import AccountAddressBytes
from pycspr.type_defs.crypto import KeyAlgorithm, PublicKey


class AccountAddress_Builder():
    def __init__(self):
        self.public_key: PublicKey = None

    def set_public_Key(self, value: PublicKey):
        assert isinstance(value, PublicKey)
        self.public_key = value
        return self

    def build(self) -> AccountAddressBytes:
        return get_account_address(
            get_account_key(
                self.public_key.algo,
                self.public_key.pbk
            )
        )
