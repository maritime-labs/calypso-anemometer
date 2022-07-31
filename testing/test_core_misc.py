# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import dataclasses
from unittest.mock import AsyncMock, call

import pytest
from pytest_mock import MockerFixture

import calypso_anemometer
from calypso_anemometer.core import CalypsoDeviceApi, get_adapter_name


@pytest.mark.asyncio
async def test_read_characteristic_string_success(mocker: MockerFixture, caplog):

    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=b"hello world"))

    spy = mocker.spy(calypso_anemometer.core.BleakClient, "read_gatt_char")
    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        reading = await calypso.read_characteristic_string(characteristic_id="7511CFCC-0B20-4E20-82B5-BC94969768B6")
        assert reading == "hello world"

    assert spy.mock_calls == [call("7511CFCC-0B20-4E20-82B5-BC94969768B6")]

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Reading the characteristic 7511CFCC-0B20-4E20-82B5-BC94969768B6 as string" in caplog.messages
    assert "Disconnecting" in caplog.messages


def test_adapter_name_valid():
    @dataclasses.dataclass
    class foo:
        _adapter: str

    dummy = foo(_adapter="bar")
    assert get_adapter_name(dummy) == "bar"


def test_adapter_name_none():
    dummy = object()
    assert get_adapter_name(dummy) is None
