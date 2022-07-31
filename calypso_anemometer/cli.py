# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
import logging
import typing as t

import click

from calypso_anemometer.core import CalypsoDeviceApi
from calypso_anemometer.engine import handler_factory, run_engine
from calypso_anemometer.fake import CalypsoDeviceApiFake
from calypso_anemometer.model import ApplicationSettings, CalypsoDeviceDataRate, CalypsoDeviceMode
from calypso_anemometer.util import EnumChoice, make_sync, setup_logging

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
@click.option("--verbose", is_flag=True, required=False, help="Increase log verbosity.")
@click.option("--debug", is_flag=True, required=False, help="Enable debug messages.")
@click.pass_context
def cli(ctx, verbose, debug):
    setup_logging(level=logging.INFO)


@click.command()
@click.pass_context
@make_sync
async def info(ctx):
    await run_engine(workhorse=CalypsoDeviceApi, handler=lambda calypso: calypso.about())


@click.command()
@click.pass_context
@make_sync
async def explore(ctx):
    await run_engine(workhorse=CalypsoDeviceApi, handler=lambda calypso: calypso.explore())


ble_adapter_option = click.option(
    "--ble-adapter",
    envvar="CALYPSO_BLE_ADAPTER",
    type=str,
    required=False,
    default="hci0",
    help="Which Bluetooth adapter to use, e.g. `hci1`. Default: `hci0`",
)
rate_option = click.option(
    "--rate",
    type=EnumChoice(CalypsoDeviceDataRate, case_sensitive=False),
    required=False,
    help="Set device data rate to one of HZ_1, HZ_4, or HZ_8.",
)
subscribe_option = click.option("--subscribe", is_flag=True, required=False, help="Continuously receive readings")
target_option = click.option("--target", type=str, required=False, help="Submit telemetry data to target")


@click.command()
@ble_adapter_option
@click.option(
    "--mode",
    type=EnumChoice(CalypsoDeviceMode, case_sensitive=False),
    required=False,
    help="Set device mode to one of SLEEP, LOW_POWER, or NORMAL.",
)
@rate_option
@click.pass_context
@make_sync
async def set_option(
    ctx,
    ble_adapter: str = None,
    mode: t.Optional[CalypsoDeviceMode] = None,
    rate: t.Optional[CalypsoDeviceDataRate] = None,
):
    async def handler(calypso: CalypsoDeviceApi):
        if mode is not None:
            logger.info(f"Setting device mode to {mode}")
            await calypso.set_mode(mode)
        if rate is not None:
            logger.info(f"Setting device data rate to {rate}")
            await calypso.set_datarate(rate)
        await calypso.about()

    settings = ApplicationSettings(ble_adapter=ble_adapter)
    await run_engine(workhorse=CalypsoDeviceApi, settings=settings, handler=handler)


@click.command()
@ble_adapter_option
@subscribe_option
@target_option
@rate_option
@click.pass_context
@make_sync
async def read(
    ctx,
    ble_adapter: str = None,
    subscribe: bool = False,
    target: t.Optional[str] = None,
    rate: t.Optional[CalypsoDeviceDataRate] = None,
):
    settings = ApplicationSettings(ble_adapter=ble_adapter)
    handler = await handler_factory(subscribe=subscribe, target=target, rate=rate)
    await run_engine(workhorse=CalypsoDeviceApi, settings=settings, handler=handler)


@click.command()
@subscribe_option
@target_option
@rate_option
@click.pass_context
@make_sync
async def fake(
    ctx, subscribe: bool = False, target: t.Optional[str] = None, rate: t.Optional[CalypsoDeviceDataRate] = None
):
    handler = await handler_factory(subscribe=subscribe, target=target, rate=rate)
    await run_engine(workhorse=CalypsoDeviceApiFake, handler=handler)


cli.add_command(info, name="info")
cli.add_command(explore, name="explore")
cli.add_command(set_option, name="set-option")
cli.add_command(read, name="read")
cli.add_command(fake, name="fake")
