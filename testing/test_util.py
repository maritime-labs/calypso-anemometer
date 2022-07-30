# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from calypso_anemometer.model import BleCharSpec
from calypso_anemometer.util import to_json


def test_json_encoder_primitive():
    assert to_json("foobar") == '"foobar"'


def test_json_encoder_dataclass():
    assert to_json(BleCharSpec("foo", "12345"), pretty=False) == '{"name": "foo", "uuid": "12345", "decoder": null}'
