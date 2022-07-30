# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from examples.calypso_telemetry_nmea0183 import calypso_nmea0183_telemetry_demo
from examples.calypso_telemetry_signalk import calypso_signalk_telemetry_demo


def test_telemetry_signalk_demo(caplog):
    calypso_signalk_telemetry_demo()
    assert "Sending message to udp://localhost:4123" in caplog.text


def test_telemetry_nmea0183_demo(caplog):
    calypso_nmea0183_telemetry_demo()
    assert "Sending message to udp://255.255.255.255:10110. $IIVWR,154.0,L,11.06,N,5.69,M,20.48,K*65" in caplog.messages