DECODERS = {
    bool: lambda x: None if x is None else bool(x),
    bytes: lambda x: None if x is None else bytes.fromhex(x),
    dict: lambda x: x,
    int: lambda x: None if x is None else int(x),
    str: lambda x: None if x is None else x.strip(),
}
