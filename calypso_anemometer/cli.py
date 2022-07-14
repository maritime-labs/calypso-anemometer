# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging
import os
import sys
from typing import Callable, Optional

import click

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.exception import CalypsoError
from calypso_anemometer.model import CalypsoDeviceDataRate, CalypsoDeviceMode, CalypsoReading
from calypso_anemometer.telemetry import TelemetryAdapter
from calypso_anemometer.util import EnumChoice, make_sync, setup_logging, to_json, wait_forever

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
@click.option("--verbose", is_flag=True, required=False, help="Increase log verbosity.")
@click.option("--debug", is_flag=True, required=False, help="Enable debug messages.")
@click.pass_context
def cli(ctx, verbose, debug):
    setup_logging(level=logging.INFO)


async def calypso_run(callback: Callable):
    try:
        async with CalypsoDeviceApi(ble_address=os.getenv("CALYPSO_ADDRESS")) as calypso:
            await callback(calypso)
    except CalypsoError as ex:
        logger.error(ex)
        sys.exit(1)


@click.command()
@click.pass_context
@make_sync
async def info(ctx):
    await calypso_run(lambda calypso: calypso.about())


@click.command()
@click.pass_context
@make_sync
async def explore(ctx):
    await calypso_run(lambda calypso: calypso.explore())


rate_option = click.option(
    "--rate",
    type=EnumChoice(CalypsoDeviceDataRate, case_sensitive=False),
    required=False,
    help="Set device data rate to one of HZ_1, HZ_4, or HZ_8.",
)


@click.command()
@click.option(
    "--mode",
    type=EnumChoice(CalypsoDeviceMode, case_sensitive=False),
    required=False,
    help="Set device mode to one of SLEEP, LOW_POWER, or NORMAL.",
)
@rate_option
@click.pass_context
@make_sync
async def set_option(ctx, mode: Optional[CalypsoDeviceMode] = None, rate: Optional[CalypsoDeviceDataRate] = None):
    async def handler(calypso: CalypsoDeviceApi):
        if mode is not None:
            logger.info(f"Setting device mode to {mode}")
            await calypso.set_mode(mode)
        if rate is not None:
            logger.info(f"Setting device data rate to {rate}")
            await calypso.set_datarate(rate)
        await calypso.about()

    await calypso_run(handler)


@click.command()
@click.option("--subscribe", is_flag=True, required=False, help="Continuously receive readings")
@click.option("--target", type=str, required=False, help="Submit telemetry data to target")
@rate_option
@click.pass_context
@make_sync
async def read(
    ctx, subscribe: bool = False, target: Optional[str] = None, rate: Optional[CalypsoDeviceDataRate] = None
):

    telemetry = None
    if target is not None:
        telemetry = TelemetryAdapter(uri=target)

    async def handler(calypso: CalypsoDeviceApi):

        # One-shot reading.
        if not subscribe:
            reading = await calypso.get_reading()
            reading.print()

        # Continuous readings.
        else:
            if rate is not None:
                logger.info(f"Setting device data rate to {rate}")
                await calypso.set_datarate(rate)

            def process_reading(reading: CalypsoReading):
                reading.print()
                if telemetry is not None:
                    telemetry.submit(reading)

            await calypso.subscribe_reading(process_reading)
            await wait_forever()

    await calypso_run(handler)


cli.add_command(info, name="info")
cli.add_command(explore, name="explore")
cli.add_command(set_option, name="set-option")
cli.add_command(read, name="read")
