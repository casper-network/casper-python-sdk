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


# Map: SSE channel <-> SSE event.
SSE_CHANNEL_TO_SSE_EVENT: typing.Dict[NodeEventChannel, typing.Set[NodeEventType]] = {
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
