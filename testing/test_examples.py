# -*- coding: utf-8 -*-
# (c) 2022 Andreas Motl <andreas.motl@panodata.org>
# License: GNU Affero General Public License, Version 3
from examples.calypso_telemetry_nmea0183 import calypso_nmea0183_telemetry_demo
from examples.calypso_telemetry_signalk import calypso_signalk_telemetry_demo


def test_telemetry_signalk_demo(caplog):
    calypso_signalk_telemetry_demo(port=64123)
    assert "Sending message to udp://localhost:64123" in caplog.text


def test_telemetry_nmea0183_demo(caplog):
    calypso_nmea0183_telemetry_demo(port=60110)
    assert (
        "Sending message to udp://255.255.255.255:60110\n"
        "$MLHDT,235.0,T*27\r\n"
        "$MLVWR,154.0,L,11.06,N,5.69,M,20.48,K*64\r\n"
        "$MLXDR,A,-60.0,D,PTCH#CAL,A,30.0,D,ROLL#CAL*75\r\n"
        "$MLXDR,C,33.0,C,AIRTEMP#CAL*6A\r\n"
        "$MLXDR,L,0.9,R,BATT#CAL*18" in caplog.messages
    )
