class GQLException(Exception):
    pass


import inspect


def gql(f):
    """Unused"""

    def wrapper(*args, **kwargs):
        print("signature", inspect.signature(f))
        print("args", args, "kwargs", kwargs)
        return f(*args, **kwargs)

    return wrapper
