import typing
import operator
from operator import add


def to_bytes(instance: list, item_encoder: typing.Callable) -> bytearray:
    return [len(instance)] + map(operator.add, [item_encoder(i) for i in instance])

