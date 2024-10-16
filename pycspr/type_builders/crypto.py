import pathlib

from pycspr.type_defs.crypto import \
    KeyAlgorithm, \
    PrivateKey, \
    PrivateKeyBytes, \
    PublicKey, \
    PublicKeyBytes
from pycspr.crypto import \
    get_key_pair_from_bytes, \
    get_key_pair_from_pem_file


class PrivateKey_Builder():
    def __init__(self):
        self.algo: KeyAlgorithm = None
        self.pbk: PublicKeyBytes = None
        self.pvk: PrivateKeyBytes = None

    def parse_pem_file(self, fpath: pathlib.Path):
        (pvk, pbk) = get_key_pair_from_pem_file(fpath, self.algo)
        self.set_private_key_bytes(pvk)
        self.set_public_key_bytes(pbk)
        return self

    def parse_private_key_bytes(self, pvk: PrivateKeyBytes):
        (pvk, pbk) = get_key_pair_from_bytes(pvk, self.algo)
        self.set_private_key_bytes(pvk)
        self.set_public_key_bytes(pbk)
        return self

    def set_algo(self, value: KeyAlgorithm):
        assert isinstance(value, KeyAlgorithm)
        self.algo = value
        return self

    def set_private_key_bytes(self, value: PrivateKeyBytes):
        assert isinstance(value, bytes) and len(value) == 32
        self.pvk = value
        return self

    def set_public_key_bytes(self, value: PublicKeyBytes):
        assert isinstance(value, bytes) and len(value) in (32, 33)
        self.pbk = value
        return self

    def build(self) -> PrivateKey:
        return PrivateKey(self.algo, self.pvk, self.pbk)


class PublicKey_Builder():
    def __init__(self):
        self.algo: KeyAlgorithm = None
        self.pbk: PublicKeyBytes = None

    def set_algo(self, value: KeyAlgorithm):
        assert isinstance(value, KeyAlgorithm)
        self.algo = value
        return self

    def set_key(self, value: PublicKeyBytes):
        assert isinstance(value, bytes) and len(value) in (32, 33)
        self.pbk = value
        return self

    def build(self) -> PublicKey:
        return PublicKey(self.algo, self.pbk)
