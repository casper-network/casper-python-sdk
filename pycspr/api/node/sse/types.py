from __future__ import annotations

import dataclasses
import enum
import typing


class EventType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.

    """
    ApiVersion = enum.auto()
    BlockAdded = enum.auto()
    DeployAccepted = enum.auto()
    DeployProcessed = enum.auto()
    DeployExpired = enum.auto()
    Fault = enum.auto()
    FinalitySignature = enum.auto()
    Shutdown = enum.auto()
    Step = enum.auto()


@dataclasses.dataclass
class EventInfo():
    """Encapsulates emitted event information.

    """
    # Type of event emitted by a node.
    typeof: EventType

    # Event ordinal identifier - acts as an offset.
    idx: int

    # Event payload ... typically data but sometimes a simple string.
    payload: typing.Union[dict, str]
