def enum(*args, **kwargs):
    """ Add the ability to define an enum-like object """
    enums = dict(zip(args, range(len(args))), **kwargs)
    return type('Enum', (), enums)