# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import sys
from unittest import mock

import pytest

if sys.version_info < (3, 8, 0):
    raise pytest.skip(reason="AsyncMock not supported on Python 3.7", allow_module_level=True)
from unittest.mock import AsyncMock

from pytest_mock import MockerFixture

from calypso_anemometer.core import CHARSPEC_COMPASS_STATUS, CHARSPEC_DATARATE, CHARSPEC_MODE, CalypsoDeviceApi
from calypso_anemometer.model import (
    CalypsoDeviceCompassStatus,
    CalypsoDeviceDataRate,
    CalypsoDeviceInfo,
    CalypsoDeviceMode,
    CalypsoDeviceStatus,
)
from testing.data import dummy_device_info, dummy_device_status


@pytest.mark.asyncio
@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=b"foobar"))
async def test_info_success(caplog):

    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        device_info_mocked = await calypso.get_info()
        device_info_reference = CalypsoDeviceInfo(
            ble_address="bar",
            manufacturer_name="foobar",
            model_number="foobar",
            serial_number="foobar",
            hardware_revision="foobar",
            firmware_revision="foobar",
            software_revision="foobar",
        )

        assert device_info_mocked == device_info_reference

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Getting device information" in caplog.messages
    assert "Disconnecting" in caplog.messages


@pytest.mark.asyncio
async def test_status_success(mocker: MockerFixture, caplog):

    char_value_map = {
        CHARSPEC_MODE.uuid: 0x02,
        CHARSPEC_DATARATE.uuid: 0x08,
        CHARSPEC_COMPASS_STATUS.uuid: 0x01,
    }

    async def read_gatt_char(client, char_specifier):
        value = char_value_map.get(char_specifier)
        return [value]

    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.read_gatt_char", read_gatt_char)

    async with CalypsoDeviceApi(ble_address="bar") as calypso:

        device_status_mocked = await calypso.get_status()

        device_status_reference = CalypsoDeviceStatus(
            mode=CalypsoDeviceMode.NORMAL,
            rate=CalypsoDeviceDataRate.HZ_8,
            compass=CalypsoDeviceCompassStatus.ON,
        )

        assert device_status_mocked == device_status_reference

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Getting status information" in caplog.messages
    assert "Disconnecting" in caplog.messages


@pytest.mark.asyncio
async def test_status_failure(mocker: MockerFixture, caplog):

    char_value_map = {
        CHARSPEC_MODE.uuid: 0x42,
        CHARSPEC_DATARATE.uuid: 0x43,
        CHARSPEC_COMPASS_STATUS.uuid: 0x44,
    }

    async def read_gatt_char(client, char_specifier):
        value = char_value_map.get(char_specifier)
        return [value]

    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.BleakClient.read_gatt_char", read_gatt_char)

    async with CalypsoDeviceApi(ble_address="bar") as calypso:

        with pytest.raises(ValueError) as ex:
            await calypso.get_status()
        ex.match("66 is not a valid CalypsoDeviceMode")

    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Getting status information" in caplog.messages
    assert "Disconnecting" in caplog.messages


@pytest.mark.asyncio
async def test_about_success(mocker: MockerFixture, caplog, capsys):
    mocker.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
    mocker.patch("calypso_anemometer.core.CalypsoDeviceApi.get_info", AsyncMock(return_value=dummy_device_info))
    mocker.patch("calypso_anemometer.core.CalypsoDeviceApi.get_status", AsyncMock(return_value=dummy_device_status))

    async with CalypsoDeviceApi(ble_address="bar") as calypso:
        await calypso.about()

    stdout, stderr = capsys.readouterr()
    assert '"ble_address": "bar"' in stdout
    assert '"rate": "HZ_8"' in stdout
