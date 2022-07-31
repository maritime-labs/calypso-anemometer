# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import sys

import pytest

from calypso_anemometer.model import BleCharSpec
from calypso_anemometer.util import to_json, wait_forever


def test_json_encoder_primitive():
    assert to_json("foobar") == '"foobar"'


def test_json_encoder_object():
    with pytest.raises(TypeError) as ex:
        to_json(object())
    assert ex.match("Object of type object is not JSON serializable")


def test_json_encoder_dataclass():
    assert to_json(BleCharSpec("foo", "12345"), pretty=False) == '{"name": "foo", "uuid": "12345", "decoder": null}'


@pytest.mark.asyncio
async def test_wait_forever(mocker):
    if sys.version_info < (3, 8, 0):
        raise pytest.skip(reason="AsyncMock not supported on Python 3.7")

    from unittest.mock import AsyncMock

    mocker.patch("calypso_anemometer.util.asyncio.wait_for", AsyncMock(return_value=None))

    await wait_forever()
