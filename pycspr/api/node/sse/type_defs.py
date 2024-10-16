from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.api.node.sse.constants import \
    DEFAULT_HOST, \
    DEFAULT_PORT


@dataclasses.dataclass
class ConnectionInfo:
    """Encapsulates information required to connect to a node's SSE API.

    """
    # Host address.
    host: str = DEFAULT_HOST

    # Number of exposed speculative SSE port.
    port: int = DEFAULT_PORT

    def get_url(self, eid: int = 0) -> str:
        """Returns URL for remote SSE server connection.

        """
        url: str = f"http://{self.host}:{self.port}/events"
        if eid:
            url = f"{url}?start_from={eid}"

        return url


class EventType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.

    """
    All = enum.auto()
    ApiVersion = enum.auto()
    BlockAdded = enum.auto()
    Fault = enum.auto()
    FinalitySignature = enum.auto()
    Shutdown = enum.auto()
    Step = enum.auto()
    TransactionAccepted = enum.auto()
    TransactionsExpired = enum.auto()
    TransactionProcessed = enum.auto()


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
