import enum
import inspect



def _has_class(mod, cls):
    """Asserts that a container exposes a class.

    """
    _has_member(mod, cls)
    assert inspect.isclass(getattr(mod, cls)), '{} is not a class'.format(cls)


def _has_constant(mod, constant):
    """Asserts that a container exposes a constant.

    """
    _has_member(mod, constant)


def _has_enum(mod, enm):
    """Asserts that a container exposes an enumeration.

    """
    _has_member(mod, enm)
    assert issubclass(getattr(mod, enm), enum.Enum), '{} is not an enum'.format(enm)


def _has_exception(mod, err):
    """Asserts that a container exposes an exception.

    """
    _has_class(mod, err)
    assert issubclass(getattr(mod, err), Exception), \
           'Exception type does not inherit from builtin Exception class.'


def _has_function(mod, func):
    """Asserts that a container exposes a function.

    """
    _has_member(mod, func)
    assert inspect.isfunction(getattr(mod, func)), '{} is not a function'.format(func)


def _has_member(mod, member):
    """Asserts that a module exposes a member.

    """
    assert inspect.ismodule(mod)
    assert hasattr(mod, member), 'Missing member: {}'.format(member)


# Expected interface.
_INTERFACE_OF_LIBRARY = {
    _has_class: {
        "NodeClient",
        "NodeConnectionInfo",
    },
    _has_enum: {
        "NodeEventChannelType",
        "NodeEventType",
    },
    _has_constant: set(),
    _has_exception: set(),
    _has_function: {
        "create_deploy",
        "create_execution_arg",
        "create_standard_payment",
        "create_standard_transfer",
        "from_json",
        "to_bytes",
        "to_hex",
        "to_json",
        "get_account_hash",
        "get_account_key",
        "get_account_key_algo",
        "read_deploy",
        "write_deploy",
    },
    _has_member: {
        "crypto",
        "factory",
        "types",
    }
}


# Expected interface of factory methods.
_INTERFACE_OF_FACTORY = {
    _has_member: {
        "accounts",
        "cl",
        "deploys",
    },
}


def test_version_of_library(LIB):
    assert LIB.__version__ == "0.5.0"


def test_exports_of_library(LIB):
    for assertor, members in _INTERFACE_OF_LIBRARY.items():
        for member in members:
            assertor(LIB, member)


def test_exports_of_factory(LIB):
    _test_exports(LIB.factory, _INTERFACE_OF_FACTORY)


def _test_exports(module, interface):
    for assertor, members in interface.items():
        for member in members:
            assertor(module, member)
