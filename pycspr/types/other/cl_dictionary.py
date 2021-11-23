import dataclasses


@dataclasses.dataclass
class CL_DictionaryIdentifier():
    """A set of variants for performation dictionary item state queries.

    """
    pass


@dataclasses.dataclass
class CL_DictionaryIdentifier_AccountNamedKey(CL_DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via an Account's named keys.

    """
    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    # The account key as a formatted string whose named keys contains dictionary_name.
    key: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.dictionary_name == other.dictionary_name and \
               self.key == other.key


@dataclasses.dataclass
class CL_DictionaryIdentifier_ContractNamedKey(CL_DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via a Contract's named keys.

    """
    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    # The contract key as a formatted string whose named keys contains dictionary_name.
    key: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.dictionary_name == other.dictionary_name and \
               self.key == other.key


@dataclasses.dataclass
class CL_DictionaryIdentifier_SeedURef(CL_DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item
       via it's seed unforgeable reference.

    """
    # The dictionary item key.
    dictionary_item_key: str

    # The dictionary's seed URef.
    seed_uref: lambda: object

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.seed_uref == other.seed_uref


@dataclasses.dataclass
class CL_DictionaryIdentifier_UniqueKey(CL_DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via it's unique key.

    """
    # The globally unique dictionary key.
    key: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.key == other.key
