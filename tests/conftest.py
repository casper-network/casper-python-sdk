import datetime
import json
import operator
import os
import pathlib
import random
import typing

import pytest

import pycspr



_A_KNOWN_DEPLOY_TIMESTAMP = datetime.datetime.fromisoformat("2021-06-28T15:55:25.335+00:00").timestamp()
_A_KNOWN_DEPLOY_HUMANIZED_TTL = "1day"
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
    data = _get_vector("crypto_hashes.json")
    for i in data:
        for j in i["hashes"]:
            j["digest"] = bytes.fromhex(j["digest"])

    return data


@pytest.fixture(scope="session")
def vector_crypto_2() -> list:
    data = _get_vector("crypto_key_pairs.json")
    for i in data:
        i["pvk"] = bytes.fromhex(i["pvk"])
        i["pbk"] = bytes.fromhex(i["pbk"])
        i["accountKey"] = bytes.fromhex(i["accountKey"])
        i["accountHash"] = bytes.fromhex(i["accountHash"])

    return data


@pytest.fixture(scope="session")
def vector_crypto_3() -> list:
    data = _get_vector("crypto_signatures.json")
    for i in data:
        i["signingKey"]["pvk"] = bytes.fromhex(i["signingKey"]["pvk"])
        i["sig"] = bytes.fromhex(i["sig"])

    return data


@pytest.fixture(scope="session")
def vector_deploy_1() -> list:
    data = _get_vector("deploys_1.json")
    for i in data:
        i["bytes"]["payment"] = bytes.fromhex(i["bytes"]["payment"])
        i["bytes"]["session"] = bytes.fromhex(i["bytes"]["session"])
        i["hashes"]["body"] = bytes.fromhex(i["hashes"]["body"])
        i["hashes"]["deploy"] = bytes.fromhex(i["hashes"]["deploy"])
        i["session"]["target"] = bytes.fromhex(i["session"]["target"])

    return data


@pytest.fixture(scope="session")
def LIB() -> pycspr:
    """Returns pointer to configured library instance. 
    
    """
    return pycspr


@pytest.fixture(scope="session")
def CLIENT(LIB):
    """Returns pointer to a client pointing at NCTL:N1. 
    
    """    
    return LIB.NodeClient(LIB.NodeConnectionInfo(
        host="localhost",
        port_rest=14101,
        port_rpc=11101,
        port_sse=18101
    ))


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
    
    return FACTORY.create_private_key(algo, pvk, pbk)


@pytest.fixture(scope="session")
def a_test_chain_id() -> str:
    """Returns name of a test chain. 
    
    """
    return "casper-net-1"


@pytest.fixture(scope="session")
def a_test_timestamp() -> int:
    """Returns a test timestamp. 
    
    """
    return datetime.datetime.now(tz=datetime.timezone.utc).timestamp()


@pytest.fixture(scope="session")
def a_test_ttl_humanized() -> str:
    """Returns a humanized time interval. 
    
    """
    (unit, quantity) = random.choice((
        ("ms", random.randint(1, 1000 * 60 * 60 * 24)),
        ("s", random.randint(1, 60)),
        ("m", random.randint(1, 60)),
        ("h", random.randint(1, 24)),
        ("day", 1)
        ))

    return f"{quantity}{unit}"


@pytest.fixture(scope="session")
def test_account_1(LIB):
    """Returns test user account information. 
    
    """
    path = pathlib.Path(_PATH_TO_ACCOUNTS) / "account-1"  / "secret_key.pem"
    (pvk, pbk) = LIB.crypto.get_key_pair_from_pem_file(path)

    return LIB.types.PrivateKey(
        pbk=pbk,
        pvk=pvk,
        algo=LIB.crypto.KeyAlgorithm.ED25519
    )


def _get_account_of_nctl_faucet(LIB):
    """Returns account information related to NCTL faucet. 
    
    """
    path = _PATH_TO_NCTL_ASSETS / "net-1" / "faucet" / "secret_key.pem"

    return LIB.parse_private_key(path, LIB.crypto.KeyAlgorithm.ED25519)


def _get_account_of_nctl_user(LIB, user_id: int):
    """Returns account information related to NCTL user 1. 
    
    """
    path = _PATH_TO_NCTL_ASSETS / "net-1" / "users" / f"user-{user_id}" / "secret_key.pem"

    return LIB.parse_private_key(path, LIB.crypto.KeyAlgorithm.ED25519)


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
def deploy_params(FACTORY, a_test_chain_id, a_test_ttl_humanized, cp1):
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
            timestamp=datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            ttl=a_test_ttl_humanized
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
            ttl=FACTORY.create_deploy_ttl(_A_KNOWN_DEPLOY_HUMANIZED_TTL),
        )


@pytest.fixture(scope="session")
def key_pair_specs(LIB) -> typing.Tuple[pycspr.crypto.KeyAlgorithm, str, str]:
    """Returns sets of specifications for key pair generation. 
    
    """
    return (
        (LIB.crypto.KeyAlgorithm.ED25519, 32, 32),
        (LIB.crypto.KeyAlgorithm.SECP256K1, 32, 33),
    )


@pytest.fixture(scope="session")
def account_key() -> bytes:
    """Returns a test NCTL account key. 
    
    """
    path = pathlib.Path(os.getenv("NCTL"))
    path = path / "assets" / "net-1" / "users" / "user-1" / "public_key_hex"

    with open(path) as fstream:
        return bytes.fromhex(fstream.read())


@pytest.fixture(scope="session")
def account_hash(LIB, account_key: bytes) -> bytes:
    """Returns a test NCTL account key. 
    
    """
    return LIB.get_account_hash(account_key)


@pytest.fixture(scope="function")
def account_main_purse_uref(CLIENT, account_key: bytes, state_root_hash) -> str:
    """Returns a test account main purse unforgeable reference. 
    
    """
    return CLIENT.queries.get_account_main_purse_uref(account_key, state_root_hash)


@pytest.fixture(scope="function")
def state_root_hash(CLIENT) -> bytes:
    """Returns current state root hash @ NCTL Node 1. 
    
    """
    return CLIENT.queries.get_state_root_hash()


@pytest.fixture(scope="function")
def block_hash(CLIENT) -> str:
    """Returns hash of most recent block @ NCTL Node 1. 
    
    """
    return CLIENT.queries.get_block()["hash"]


@pytest.fixture(scope="session")
def switch_block(CLIENT) -> str:
    """Returns hash of most next switch. 
    
    """
    return CLIENT.queries.get_block_at_era_switch()


@pytest.fixture(scope="session")
def switch_block_hash(switch_block) -> str:
    """Returns hash of most next switch. 
    
    """
    return switch_block["hash"]


@pytest.fixture(scope="function")
def a_deploy(FACTORY, deploy_params, cp1, cp2):
    """Returns hash of most next switch. 
    
    """
    deploy = FACTORY.create_native_transfer(
        deploy_params,
        amount = 2500000000,
        correlation_id = 1,
        target = cp2.account_hash,
        )
    deploy.set_approval(FACTORY.create_deploy_approval(deploy, cp1))    

    return deploy

