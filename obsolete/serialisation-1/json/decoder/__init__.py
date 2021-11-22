import json
import typing

from pycspr.serialisation.json.decoder.deploy import decode_deploy


def decode(entity: str) -> object:
    """Decodes a JSON representation of a domain entity.

    :param entity: A domain entity encoded as a JSON text blob.
    :returns: A domain entity.

    """
    obj = json.loads(entity)

    # NOTE: at present only deploys need to decoded.
    return decode_deploy(obj)
