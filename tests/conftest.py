import json
import operator
import os
import pathlib
import random
import typing

import pytest

import pycspr


# Path to test vectors.
_VECTORS = pathlib.Path(os.path.dirname(__file__)) / "vectors"


def _get_vector(fname: str, parser: typing.Callable = None):
    """Returns contents of a test vector.
    
    """
    with open(_VECTORS / fname) as fhandle:
        return fhandle.read() if parser is None else parser(fhandle)
        

class VectorSet1_Accessor():
    """Vector 1 access simplifier.
    
    """
    def __init__(self):
        self.fixture = _get_vector("for_data_tests.json", json.load)
    
    def get_vectors(self, typeof: str) -> list:
        typeof = typeof if isinstance(typeof, str) else typeof.name
        return [i for i in self.fixture if i["typeof"] == typeof.upper()]

    def get_vector(self, typeof: str) -> dict:
        return self.get_vectors(typeof)[0]

    def get_value(self, typeof: str) -> object:
        return self.get_vector(typeof)["value"]

    def get_value_as_bytes(self, typeof: str) -> bytes:
        return bytes.fromhex(self.get_value(typeof))


@pytest.fixture(scope="session")
def vectors_1() -> list:
    """Returns a set of fixtures for use as input to upstream data tests. 
    
    """
    return VectorSet1_Accessor()


@pytest.fixture(scope="session")
def vectors_2() -> list:
    """Returns a set of fixtures for use as input to upstream hashing tests. 
    
    """
    return _get_vector("for_hash_tests.json", json.load)


@pytest.fixture(scope="session")
def vectors_3() -> list:
    """Returns a set of fixtures for use as input to upstream key-pair tests. 
    
    """
    return _get_vector("for_key_pair_tests.json", json.load)


@pytest.fixture(scope="session")
def fixtures_for_public_key_tests() -> list:
    """Returns a set of fixtures for use as input to upstream key tests. 
    
    """
    return _get_vector("for_public_key_tests.json", json.load)


@pytest.fixture(scope="session")
def vectors_4() -> list:
    """Returns a set of fixtures for use as input to upstream signature tests. 
    
    """
    return _get_vector("for_signature_tests.json", json.load)


@pytest.fixture(scope="session")
def LIB() -> pycspr:
    """Returns pointer to configured library instance. 
    
    """
    # Initialise with default NCTL node 1 connection info.
    pycspr.initialise(pycspr.NodeConnectionInfo(
        host="localhost",
        port_rest=50101,
        port_rpc=40101,
        port_sse=60101
    ))

    return pycspr


@pytest.fixture(scope="session")
def FACTORY(LIB):
    """Returns pointer to the library's type factory. 
    
    """    
    return LIB.factory


@pytest.fixture(scope="session")
def TYPES(LIB):
    """Returns pointer to the library's typeset. 
    
    """  
    return LIB.types


@pytest.fixture(scope="session")
def a_test_account(FACTORY, vectors_3) -> pycspr.types.AccountKeyInfo:
    """Returns a test account key. 
    
    """
    algo, pbk, pvk = operator.itemgetter("algo", "pbk", "pvk")(vectors_3[0])
    
    return FACTORY.accounts.create_account_info(pbk, pvk, algo)


@pytest.fixture(scope="session")
def a_test_chain_id() -> str:
    """Returns name of a test chain. 
    
    """
    return "casper-net-1"


def _get_account_info_of_nctl_user(LIB, user_id: int) -> pycspr.types.AccountKeyInfo:
    """Returns account information related to NCTL user 1. 
    
    """
    path = pathlib.Path(os.getenv("NCTL"))
    path = path / "assets" / "net-1" / "users" / f"user-{user_id}" / "secret_key.pem"
    (pvk, pbk) = LIB.crypto.get_key_pair_from_pem_file(path)

    return LIB.types.AccountKeyInfo(
        pbk=pbk,
        pvk=pvk,
        algo=LIB.crypto.KeyAlgorithm.ED25519
    )


@pytest.fixture(scope="session")
def cp1(LIB) -> pycspr.types.AccountKeyInfo:
    """Returns a test account key. 
    
    """
    return _get_account_info_of_nctl_user(LIB, 1)


@pytest.fixture(scope="session")
def cp2(LIB) -> pycspr.types.AccountKeyInfo:
    """Returns a test account key. 
    
    """
    return _get_account_info_of_nctl_user(LIB, 2)


@pytest.fixture(scope="session")
def key_pair_specs(LIB) -> typing.Tuple[pycspr.crypto.KeyAlgorithm, str, str]:
    """Returns sets of specifications for key pair generation. 
    
    """
    return (
        (
            LIB.crypto.KeyAlgorithm.ED25519,
            LIB.crypto.KeyEncoding.BYTES,
            bytes,
            32,
            32,
        ),
        (
            LIB.crypto.KeyAlgorithm.ED25519,
            LIB.crypto.KeyEncoding.HEX,
            str,
            64,
            64,
        ),
        (
            LIB.crypto.KeyAlgorithm.SECP256K1,
            LIB.crypto.KeyEncoding.BYTES,
            bytes,
            32,
            33,
        ),
        (
            LIB.crypto.KeyAlgorithm.SECP256K1,
            LIB.crypto.KeyEncoding.HEX,
            str,
            64,
            66,
        ),
    )


@pytest.fixture(scope="session")
def account_key() -> str:
    """Returns a test NCTL account key. 
    
    """
    path = pathlib.Path(os.getenv("NCTL"))
    path = path / "assets" / "net-1" / "users" / "user-1" / "public_key_hex"

    with open(path) as fstream:
        return fstream.read()


@pytest.fixture(scope="function")
def account_main_purse_uref(LIB, account_key, state_root_hash) -> str:
    """Returns a test account main purse unforgeable reference. 
    
    """
    return LIB.get_account_main_purse_uref(account_key, state_root_hash)


@pytest.fixture(scope="function")
def state_root_hash(LIB) -> str:
    """Returns current state root hash @ NCTL Node 1. 
    
    """
    return LIB.get_state_root_hash()


@pytest.fixture(scope="function")
def block_hash(LIB) -> str:
    """Returns hash of most recent block @ NCTL Node 1. 
    
    """
    return LIB.get_block()["hash"]


@pytest.fixture(scope="session")
def switch_block(LIB) -> str:
    """Returns hash of most next switch. 
    
    """
    return LIB.get_switch_block()


@pytest.fixture(scope="session")
def switch_block_hash(switch_block) -> str:
    """Returns hash of most next switch. 
    
    """
    return switch_block["hash"]
