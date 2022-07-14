############################
calypso-anemometer changelog
############################


in progress
===========
- Add software tests for telemetry subsystem
- NMEA-0183: Fix message structure
- NMEA-0183: Fix wind direction and add "left/right of bow" indicator


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
