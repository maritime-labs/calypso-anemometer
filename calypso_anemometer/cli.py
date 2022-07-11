import logging
import os
import sys
from typing import Callable, Optional

import click

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.exception import CalypsoError
from calypso_anemometer.model import CalypsoDeviceDataRate, CalypsoDeviceMode
from calypso_anemometer.util import EnumChoice, make_sync, setup_logging, to_json, wait_forever

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
@click.option("--verbose", is_flag=True, required=False, help="Increase log verbosity.")
@click.option("--debug", is_flag=True, required=False, help="Enable debug messages.")
@click.pass_context
def cli(ctx, verbose, debug):
    setup_logging(level=logging.INFO)


"""
@click.argument("kind", type=str, required=True)
@click.option("--flavor", type=str, required=False,
              help="Use `--flavor=docker-compose` for generating a configuration file suitable "
                   "for use within the provided Docker Compose environment.")
"""


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
    async def handler(calypso: CalypsoDeviceApi):
        device_info = await calypso.get_info()
        print(to_json(device_info))
        device_status = await calypso.get_status()
        print(to_json(device_status.aslabeldict()))

    await calypso_run(handler)


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

    await calypso_run(handler)


@click.command()
@click.option("--subscribe", is_flag=True, required=False, help="Continuously receive readings")
@rate_option
@click.pass_context
@make_sync
async def read(ctx, subscribe: bool = False, rate: Optional[CalypsoDeviceDataRate] = None):
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

            await calypso.subscribe_reading(lambda reading: reading.print())
            await wait_forever()

    await calypso_run(handler)


cli.add_command(info, name="info")
cli.add_command(explore, name="explore")
cli.add_command(set_option, name="set-option")
cli.add_command(read, name="read")