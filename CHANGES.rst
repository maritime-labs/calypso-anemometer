############################
calypso-anemometer changelog
############################


in progress
===========


2022-08-03 0.5.1
================
- Fix import error ``ModuleNotFoundError: No module named 'aiorate'``
- Configure minimum log level to ``WARNING`` when using the ``--quiet`` option


2022-08-01 0.5.0
================

Changes
-------
- Fix import error on Python 3.7
  ``AttributeError: module 'asyncio' has no attribute 'exceptions'``
- Add a few more software tests
- Add a few example programs
- Drop support for Python 3.6
- Add ``make lint`` sandbox utility task
- Emit ``CalypsoDecodingError`` exceptions when decoding wire data fails
- Refactor workhorse functions from ``cli.py`` to ``engine.py``
- Significantly improve test coverage
- Introduce ``Settings``, to bundle configuration settings
  through command line options or environment variables.

  - ``--ble-adapter`` / ``CALYPSO_BLE_ADAPTER``
  - ``--ble-address`` / ``CALYPSO_BLE_ADDRESS``
  - ``--ble-discovery-timeout`` / ``CALYPSO_BLE_DISCOVERY_TIMEOUT``
  - ``--ble-connect-timeout`` / ``CALYPSO_BLE_CONNECT_TIMEOUT``
- Add ``--quiet`` option / ``CALYPSO_QUIET`` environment variable for
  silencing output to STDOUT
- Explicitly use little-endian byte order for decoding binary data

Breaking changes
----------------
- The ``CALYPSO_ADDRESS`` environment variable has been renamed to
  ``CALYPSO_BLE_ADDRESS``.


2022-07-25 0.4.0
================
- Telemetry: Generate fake device readings, for supplying synthetic data


2022-07-17 0.3.0
================
- CI: Run software tests on GHA
- Fix installation on Python 3.6
- NMEA-0183: Fix computing ``LR`` direction indicator
- NMEA-0183: Compute missing ``speed_`` from other ``speed_`` values
- NMEA-0183: Implement checksum
- Telemetry: Synthesize zeroing of wind direction, when wind speed goes zero


2022-07-15 0.2.0
================
- Add software tests for telemetry subsystem
- NMEA-0183: Fix message structure
- NMEA-0183: Fix wind direction and add "left/right of bow" indicator
- Fix reading/decoding data rate
- Optimize discovery: Stop scanning when device was found


2022-07-14 0.1.0
================
- Minimal implementation, connecting to the device
- Add CLI interface with subcommands ``info`` and ``explore``
- Implement client interface as context manager
- Increase default timeout values to 15 seconds
- Rework device info acquisition
- Read and decode device status bytes: mode, rate, compass
- Add ``set-option`` subcommand
- Add ``read`` subcommand
- Implement ``--subscribe`` flag to ``read`` subcommand
- Add ``--rate`` option to ``read`` subcommand to set the device
  data rate before starting the conversation
- Add telemetry subsystem, to be used with new ``--target`` option
- Add telemetry adapter for ``UDP_SIGNALK_DELTA``
- Add telemetry adapter for ``UDP_BROADCAST_NMEA0183``
