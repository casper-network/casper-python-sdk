import typing


def from_bytes(value: bytes) -> None:
    if len(value) != 0:
        raise ValueError("Invalid unit bytes")
    return None
    

def to_bytes(_: typing.Type[None]) -> bytes:
    return bytes([])


def from_json(value: str) -> object:
    if len(value) != 0:
        raise ValueError("Invalid unit json")
    return None


def to_json(value: typing.Type[None]) -> str:
    return ""
