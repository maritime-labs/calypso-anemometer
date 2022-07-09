import logging
import os
import sys
from typing import Callable, Optional

import click

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.exception import CalypsoError
from calypso_anemometer.util import make_sync, setup_logging, to_json

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


cli.add_command(info, name="info")
cli.add_command(explore, name="explore")
