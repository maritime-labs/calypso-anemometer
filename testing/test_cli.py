# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import re
import shlex

from click.testing import CliRunner

from calypso_anemometer.cli import cli
from calypso_anemometer.model import CalypsoReading


def test_cli_version():
    """
    Test `calypso-anemometer --version`
    """
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"], catch_exceptions=False)
    assert re.match(r"cli, version \d+\.\d+\.\d+", result.stdout) is not None


def test_cli_fake_default(caplog):
    """
    Test `calypso-anemometer --verbose fake`
    """
    fake_reading = CalypsoReading(
        wind_speed=1, wind_direction=1, battery_level=1, temperature=-99, roll=-89, pitch=-89, compass=1
    )
    runner = CliRunner()
    result = runner.invoke(cli, shlex.split("--verbose fake"), catch_exceptions=False)
    stdout = result.stdout.strip()
    assert stdout == fake_reading.asjson()
    assert "Producing reading" in caplog.messages


def test_cli_fake_rate(caplog):
    """
    Test `calypso-anemometer --verbose fake --rate=hz_8`
    """
    fake_reading = CalypsoReading(
        wind_speed=1, wind_direction=1, battery_level=1, temperature=-99, roll=-89, pitch=-89, compass=1
    )
    runner = CliRunner()
    result = runner.invoke(cli, shlex.split("--verbose fake --rate=hz_8"), catch_exceptions=False)
    stdout = result.stdout.strip()
    assert stdout == fake_reading.asjson()
    assert "Producing reading" in caplog.messages
