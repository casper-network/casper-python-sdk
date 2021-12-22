import json
import os
import pathlib
import typing

import pytest

import pycspr
from pycspr.types import CL_TypeKey
from tests.fixtures.iterator_cl_types import yield_cl_types
from tests.fixtures.iterator_cl_values import yield_cl_values


_PATH_TO_ASSETS = pathlib.Path(os.path.dirname(__file__)).parent / "assets"
_PATH_TO_VECTORS = _PATH_TO_ASSETS / "vectors"


@pytest.fixture(scope="session")
def cl_types() -> list:
    class _Accessor():
        """Streamlines access to cl types vector.

        """
        def __init__(self):
            self.fixtures = _read_vector("cl-types.json")
            for obj in self.fixtures:
                obj["cl_type"] = CL_TypeKey[obj["cl_type"]]

        def __iter__(self):
            return yield_cl_types(self.fixtures)

    return _Accessor()


@pytest.fixture(scope="session")
def cl_values() -> list:
    class _Accessor():
        """Streamlines access to cl values vector.

        """
        def __init__(self):
            self.fixtures = _read_vector("cl-values.json")
            for obj in self.fixtures:
                obj["cl_type"] = CL_TypeKey[obj["cl_type"]]

        def __iter__(self):
            return yield_cl_values(self.fixtures)

    return _Accessor()


@pytest.fixture(scope="session")
def crypto_checksums() -> list:
    data = _read_vector("crypto-checksums.json")
    for i in data:
        i["input"] = bytes.fromhex(i["input"])

    return data


@pytest.fixture(scope="session")
def crypto_hashes() -> list:
    data = _read_vector("crypto-hashes.json")
    for i in data:
        for j in i["hashes"]:
            j["digest"] = bytes.fromhex(j["digest"])

    return data


@pytest.fixture(scope="session")
def crypto_key_pairs() -> list:
    data = _read_vector("crypto-key-pairs.json")
    for i in data:
        i["pbk"] = bytes.fromhex(i["pbk"])
        i["pvk"] = bytes.fromhex(i["pvk"])
        i["accountKey"] = bytes.fromhex(i["accountKey"])
        i["accountHash"] = bytes.fromhex(i["accountHash"])

    return data


@pytest.fixture(scope="session")
def crypto_key_pair_specs() -> typing.Tuple[pycspr.KeyAlgorithm, int, int]:
    """Returns sets of specifications for key pair generation.

    """
    return (
        (pycspr.KeyAlgorithm.ED25519, 32, 32),
        (pycspr.KeyAlgorithm.SECP256K1, 32, 33),
    )


@pytest.fixture(scope="session")
def crypto_signatures() -> list:
    data = _read_vector("crypto-signatures.json")
    for i in data:
        i["key"]["pbk"] = bytes.fromhex(i["key"]["pbk"])
        i["key"]["pvk"] = bytes.fromhex(i["key"]["pvk"])
        i["sig"] = bytes.fromhex(i["sig"])

    return data


@pytest.fixture(scope="session")
def deploys_1() -> list:
    data = _read_vector("deploys-1.json")
    for i in data:
        i["bytes"]["payment"] = bytes.fromhex(i["bytes"]["payment"])
        i["bytes"]["session"] = bytes.fromhex(i["bytes"]["session"])
        i["hashes"]["body"] = bytes.fromhex(i["hashes"]["body"])
        i["hashes"]["deploy"] = bytes.fromhex(i["hashes"]["deploy"])
        i["session"]["target"] = bytes.fromhex(i["session"]["target"])

    return data


def _read_vector(fname: str, parser: typing.Callable = json.load):
    with open(_PATH_TO_VECTORS / fname) as fstream:
        return fstream.read() if parser is None else parser(fstream)
