import dataclasses
import enum
import typing


@dataclasses.dataclass
class ExecutionResult:
    """Base class for execution results emitted by a node's execution engine upon execution of a deploy.

    """
	pass


@dataclasses.dataclass
class ExecutionResultFailure:
    """Encapsulates information emitted by a node's execution engine upon failed execution of a deploy.

    """
	pass


@dataclasses.dataclass
class ExecutionResultSuccess:
    """Encapsulates information emitted by a node's execution engine upon successful execution of a deploy.

    """
	pass


@dataclasses.dataclass
class OperationKind(enum.Enum):
    """Enumeration over set of execution engine operation types.

    """
    ADD = enum.auto()
    NOOP = enum.auto()
    READ = enum.auto()
    WRITE = enum.auto()


@dataclasses.dataclass
class Operation:
    """Encapsulates information pertaining to an operation performed by a node's execution engine during the course of executing a deploy.

    """
    # The formatted string of the operation 'Key'.
    key: str

	# The kind of operation being executed.
	kind: OperationKind


@dataclasses.dataclass
class Transform:
    pass


@dataclasses.dataclass
class Entry:
    # The formatted string of the key.
    key: str

    transform: Transform


@dataclasses.dataclass
class ExecutionEffect:
    """The side effect of executing a single deploy.

    """
    # Set of operations performed by execution engine during the course of executing a deploy.
    operations: typing.List[Operation]

    # Set of global state transformations committed by execution engine during the course of executing a deploy.
    transforms: typing.List[Operation]
