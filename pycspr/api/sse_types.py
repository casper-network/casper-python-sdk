import dataclasses
import enum
import typing


class NodeEventChannel(enum.Enum):
    """Enumeration over set of exposed node SEE event types.

    """
    deploys = enum.auto()
    main = enum.auto()
    sigs = enum.auto()


class NodeEventType(enum.Enum):
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
class NodeEventInfo():
    """Encapsulates emitted event information.

    """
    # Channel over which event emitted by a node.
    channel: NodeEventChannel

    # Type of event emitted by a node.
    typeof: NodeEventType

    # Event ordinal identifier - acts as an offset.
    idx: int

    # Event payload ... typically data but sometimes a simple string.
    payload: typing.Union[dict, str]


# Map: SSE channel <-> SSE event.
SSE_CHANNEL_TO_SSE_EVENT = {
    NodeEventChannel.deploys: {
        NodeEventType.ApiVersion,
        NodeEventType.DeployAccepted
    },
    NodeEventChannel.main: {
        NodeEventType.ApiVersion,
        NodeEventType.BlockAdded,
        NodeEventType.DeployExpired,
        NodeEventType.DeployProcessed,
        NodeEventType.Fault,
        NodeEventType.Step
    },
    NodeEventChannel.sigs: {
        NodeEventType.ApiVersion,
        NodeEventType.FinalitySignature
    }
}
