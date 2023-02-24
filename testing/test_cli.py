# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import json
import os
import re
import shlex
import sys
from unittest import mock

import pytest
from pytest_mock import MockerFixture

if sys.version_info < (3, 8, 0):
    raise pytest.skip(reason="AsyncMock not supported on Python 3.7", allow_module_level=True)
from unittest.mock import AsyncMock

from bleak.backends.device import BLEDevice
from click.testing import CliRunner

from calypso_anemometer.cli import cli
from calypso_anemometer.model import CalypsoReading
from testing.data import dummy_device_info, dummy_device_status, dummy_wire_message_bad, dummy_wire_message_good


def test_cli_version():
    """
    Test `calypso-anemometer --version`
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"], catch_exceptions=False)
    assert re.match(r"cli, version \d+\.\d+\.\d+", result.stdout) is not None


def test_cli_fake_verbose(caplog):
    """
    Test `calypso-anemometer --verbose fake`
    """
    fake_reading = CalypsoReading(
        wind_speed=1, wind_direction=1, battery_level=1, temperature=-99, roll=-89, pitch=-89, heading=1
    )
    runner = CliRunner()
    result = runner.invoke(cli, shlex.split("--verbose fake"), catch_exceptions=False)
    stdout = result.stdout.strip()
    assert stdout == fake_reading.asjson()
    assert "Producing reading" in caplog.messages


def test_cli_fake_quiet(caplog):
    """
    Test `calypso-anemometer --quiet fake`
    """
    runner = CliRunner()
    result = runner.invoke(cli, shlex.split("--quiet fake"), catch_exceptions=False)
    stdout = result.stdout.strip()
    assert stdout == ""
    assert "Producing reading" in caplog.messages


def test_cli_fake_rate(caplog):
    """
    Test `calypso-anemometer --verbose fake --rate=hz_8`
    """
    fake_reading = CalypsoReading(
        wind_speed=1, wind_direction=1, battery_level=1, temperature=-99, roll=-89, pitch=-89, heading=1
    )
    runner = CliRunner()
    result = runner.invoke(cli, shlex.split("--verbose fake --rate=hz_8"), catch_exceptions=False)
    stdout = result.stdout.strip()
    assert stdout == fake_reading.asjson()
    assert "Producing reading" in caplog.messages


@mock.patch(
    "calypso_anemometer.core.BleakScanner.find_device_by_filter",
    AsyncMock(return_value=BLEDevice(name="foo", address="bar")),
)
@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=b"foobar"))
@mock.patch("calypso_anemometer.core.CalypsoDeviceApi.get_status", AsyncMock(return_value=dummy_device_status))
def test_cli_info(caplog):
    """
    Test `calypso-anemometer info`
    """

    runner = CliRunner()
    result = runner.invoke(cli, ["info"], catch_exceptions=False)

    response = json.loads(result.stdout)
    assert response["info"]["ble_address"] == "bar"
    assert response["status"]["rate"] == "HZ_8"

    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
    assert "Found device at address: bar: foo" in caplog.messages
    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Getting device information" in caplog.messages
    assert "Disconnecting" in caplog.messages


@mock.patch(
    "calypso_anemometer.core.BleakScanner.find_device_by_filter",
    AsyncMock(return_value=BLEDevice(name="foo", address="bar")),
)
@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_good))
def test_cli_read_stdout_success(caplog):
    """
    Test successful `calypso-anemometer read`
    """

    runner = CliRunner()
    result = runner.invoke(cli, ["read"], catch_exceptions=False)
    assert result.exit_code == 0

    response = json.loads(result.stdout)
    assert response == {
        "battery_level": 90,
        "heading": 235,
        "pitch": -60,
        "roll": 30,
        "temperature": 33,
        "wind_direction": 206,
        "wind_speed": 5.69,
    }

    assert (
        "Initializing client with Settings(ble_adapter='hci0', ble_address=None, "
        "ble_discovery_timeout=10.0, ble_connect_timeout=10.0)" in caplog.messages
    )
    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
    assert "Found device at address: bar: foo" in caplog.messages
    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Requesting reading" in caplog.messages
    assert "Received buffer:  b'9\\x02\\xce\\x00\\t\\x85x\\x1e}\\x00'" in caplog.messages
    assert (
        "Decoded reading: CalypsoReading(wind_speed=5.69, wind_direction=206, battery_level=90, "
        "temperature=33, roll=30, pitch=-60, heading=235)" in caplog.messages
    )
    assert "Disconnecting" in caplog.messages


@mock.patch(
    "calypso_anemometer.core.BleakScanner.find_device_by_filter",
    AsyncMock(return_value=BLEDevice(name="foo", address="bar")),
)
@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.write_gatt_char", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.start_notify", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.engine.wait_forever", AsyncMock(return_value=None))
def test_cli_subscribe_stdout_success(caplog):
    """
    Test successful `calypso-anemometer read --subscribe`
    """

    runner = CliRunner()
    result = runner.invoke(cli, ["read", "--subscribe", "--rate=HZ_8"], catch_exceptions=False)
    assert result.exit_code == 0

    # TODO: Currently no reading is emitted and processed, because `start_notify` is mocked
    #       and actually does nothing. Is there a way to emulate emitting readings easily?
    # response = json.loads(result.stdout)  # noqa: ERA001

    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
    assert "Found device at address: bar: foo" in caplog.messages
    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Setting data rate to 8" in caplog.messages
    assert "Subscribing to readings" in caplog.messages
    assert "Disconnecting" in caplog.messages


@mock.patch(
    "calypso_anemometer.core.BleakScanner.find_device_by_filter",
    AsyncMock(return_value=BLEDevice(name="foo", address="bar")),
)
@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_bad))
def test_cli_read_failure(caplog):
    """
    Test unsuccessful `calypso-anemometer read`
    """

    runner = CliRunner()
    result = runner.invoke(cli, ["read"], catch_exceptions=False)
    assert result.exit_code == 1
    assert result.stdout == ""

    assert "Using BLE discovery to find Calypso UP10 anemometer" in caplog.messages
    assert "Found device at address: bar: foo" in caplog.messages
    assert "Connecting to device at 'bar' with adapter 'hci0'" in caplog.messages
    assert "Requesting reading" in caplog.messages
    assert "Received buffer:  b'\\xaa'" in caplog.messages
    assert "Decoding reading failed. Reason: unpack requires a buffer of 10 bytes. Data: b'\\xaa'" in caplog.messages
    assert "Disconnecting" in caplog.messages


@mock.patch(
    "calypso_anemometer.core.BleakScanner.find_device_by_filter",
    AsyncMock(return_value=BLEDevice(name="foo", address="bar")),
)
@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_good))
def test_cli_read_telemetry_success(caplog):
    """
    Test successful `calypso-anemometer read --target=...`, with telemetry.
    """

    runner = CliRunner()
    result = runner.invoke(
        cli, ["read", "--target=udp+broadcast+nmea0183://255.255.255.255:60110"], catch_exceptions=False
    )
    assert result.exit_code == 0

    response = json.loads(result.stdout)
    assert response == {
        "battery_level": 90,
        "heading": 235,
        "pitch": -60,
        "roll": 30,
        "temperature": 33,
        "wind_direction": 206,
        "wind_speed": 5.69,
    }

    assert "Sending message to udp://255.255.255.255:60110. $IIVWR,154.0,L,11.06,N,5.69,M,20.48,K*65" in caplog.messages


@mock.patch(
    "calypso_anemometer.core.BleakScanner.find_device_by_filter",
    AsyncMock(return_value=BLEDevice(name="foo", address="bar")),
)
@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_good))
def test_cli_read_ble_adapter_success(mocker, caplog):
    """
    Test successful `calypso-anemometer read --ble-adapter=...`.
    """

    mocker.patch("calypso_anemometer.core.get_adapter_name", return_value="hci99")

    runner = CliRunner()
    result = runner.invoke(cli, ["read", "--ble-adapter=hci99"], catch_exceptions=False)
    assert result.exit_code == 0

    assert (
        "Initializing client with Settings(ble_adapter='hci99', ble_address=None, "
        "ble_discovery_timeout=10.0, ble_connect_timeout=10.0)" in caplog.messages
    )
    assert "Connecting to device at 'bar' with adapter 'hci99'" in caplog.messages


@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_good))
def test_cli_read_ble_address_option_success(caplog):
    """
    Test successful `calypso-anemometer read --ble-address=...`.
    """

    runner = CliRunner()
    result = runner.invoke(cli, ["read", "--ble-address=F8:C7:2C:EC:13:D0"], catch_exceptions=False)
    assert result.exit_code == 0

    assert (
        "Initializing client with Settings(ble_adapter='hci0', ble_address='F8:C7:2C:EC:13:D0', "
        "ble_discovery_timeout=10.0, ble_connect_timeout=10.0)" in caplog.messages
    )
    assert "Connecting to device at 'F8:C7:2C:EC:13:D0' with adapter 'hci0'" in caplog.messages


@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_good))
def test_cli_read_ble_address_envvar_success(mocker: MockerFixture, caplog):
    """
    Test successful `calypso-anemometer read`, with environment variable `CALYPSO_BLE_ADDRESS`.
    """

    mocker.patch.dict(os.environ, {"CALYPSO_BLE_ADDRESS": "F8:C7:2C:EC:13:D0"})

    runner = CliRunner()
    result = runner.invoke(cli, ["read"], catch_exceptions=False)
    assert result.exit_code == 0

    assert (
        "Initializing client with Settings(ble_adapter='hci0', ble_address='F8:C7:2C:EC:13:D0', "
        "ble_discovery_timeout=10.0, ble_connect_timeout=10.0)" in caplog.messages
    )
    assert "Connecting to device at 'F8:C7:2C:EC:13:D0' with adapter 'hci0'" in caplog.messages


@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.read_gatt_char", AsyncMock(return_value=dummy_wire_message_good))
def test_cli_read_ble_timeout_success(mocker: MockerFixture, caplog):
    """
    Test successful `calypso-anemometer read`, with `--ble-discovery-timeout` option and
    `CALYPSO_BLE_CONNECT_TIMEOUT` environment variable.
    """

    mocker.patch.dict(os.environ, {"CALYPSO_BLE_ADDRESS": "F8:C7:2C:EC:13:D0"})
    mocker.patch.dict(os.environ, {"CALYPSO_BLE_CONNECT_TIMEOUT": "7.7"})

    runner = CliRunner()
    result = runner.invoke(cli, ["read", "--ble-discovery-timeout=8.8"], catch_exceptions=False)
    assert result.exit_code == 0

    assert (
        "Initializing client with Settings(ble_adapter='hci0', ble_address='F8:C7:2C:EC:13:D0', "
        "ble_discovery_timeout=8.8, ble_connect_timeout=7.7)" in caplog.messages
    )


@mock.patch(
    "calypso_anemometer.core.BleakScanner.find_device_by_filter",
    AsyncMock(return_value=BLEDevice(name="foo", address="bar")),
)
@mock.patch("calypso_anemometer.core.BleakClient.connect", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.BleakClient.write_gatt_char", AsyncMock(return_value=None))
@mock.patch("calypso_anemometer.core.CalypsoDeviceApi.get_info", AsyncMock(return_value=dummy_device_info))
@mock.patch("calypso_anemometer.core.CalypsoDeviceApi.get_status", AsyncMock(return_value=dummy_device_status))
def test_cli_set_option_rate_success(caplog):
    """
    Test successful `calypso-anemometer set-option --rate=HZ_8`, with telemetry.
    """

    runner = CliRunner()
    result = runner.invoke(cli, ["set-option", "--rate=HZ_8"], catch_exceptions=False)
    assert result.exit_code == 0

    response = json.loads(result.stdout)
    assert response["info"]["ble_address"] == "bar"
    assert response["status"]["rate"] == "HZ_8"

    assert "Setting device data rate to 8" in caplog.messages
    assert "Setting data rate to 8" in caplog.messages
    # assert "Getting device information" in caplog.messages
