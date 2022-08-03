##########################
calypso-anemometer backlog
##########################


************
Iteration +0
************
- [x] Acquire device state
- [x] Acquire readings
- [x] Send readings to SignalK via UDP
- [x] File headers
- [x] Badges
- [x] Release 0.1.0


************
Iteration +1
************
- [x] Start with software tests
- [x] Fix ``NMEA-0183`` wind direction and add "left/right of bow"
  indicator with formula ``(angle > 180) and angle - 360 or angle``
- [x] Optimize discovery: Stop scanning when device was found


**************
Iteration +1.5
**************
- [x] CI: Run software tests on GHA
- [x] Docs: Get rid of mentioning port 2000, only use port 10110
- [x] Docs: Replace screenshot ``NMEA-0183 UDP receiver on port 2000``
- [x] NMEA-0183: Fix computing ``LR`` direction indicator
- [x] NMEA-0183: Compute missing ``speed_`` from other ``speed_`` values.
- [x] Telemetry: Synthesize zeroing of wind direction, when wind speed goes zero
- [x] NMEA-0183: Implement checksum


************
Iteration +2
************
Topic: Documentation improvements, more fixes

- [x] Documentation about getting started (socat) vs. running in production (systemd)
  => Use separate pages than README
- [x] Docs: Project information on README
- [x] Docs: Other projects / credits
- [x] Docs: README: Adjust layout of badges
- [x] Docs: FAQ: Connected to wrong device?
- [x] Telemetry: Submit fake measurements, for supplying synthetic data to OpenCPN
  and other clients, like ``nmea-ui``


**************
Iteration +2.2
**************
- [x] Exception: ``AttributeError: module 'asyncio' has no attribute 'exceptions'``
- [x] Error when sending to ``255.255.255.255``: ``PermissionError: [Errno 13] Permission denied``


**************
Iteration +2.3
**************
Topic: QA

- [x] Tests: Add more software tests, significantly improve code coverage
- [x] Tests: Don't use port 10110 within software tests
- [x] Naming things: Telemetry subsystem
- [x] Naming things: ``Nmea0183Envelope``
- [x] Add test for ``CALYPSO_BLE_ADDRESS`` environment variable
- [x] CLI: Rework ``about`` command: Output a single result document to improve testing


**************
Iteration +2.5
**************
Topic: Production I

- [x] Introduce ``Settings`` container entity, for the following three options/settings
- [x] BLE: Select BLE adapter, using ``--ble-adapter`` or ``CALYPSO_BLE_ADAPTER``
- [x] BLE: Obtain peripheral address from both ``--ble-address`` or ``CALYPSO_BLE_ADDRESS``
- [x] BLE: Unlock ``--ble-*-timeout`` or ``CALYPSO_BLE_*_TIMEOUT``
- [x] CLI: Turn off logging to STDOUT
- [x] CLI: Use extended settings also for CLI entrypoints ``info`` and ``explore``
- [x] Endianness
- [x] Docs: Picture
- [x] Fix ``ModuleNotFoundError: No module named 'aiorate'``
- [/] Add option ``--log-level`` to complement ``--quiet``


**************
Iteration +2.7
**************
Topic: Production II

- [o] Engine: Do we need a retry logic, or should this just be handed over to ``systemd``?
- [o] Engine: Do we need a thread-based watchdog to kill the asyncio domain
  when it stalls completely? Is there any chance to recover at all?
- [o] Auxiliary: Add systemd unit file, optionally with installer
- [o] Auxiliary: Day/night switching
- [o] NMEA-0183: Review if sentence termination ``<CR><LF>`` is properly sent.


************
Iteration +3
************
- [o] Scan for ``FIXME`` and ``TODO`` markers
- [o] Unlock support for device's "compass" feature
- [o] Make up ``NMEA-0183`` messages for other parameters ``battery_level``,
  ``temperature``, ``roll``, ``pitch``, and ``compass``
  - What about ``$IIXDR,C,20,C,TempAir``? -- https://forum.arduino.cc/t/nmea0183-checksum/559531
- [o] Unlock adjusting offset and calibration values
- [o] Improve naming of SignalK telemetry measurement ``path`` attributes,
  like ``electrical.batteries.99``
- [o] Improve inline documentation
- [o] Improve "naming things"
- [o] Make more yet hardcoded details configurable
- [o] Add SignalK WebSocket client (documentation)
