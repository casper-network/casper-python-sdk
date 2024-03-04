import enum
import os
import pathlib

import pycspr


_NAME_OF_CCTL_EVAR = "CCTL"

COUNT_OF_USERS = 10
COUNT_OF_VALDIATORS = 10


class AccountType(enum.Enum):
    FAUCET = enum.auto()
    USER = enum.auto()
    VALIDATOR = enum.auto()


class AsymmetricKeyType(enum.Enum):
    PRIVATE = enum.auto()
    PUBLIC = enum.auto()


KEY_FILE_NAME_BY_KEY_TYPE = {
    AsymmetricKeyType.PUBLIC: "public_key_hex",
    AsymmetricKeyType.PRIVATE: "secret_key.pem",
}

_cache = {
    "keys": {}
}


def get_evar():
    return os.getenv(_NAME_OF_CCTL_EVAR)


def get_path_to_assets() -> pathlib.Path:
    return pathlib.Path(get_evar()) / "assets"


def get_path_to_public_key_of_faucet() -> pathlib.Path:
    return _get_path_to_asymmetric_key(AsymmetricKeyType.PUBLIC, AccountType.FAUCET)


def get_path_to_private_key_of_faucet() -> pathlib.Path:
    return _get_path_to_asymmetric_key(AsymmetricKeyType.PRIVATE, AccountType.FAUCET)


def get_path_to_public_key_of_user(account_idx: int) -> pathlib.Path:
    return _get_path_to_asymmetric_key(AsymmetricKeyType.PUBLIC, AccountType.USER, account_idx)


def get_path_to_private_key_of_user(account_idx: int) -> pathlib.Path:
    return _get_path_to_asymmetric_key(AsymmetricKeyType.PRIVATE, AccountType.USER, account_idx)


def get_path_to_public_key_of_validator(account_idx: int) -> pathlib.Path:
    return _get_path_to_asymmetric_key(
        AsymmetricKeyType.PUBLIC,
        AccountType.VALIDATOR,
        account_idx
        )


def get_path_to_private_key_of_validator(account_idx: int) -> pathlib.Path:
    return _get_path_to_asymmetric_key(
        AsymmetricKeyType.PRIVATE,
        AccountType.VALIDATOR,
        account_idx
        )


def get_public_key_of_faucet() -> pycspr.PublicKey:
    return _get_asymmetric_key(AsymmetricKeyType.PUBLIC, AccountType.FAUCET, None)


def get_private_key_of_faucet() -> pycspr.PrivateKey:
    return _get_asymmetric_key(AsymmetricKeyType.PRIVATE, AccountType.FAUCET, None)


def get_public_key_of_user(account_idx: int) -> pycspr.PublicKey:
    return _get_asymmetric_key(AsymmetricKeyType.PUBLIC, AccountType.USER, account_idx)


def get_private_key_of_user(account_idx: int) -> pycspr.PrivateKey:
    return _get_asymmetric_key(AsymmetricKeyType.PRIVATE, AccountType.USER, account_idx)


def get_public_key_of_validator(account_idx: int) -> pycspr.PublicKey:
    return _get_asymmetric_key(AsymmetricKeyType.PUBLIC, AccountType.VALIDATOR, account_idx)


def get_private_key_of_validator(account_idx: int) -> pycspr.PrivateKey:
    return _get_asymmetric_key(AsymmetricKeyType.PRIVATE, AccountType.VALIDATOR, account_idx)


def _get_asymmetric_key(
    key_type: AsymmetricKeyType,
    account_type: AccountType,
    account_idx: None
) -> pathlib.Path:
    cache_key = f"{key_type}-{account_type}-{account_idx}"
    if cache_key not in _cache["keys"]:
        _cache["keys"][cache_key] = \
            _get_parsed_asymmetric_key(
                key_type,
                _get_path_to_asymmetric_key(key_type, account_type, account_idx)
                )

    return _cache["keys"][cache_key]


def _get_path_to_asymmetric_key(
    key_type: AsymmetricKeyType,
    account_type: AccountType,
    account_idx: None
) -> pathlib.Path:
    path = get_path_to_assets()
    if account_type == AccountType.FAUCET:
        path = path / "faucet"
    elif account_type == AccountType.USER:
        path = path / "users" / f"user-{account_idx}"
    elif account_type == AccountType.VALIDATOR:
        path = path / "nodes" / f"node-{account_idx}" / "keys"

    return path / KEY_FILE_NAME_BY_KEY_TYPE[key_type]


def _get_parsed_asymmetric_key(key_type: AsymmetricKeyType, path_to_key: pathlib.Path):
    return \
        pycspr.parse_private_key(path_to_key) \
        if key_type == AsymmetricKeyType.PRIVATE else \
        pycspr.parse_public_key(path_to_key)
