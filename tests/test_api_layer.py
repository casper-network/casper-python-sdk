from pycspr.types import DictionaryIdentifier_AccountNamedKey
from pycspr.api import NodeAPIError


def test_get_dictionary_item(CLIENT, account_key: bytes):
    """ test if we get a node response. """
    # @TODO: wrong params, what values can we use for testing local and remote?
    try:
        identifier = DictionaryIdentifier_AccountNamedKey("wrong_dictkey",
                                                          "wrong_dictname",
                                                          account_key.hex())
        _ = CLIENT.queries.get_dictionary_item(identifier)
    except Exception as e:
        assert isinstance(e, NodeAPIError)
