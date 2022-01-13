import operator
import os
import pathlib

import pytest

import pycspr


_PATH_TO_ASSETS = pathlib.Path(os.path.dirname(__file__)).parent / "assets"
_PATH_TO_ACCOUNTS = _PATH_TO_ASSETS / "accounts"
_PATH_TO_NCTL_ASSETS = pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1"


@pytest.fixture(scope="session")
def a_test_account(crypto_key_pairs) -> pycspr.types.PrivateKey:
    """Returns a test account key.

    """
    algo, pbk, pvk = operator.itemgetter("algo", "pbk", "pvk")(crypto_key_pairs[0])

    return pycspr.factory.create_private_key(algo, pvk, pbk)


@pytest.fixture(scope="session")
def test_account_1():
    """Returns test user account information.

    """
    path = _PATH_TO_ACCOUNTS / "account-1"  / "secret_key.pem"
    (pvk, pbk) = pycspr.crypto.get_key_pair_from_pem_file(path)

    return pycspr.types.PrivateKey(
        pbk=pbk,
        pvk=pvk,
        algo=pycspr.crypto.KeyAlgorithm.ED25519
    )


@pytest.fixture(scope="session")
def test_account_2():
    """Returns test user account information.

    """
    path = _PATH_TO_ACCOUNTS / "account-2"  / "secret_key.pem"
    (pvk, pbk) = pycspr.crypto.get_key_pair_from_pem_file(path)

    return pycspr.types.PrivateKey(
        pbk=pbk,
        pvk=pvk,
        algo=pycspr.crypto.KeyAlgorithm.SECP256K1
    )


@pytest.fixture(scope="session")
def cp1():
    """Returns counter-party 1 test account key.

    """
    return get_account_of_nctl_faucet()


@pytest.fixture(scope="session")
def cp2():
    """Returns counter-party 2 test account key.

    """
    return get_account_of_nctl_user(1)


@pytest.fixture(scope="session")
def account_key() -> bytes:
    """Returns a test NCTL account key.

    """
    path = _PATH_TO_NCTL_ASSETS / "users" / "user-1" / "public_key_hex"

    with open(path) as fstream:
        return bytes.fromhex(fstream.read())


@pytest.fixture(scope="session")
def account_hash(account_key: bytes) -> bytes:
    """Returns a test NCTL account key.

    """
    return pycspr.get_account_hash(account_key)


def get_account_of_nctl_faucet():
    """Returns account information related to NCTL faucet.

    """
    path = _PATH_TO_NCTL_ASSETS / "faucet" / "secret_key.pem"

    return pycspr.parse_private_key(path, pycspr.crypto.KeyAlgorithm.ED25519)


def get_account_of_nctl_user(user_id: int):
    """Returns account information related to NCTL user 1.

    """
    path = _PATH_TO_NCTL_ASSETS / "users" / f"user-{user_id}" / "secret_key.pem"

    return pycspr.parse_private_key(path, pycspr.crypto.KeyAlgorithm.ED25519)


def create_account():
    """Returns a test account.
    
    """
    algo = pycspr.crypto.DEFAULT_KEY_ALGO
    pvk, pbk = pycspr.crypto.get_key_pair(algo)

    return pycspr.factory.create_private_key(algo, pvk, pbk)
