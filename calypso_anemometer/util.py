import asyncio
import functools
import logging
import sys


def setup_logging(level=logging.INFO):
    log_format = "%(asctime)-15s [%(name)-8s] %(levelname)-8s: %(message)s"
    logging.basicConfig(format=log_format, stream=sys.stderr, level=level)


def make_sync(func):
    """
    Click entrypoint decorator for wrapping asynchronous functions.

    https://github.com/pallets/click/issues/2033
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper
