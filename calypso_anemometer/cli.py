import json
import logging
import os
import sys

import click

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.util import make_sync, setup_logging

logger = logging.getLogger()


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


async def api_factory() -> CalypsoDeviceApi:
    calypso = CalypsoDeviceApi(ble_address=os.getenv("CALYPSO_ADDRESS"))
    if not await calypso.discover():
        logger.error("Unable to discover device")
        sys.exit(1)
    return calypso


@click.command()
@click.pass_context
@make_sync
async def info(ctx):
    calypso = await api_factory()
    try:
        await calypso.connect()
        info = await calypso.get_info()
        print(json.dumps(info, indent=2))
    finally:
        await calypso.disconnect()


@click.command()
@click.pass_context
@make_sync
async def explore(ctx):
    calypso = await api_factory()
    try:
        await calypso.connect()
        await calypso.explore()
    finally:
        await calypso.disconnect()


cli.add_command(info, name="info")
cli.add_command(explore, name="explore")
