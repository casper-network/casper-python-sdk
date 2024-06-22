import json
import typing

import requests
import sseclient

from pycspr.api.node.sse.connection import ConnectionInfo
from pycspr.api.node.sse.types import EventInfo
from pycspr.api.node.sse.types import EventType


class Proxy:
    """Node SSE server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.connection_info = connection_info

    @property
    def address(self) -> str:
        """A node's REST server base address."""
        return f"http://{self.connection_info.host}:{self.connection_info.port}/events"

    def __str__(self):
        """Instance string representation."""
        return self.address

    def yield_events(
        self,
        etype: EventType = None,
        eid: int = 0
    ) -> typing.Generator[EventInfo, None, None]:
        """Returns generator yielding (filterable) events emitted by a node's event stream.

        :param etype: Type of event type to listen for (all if unspecified).
        :param eid: Identifier of event from which to start stream listening.

        """
        # Set client.
        url = self.address
        if eid:
            url = f"{url}?start_from={eid}"
        sse_client: sseclient.SSEClient = sseclient.SSEClient(
            requests.get(url, stream=True)
        )

        # Open connection & iterate event stream.
        try:
            for event in sse_client.events():
                # Set event data.
                try:
                    edata = json.loads(event.data)
                except json.JSONDecodeError:
                    edata = event.data
                print(edata)

                # Set event type.
                if isinstance(edata, str):
                    etype_in = EventType.Shutdown
                else:
                    for etype_in in EventType:
                        if etype_in.name in edata:
                            break
                    else:
                        raise ValueError(f"Unknown event type: {edata}")

                # If event type is in scope then yield event information.
                if etype is None or etype == etype_in:
                    yield EventInfo(etype_in, event.id, edata)

        # On error ensure that connection is closed.
        except Exception as err:
            try:
                sse_client.close()
            except Exception as inner_err:
                print(f"Ignoring error raised on closing SSE connection: {inner_err}.")
            finally:
                raise err
