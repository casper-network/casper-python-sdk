from pycspr.types import DictionaryIdentifier
from pycspr.types import DictionaryIdentifier_AccountNamedKey
from pycspr.types import DictionaryIdentifier_ContractNamedKey
from pycspr.types import DictionaryIdentifier_SeedURef
from pycspr.types import DictionaryIdentifier_UniqueKey



def encode_dictionary_identifier(entity: DictionaryIdentifier) -> dict:
    """Encodes a dictionary identifier used to issue a state query.

    """
    def _encode_account_named_key() -> dict:
        pass


    def _encode_contract_named_key() -> dict:
        pass


    def _encode_seed_uref() -> dict:
        pass


    def _encode_unique_key() -> dict:
        pass


    _ENCODERS = {
        DictionaryIdentifier_AccountNamedKey: _encode_account_named_key,
        DictionaryIdentifier_ContractNamedKey: _encode_contract_named_key,
        DictionaryIdentifier_SeedURef: _encode_seed_uref,
        DictionaryIdentifier_UniqueKey: _encode_unique_key,
    }

    return _ENCODERS[type(entity)]()
