import typing

import pytest

from pycspr import crypto


@pytest.fixture(scope="session")
def key_pair_specs() -> typing.Tuple[crypto.KeyAlgorithm, str, str]:
    """Returns sets of specifications for key pair generation. 
 
    """
    return (
        (crypto.KeyAlgorithm.ED25519, 32, 32),
        (crypto.KeyAlgorithm.SECP256K1, 32, 33),
    )
