import json
import os
import pathlib
import typing

import pytest

import pycspr
from pycspr.types import CLTypeKey
from pycspr.serialisation import CL_VALUE_SERIALISERS


_PATH_TO_ASSETS = pathlib.Path(os.path.dirname(__file__)).parent / "assets"
_PATH_TO_VECTORS = _PATH_TO_ASSETS / "vectors"


@pytest.fixture(scope="session")
def cl_types() -> list:
    class _Accessor():
        def __init__(self):            
            self._fixtures = _read_vector("cl_types_complex.json") + \
                             _read_vector("cl_types_simple_numeric.json") + \
                             _read_vector("cl_types_simple_other.json")
            self._parse_fixtures()
            self.SIMPLE_TYPES = {
                CLTypeKey.I32,
                CLTypeKey.I64,
                CLTypeKey.U8,
                CLTypeKey.U32,
                CLTypeKey.U64,
                CLTypeKey.U128,
                CLTypeKey.U256,
                CLTypeKey.U512,
                CLTypeKey.BOOL,
                CLTypeKey.PUBLIC_KEY,
                CLTypeKey.STRING,
                CLTypeKey.UNIT,
            }

        def get_fixtures(self, typeof: str = None) -> list:
            if typeof is None:
                return self._fixtures
            typeof = typeof if isinstance(typeof, str) else typeof.name
            return [i for i in self._fixtures if i["typeof"] == typeof.upper()]


        def _parse_fixtures(self):
            for obj in self._fixtures:
                if obj["typeof"] == pycspr.types.CLTypeKey.UREF.name:
                    obj["value"] = pycspr.factory.create_uref_from_string(obj["value"])
                elif obj["typeof"] == pycspr.types.CLTypeKey.PUBLIC_KEY.name:     
                    obj["value"] = pycspr.factory.create_public_key_from_account_key(bytes.fromhex(obj["value"]))
    
    return _Accessor()


@pytest.fixture(scope="session")
def cl_values() -> list:
    class _Accessor():
        """Streamlines access to cl values vector.
        
        """
        def __init__(self):            
            self.fixtures = _read_vector("cl-values-simple.json")
            self._parse_fixtures()


        def _parse_fixtures(self):
            """Map input values to higher order domain types where appropriate.
            
            """
            for obj in self.fixtures:
                obj["cl_type"] = CLTypeKey[obj["cl_type"]]
            for obj in self.fixtures:
                    # if obj["cl_type"] == CLTypeKey.KEY:
                    #     obj["value"] = pycspr.factory.create_key_from_string(obj["value"])
                if obj["cl_type"] == CLTypeKey.LIST:
                    obj["value"] = pycspr.factory.create_list(
                        obj["value"], CLTypeKey[obj["cl_type_item"]]
                        )
                    print(obj["value"])
    
    return _Accessor()


@pytest.fixture(scope="session")
def crypto_1() -> list:
    data = _read_vector("crypto_hashes.json")
    for i in data:
        for j in i["hashes"]:
            j["digest"] = bytes.fromhex(j["digest"])

    return data


@pytest.fixture(scope="session")
def crypto_2() -> list:
    data = _read_vector("crypto_key_pairs.json")
    for i in data:
        i["pbk"] = bytes.fromhex(i["pbk"])
        i["pvk"] = bytes.fromhex(i["pvk"])
        i["accountKey"] = bytes.fromhex(i["accountKey"])
        i["accountHash"] = bytes.fromhex(i["accountHash"])

    return data


@pytest.fixture(scope="session")
def crypto_3() -> list:
    data = _read_vector("crypto_signatures.json")
    for i in data:
        i["key"]["pbk"] = bytes.fromhex(i["key"]["pbk"])
        i["key"]["pvk"] = bytes.fromhex(i["key"]["pvk"])
        i["sig"] = bytes.fromhex(i["sig"])

    return data


@pytest.fixture(scope="session")
def deploy_1() -> list:
    data = _read_vector("deploys_1.json")
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
