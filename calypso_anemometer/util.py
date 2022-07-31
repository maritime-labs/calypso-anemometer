# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import asyncio
import dataclasses
import enum
import functools
import json
import logging
import sys
import typing as t

import click


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


class EnumChoice(click.Choice):
    # https://github.com/pallets/click/pull/2210
    def __init__(self, enum_type: t.Type[enum.Enum], case_sensitive: bool = True):
        super().__init__(
            choices=[element.name for element in enum_type],
            case_sensitive=case_sensitive,
        )
        self.enum_type = enum_type

    def convert(self, value: t.Any, param: t.Optional[click.Parameter], ctx: t.Optional[click.Context]) -> t.Any:
        value = super().convert(value=value, param=param, ctx=ctx)
        if value is None:  # pragma: no cover
            return None
        return self.enum_type[value]


async def wait_forever():
    future = asyncio.Future()
    return await asyncio.wait_for(future, timeout=None)
