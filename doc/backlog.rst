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
- [o] BLE: Select BLE adapter, using ``--ble-adapter`` or ``CALYPSO_BLE_ADAPTER``
- [o] BLE: Obtain peripheral address from both ``--ble-address`` or ``CALYPSO_BLE_ADDRESS``
- [o] NMEA-0183: Properly send sentence termination ``<CR><LF>``
- [o] Add more software tests


**************
Iteration +2.5
**************
Topic: Going into production

- [o] Systemd unit, with installer
- [o] Day/night switching
- [o] Turn off logging to STDOUT


************
Iteration +3
************
- [o] Make up ``NMEA-0183`` messages for other parameters ``battery_level``,
  ``temperature``, ``roll``, ``pitch``, and ``compass``
  - What about ``$IIXDR,C,20,C,TempAir``? -- https://forum.arduino.cc/t/nmea0183-checksum/559531
- [o] Unlock adjusting offset and calibration values
- [o] Improve SignalK telemetry measurement ``path`` attributes,
  like ``electrical.batteries.99``
- [o] Improve inline documentation
- [o] Improve "naming things"
- [o] Make more yet hardcoded details configurable
- [o] Add SignalK WebSocket client
