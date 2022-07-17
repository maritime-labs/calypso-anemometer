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
- [o] NMEA-0183: Implement checksum
- [o] CLI-parameterised dummy measurement sending


************
Iteration +2
************
- [o] Select BLE adapter
- [o] Day/night switching
- [o] Turn off logging to STDOUT
- [o] Obtain peripheral address from both ``--ble-address`` and ``CALYPSO_BLE_ADDRESS``
- [o] Systemd unit, with installer
- [o] Documentation about getting started (socat) vs. running in production (systemd)
  => Use separate pages than README
- [o] Docs: FAQ: Connected to wrong device?
- [o] Docs: Project information on README
- [o] Docs: README: Adjust layout of badges
- [o] Docs: Other projects / credits


************
Iteration +3
************
- [o] Make up ``NMEA-0183`` messages for other parameters ``battery_level``,
  ``temperature``, ``roll``, ``pitch``, and ``compass``
  - What about ``$IIXDR,C,20,C,TempAir``? -- https://forum.arduino.cc/t/nmea0183-checksum/559531
- [o] Unlock adjusting offset and calibration values
- [o] Improve SignalK telemetry measurement ``path`` attributes,
  like ``electrical.batteries.99``
- [o] Add more software tests
- [o] Improve inline documentation
- [o] Improve "naming things"
- [o] Make everything configurable
- [o] Add SignalK WebSocket client
