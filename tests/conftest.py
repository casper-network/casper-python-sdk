import datetime
import json
import operator
import os
import pathlib
import typing

import pytest

import pycspr



_A_KNOWN_DEPLOY_TIMESTAMP = datetime.datetime.fromisoformat("2021-06-28T15:55:25.335+00:00").timestamp()
_PATH_TO_HERE = pathlib.Path(os.path.dirname(__file__))
_PATH_TO_ACCOUNTS = _PATH_TO_HERE / "assets" / "accounts"
_PATH_TO_VECTORS = _PATH_TO_HERE / "assets" / "vectors"
_PATH_TO_NCTL_ASSETS = pathlib.Path(os.getenv("NCTL")) / "assets"


def _get_vector(fname: str, parser: typing.Callable = json.load):
    with open(_PATH_TO_VECTORS / fname) as fhandle:
        return fhandle.read() if parser is None else parser(fhandle)


@pytest.fixture(scope="session")
def vector_cl_data_1() -> list:
    class _Accessor():
        def __init__(self):
            self.fixture = _get_vector("cl_types.json")
        
        def get_vectors(self, typeof: str) -> list:
            typeof = typeof if isinstance(typeof, str) else typeof.name
            return [i for i in self.fixture if i["typeof"] == typeof.upper()]

        def get_vector(self, typeof: str) -> dict:
            return self.get_vectors(typeof)[0]

        def get_value(self, typeof: str) -> object:
            return self.get_vector(typeof)["value"]

        def get_value_as_bytes(self, typeof: str) -> bytes:
            return bytes.fromhex(self.get_value(typeof))
    
    return _Accessor()


@pytest.fixture(scope="session")
def vector_crypto_1() -> list:
    return _get_vector("crypto_hashes.json")


@pytest.fixture(scope="session")
def vector_crypto_2() -> list:
    return _get_vector("crypto_key_pairs.json")


@pytest.fixture(scope="session")
def vector_crypto_3() -> list:
    return _get_vector("crypto_signatures.json")


@pytest.fixture(scope="session")
def vector_deploy_1() -> list:
    return _get_vector("deploys_1.json")


@pytest.fixture(scope="session")
def LIB() -> pycspr:
    """Returns pointer to configured library instance. 
    
    """
    # Initialise with default NCTL node 1 connection info.
    pycspr.initialise(pycspr.NodeConnectionInfo(
        host="localhost",
        port_rest=14101,
        port_rpc=11101,
        port_sse=18101
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
def a_test_account(FACTORY, vector_crypto_2):
    """Returns a test account key. 
    
    """
    algo, pbk, pvk = operator.itemgetter("algo", "pbk", "pvk")(vector_crypto_2[0])
    
    return FACTORY.create_account_info(algo, pvk, pbk)


@pytest.fixture(scope="session")
def a_test_chain_id() -> str:
    """Returns name of a test chain. 
    
    """
    return "casper-net-1"


@pytest.fixture(scope="session")
def a_test_timestamp() -> int:
    """Returns a test timestamp. 
    
    """
    return datetime.datetime.utcnow()


@pytest.fixture(scope="session")
def test_account_1(LIB):
    """Returns test user account information. 
    
    """
    path = pathlib.Path(_PATH_TO_ACCOUNTS) / "account-1"  / "secret_key.pem"
    (pvk, pbk) = LIB.crypto.get_key_pair_from_pem_file(path)

    return LIB.types.AccountInfo(
        pbk=pbk,
        pvk=pvk,
        algo=LIB.crypto.KeyAlgorithm.ED25519
    )


def _get_account_of_nctl_faucet(LIB):
    """Returns account information related to NCTL faucet. 
    
    """
    path = _PATH_TO_NCTL_ASSETS / "net-1" / "faucet" / "secret_key.pem"
    (pvk, pbk) = LIB.crypto.get_key_pair_from_pem_file(path)

    return LIB.types.AccountInfo(
        pbk=pbk,
        pvk=pvk,
        algo=LIB.crypto.KeyAlgorithm.ED25519
    )


def _get_account_of_nctl_user(LIB, user_id: int):
    """Returns account information related to NCTL user 1. 
    
    """
    path = _PATH_TO_NCTL_ASSETS / "net-1" / "users" / f"user-{user_id}" / "secret_key.pem"
    (pvk, pbk) = LIB.crypto.get_key_pair_from_pem_file(path)

    return LIB.types.AccountInfo(
        pbk=pbk,
        pvk=pvk,
        algo=LIB.crypto.KeyAlgorithm.ED25519
    )


@pytest.fixture(scope="session")
def cp1(LIB):
    """Returns counter-party 1 test account key. 
    
    """
    return _get_account_of_nctl_faucet(LIB)


@pytest.fixture(scope="session")
def cp2(LIB):
    """Returns counter-party 2 test account key. 
    
    """
    return _get_account_of_nctl_user(LIB, 1)


@pytest.fixture(scope="function")
def deploy_params(FACTORY, a_test_chain_id, cp1):
    """Returns standard deploy parameters with current timestamp. 
    
    """
    return FACTORY.create_deploy_parameters(
            account=FACTORY.create_public_key(
                cp1.algo,
                cp1.pbk
            ),
            chain_name=a_test_chain_id,
            dependencies=[],
            gas_price=10,
            timestamp=datetime.datetime.utcnow().timestamp(),
            ttl="1day"
        )


@pytest.fixture(scope="function")
def deploy_params_static(FACTORY, a_test_chain_id, test_account_1):
    """Returns standard deploy parameters with known timestamp. 
    
    """
    return FACTORY.create_deploy_parameters(
            account=FACTORY.create_public_key(
                test_account_1.algo,
                test_account_1.pbk
            ),
            chain_name=a_test_chain_id,
            dependencies=[],
            gas_price=10,
            timestamp=_A_KNOWN_DEPLOY_TIMESTAMP,
            ttl=FACTORY.create_deploy_ttl(
                "1day"
            ),
        )


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
    return LIB.get_block_at_era_switch()


@pytest.fixture(scope="session")
def switch_block_hash(switch_block) -> str:
    """Returns hash of most next switch. 
    
    """
    return switch_block["hash"]