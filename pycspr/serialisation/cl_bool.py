def from_bytes(value: bytes) -> bool:
    return bool(value[0])


def to_bytes(value: bool) -> bytes:
    return bytes([int(value)])


def from_json(value: str) -> bool:
    if value == "False":
        return False
    elif value == "True":
        return True
    else:
        raise ValueError("Invalid boolean string representation")


def to_json(value: bool) -> str:
    return str(value)
