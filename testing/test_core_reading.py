# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import re
from unittest.mock import ANY, AsyncMock, MagicMock, call

import pytest
from pytest_mock import MockerFixture

import calypso_anemometer
from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.exception import CalypsoDecodingError
from testing.data import dummy_reading, dummy_wire_message_bad, dummy_wire_message_good


@pytest.mark.asyncio
async def test_reading_success(mocker: MockerFixture, caplog):

    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_good))

    spy = mocker.spy(calypso_anemometer.core.BleakClient, "read_gatt_char")
    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        reading = await calypso.get_reading()
        assert reading == dummy_reading

    assert spy.mock_calls == [call("00002a39-0000-1000-8000-00805f9b34fb")]

    assert "Connecting to device at 'bar' with adapter 'None'" in caplog.messages
    assert "Requesting reading" in caplog.messages
    assert "Received buffer:  b'9\\x02\\xce\\x00\\t\\x85x\\x1e}\\x00'" in caplog.messages
    assert (
        "Decoded reading: CalypsoReading(wind_speed=5.69, wind_direction=206, battery_level=90, "
        "temperature=33, roll=30, pitch=-60, compass=235)" in caplog.messages
    )
    assert "Disconnecting" in caplog.messages


@pytest.mark.asyncio
async def test_reading_failure(mocker: MockerFixture, caplog):

    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_bad))

    spy = mocker.spy(calypso_anemometer.core.BleakClient, "read_gatt_char")
    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        with pytest.raises(CalypsoDecodingError) as ex:
            await calypso.get_reading()
        assert ex.match(
            re.escape("Decoding reading failed. " "Reason: unpack requires a buffer of 10 bytes. Data: b'\\xaa'")
        )

    assert spy.mock_calls == [call("00002a39-0000-1000-8000-00805f9b34fb")]

    assert "Connecting to device at 'bar' with adapter 'None'" in caplog.messages
    assert "Requesting reading" in caplog.messages
    assert "Received buffer:  b'\\xaa'" in caplog.messages
    assert "Decoding reading failed. Reason: unpack requires a buffer of 10 bytes. Data: b'\\xaa'" in caplog.messages
    assert "Disconnecting" in caplog.messages


@pytest.mark.asyncio
async def test_subscribe_success(mocker: MockerFixture, caplog):

    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.start_notify", AsyncMock(return_value=None))

    callback = MagicMock()

    spy = mocker.spy(calypso_anemometer.core.BleakClient, "start_notify")
    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        await calypso.subscribe_reading(callback=callback)

    assert spy.mock_calls == [call("00002a39-0000-1000-8000-00805f9b34fb", ANY)]

    # FIXME: Not yet.
    # assert callback.assert_called_once_with()

    assert "Connecting to device at 'bar' with adapter 'None'" in caplog.messages
    assert "Subscribing to readings" in caplog.messages
    assert "Disconnecting" in caplog.messages


@pytest.mark.asyncio
async def test_unsubscribe_success(mocker: MockerFixture, caplog):

    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.start_notify", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.stop_notify", AsyncMock(return_value=None))

    spy_start_notify = mocker.spy(calypso_anemometer.core.BleakClient, "start_notify")
    spy_stop_notify = mocker.spy(calypso_anemometer.core.BleakClient, "stop_notify")
    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        await calypso.subscribe_reading()
        await calypso.unsubscribe_reading()

    assert spy_start_notify.mock_calls == [call("00002a39-0000-1000-8000-00805f9b34fb", ANY)]
    assert spy_stop_notify.mock_calls == [call("00002a39-0000-1000-8000-00805f9b34fb")]

    assert "Connecting to device at 'bar' with adapter 'None'" in caplog.messages
    assert "Subscribing to readings" in caplog.messages
    assert "Unsubscribing from readings" in caplog.messages
    assert "Disconnecting" in caplog.messages
