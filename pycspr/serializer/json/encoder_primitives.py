ENCODERS = {
    bool: lambda x: x,
    bytes: lambda x: None if x is None else x.hex(),
    dict: lambda x: x,
    int: lambda x: x,
    str: lambda x: None if x is None else x.strip(),
}
