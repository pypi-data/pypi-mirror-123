import sys


def err_print(*args, **kwargs) -> None:
    """
    Use sys.stderr.write() as print()
    """
    print(*args, file=sys.stderr, **kwargs)
