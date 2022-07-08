import asyncio
import dataclasses
import functools
import json
import logging
import sys


def setup_logging(level=logging.INFO):
    log_format = "%(asctime)-15s [%(name)-25s] %(levelname)-8s: %(message)s"
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


class JsonEncoderPlus(json.JSONEncoder):
    """
    JSON encoder with support for serializing Enums and Data Classes.

    - https://docs.python.org/3/library/json.html#json.JSONEncoder
    - https://docs.python.org/3/library/enum.html
    - https://docs.python.org/3/library/dataclasses.html
    """

    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return json.JSONEncoder.default(self, obj)


def to_json(obj, pretty=True):
    """
    Serialize any object to JSON by using a custom encoder.
    """
    kwargs = {}
    if pretty:
        kwargs["indent"] = 2
    return json.dumps(obj, cls=JsonEncoderPlus, **kwargs)
