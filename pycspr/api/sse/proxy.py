import dataclasses
import json
import typing

import requests
import sseclient

from pycspr.api import constants
from pycspr.api.sse.types import NodeEventChannel
from pycspr.api.sse.types import NodeEventInfo
from pycspr.api.sse.types import NodeEventType


@dataclasses.dataclass
class Proxy:
    """Node SSE server proxy.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed SSE port.
    port: int = constants.DEFAULT_PORT_SSE

    @property
    def address(self) -> str:
        """A node's SSE server base address."""
        return f"http://{self.host}:{self.port}/events"

    def __str__(self):
        """Instance string representation."""
        return self.address

    def yield_events(
        self,
        echannel: NodeEventChannel,
        etype: NodeEventType = None,
        eid: int = 0
    ) -> typing.Generator[NodeEventInfo, None, None]:
        """Returns generator yielding (filterable) events emitted by a node's event stream.

        :param echannel: Type of event channel to which to bind.
        :param etype: Type of event type to listen for (all if unspecified).
        :param eid: Identifier of event from which to start stream listening.

        """
        # Set client.
        url = f"{self.address}/{echannel.name.lower()}"
        if eid:
            url = f"{url}?start_from={eid}"
        sse_client = sseclient.SSEClient(requests.get(url, stream=True))

        # Open connection & iterate event stream.
        try:
            for event in sse_client.events():
                # Set event data.
                try:
                    edata = json.loads(event.data)
                except json.JSONDecodeError:
                    edata = event.data

                # Set event type.
                if isinstance(edata, str):
                    etype_in = NodeEventType.Shutdown
                else:
                    for etype_in in NodeEventType:
                        if etype_in.name in edata:
                            break
                    else:
                        raise ValueError(f"Unknown event type: {edata}")

                # If event type is in scope then yield event information.
                if etype is None or etype == etype_in:
                    yield NodeEventInfo(echannel, etype_in, event.id, edata)

        # On error ensure that connection is closed.
        except Exception as err:
            try:
                sse_client.close()
            except Exception as inner_err:
                print(f"Ignoring error raised on closing SSE connection: {inner_err}.")
            finally:
                raise err
