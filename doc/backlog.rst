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


************
Iteration +2
************
- [o] Systemd unit, with installer
- [o] Day/night switching
- [o] Documentation about running in production
- [o] Turn off logging to STDOUT
- [o] Docs: Get rid of mentioning port 2000
- [o] Docs: Replace screenshot ``NMEA-0183 UDP receiver on port 2000``
- [o] CI: Run software tests on GHA
- [o] Make up ``NMEA-0183`` messages for other parameters ``battery_level``,
  ``temperature``, ``roll``, ``pitch``, and ``compass``
- [o] Unlock adjusting offset and calibration values


************
Iteration +3
************
- [o] Improve SignalK telemetry measurement ``path`` attributes,
  like ``electrical.batteries.99``
- [o] Add more software tests
- [o] Improve inline documentation
- [o] Improve "naming things"
- [o] Make everything configurable
- [o] Add SignalK WebSocket client
