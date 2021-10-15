import enum


class TypeTag_ExecutableDeployItem(enum.Enum):
    """Enumeration over set of type tags for executable deploy items.

    """
    ModuleBytes = 0
    StoredContractByHash = 1
    StoredContractByHashVersioned = 2
    StoredContractByName = 3
    StoredContractByNameVersioned = 4
    Transfer = 5


class TypeTag_StorageKey(enum.Enum):
    """Enumeration over set of type tags for global state keys.

    """
    Account = 0
    Hash = 1
    URef = 2
