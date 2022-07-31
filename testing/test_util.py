# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from unittest import mock
from unittest.mock import AsyncMock

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
@mock.patch("calypso_anemometer.util.asyncio.wait_for", AsyncMock(return_value=None))
async def test_wait_forever():
    await wait_forever()
