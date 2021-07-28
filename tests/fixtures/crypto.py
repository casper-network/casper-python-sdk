import typing

import pytest

import pycspr



@pytest.fixture(scope="session")
def key_pair_specs() -> typing.Tuple[pycspr.KeyAlgorithm, str, str]:
    """Returns sets of specifications for key pair generation. 
    
    """
    return (
        (pycspr.KeyAlgorithm.ED25519, 32, 32),
        (pycspr.KeyAlgorithm.SECP256K1, 32, 33),
    )
