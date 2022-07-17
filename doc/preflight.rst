###############
Preflight notes
###############


***************
Bluetooth stack
***************

You will need a working Bluetooth/BLE stack.


Adapters
========

Occasionally, you will also have multiple Bluetooth adapters installed in your
system. This section outlines a few commands to discover the available adapters.

Enumerate Bluetooth adapters::

    hcitool dev
    Devices:
        hci1    F5:60:12:CC:82:0D
        hci0    11:2B:8E:EB:82:26

Enumerate USB devices::

    lsusb
    Bus 001 Device 004: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle (HCI mode)

Display information about two Bluetooth adapters::

    hciconfig hci0 name
    hci0:	Type: Primary  Bus: USB
        BD Address: 11:2B:8E:EB:82:26  ACL MTU: 310:10  SCO MTU: 64:8
        Name: 'openplotter #1'

    hciconfig hci1 name
    hci1:   Type: Primary  Bus: UART
        BD Address: F5:60:12:CC:82:0D  ACL MTU: 1021:8  SCO MTU: 64:1
        Name: 'openplotter'


Device
======

This section outlines a few commands to discover an ``ULTRASONIC`` device nearby.

Run a BLE device scan on a specific adapter using ``hcitool``::

    sudo hcitool -i hci0 lescan

Run a BLE device scan using Bleak::

    bleak-lescan -i hci0
    bleak-lescan -i hci1



****************************
NMEA-0183 telemetry over UDP
****************************

In order to simulate NMEA-0183 telemetry, you can use the ``socat`` program
to submit and receive NMEA-0183 sentences over UDP broadcast on the command line.

Install::

    {apt,yum,brew} install socat

Submit::

    echo '$IIVWR,045.0,L,12.6,N,6.5,M,23.3,K*52' | socat -u - udp-datagram:255.255.255.255:10110,bind=:56123,broadcast

Receive::

    while true; do socat -u udp-recvfrom:10110,reuseaddr,reuseport system:cat; sleep 0.05; done

.. note::

    To stop this process, hit CTRL+C two times in quick succession.

.. note::

    If you receive error messages like ``E bind(6, {LEN=0 AF=2 0.0.0.0:10110}, 16):
    Address already in use``, make sure no other process is listening on that port.
    For example, OpenCPN will have a listener configured on that port when running.

    Vice versa, take care to stop any ``socat`` processes listening on the designated
    port **before** starting OpenCPN. It will not croak with any error messages, but
    will just silently not receive anything.


*****************
Emulate telemetry
*****************

If you don't have a corresponding device on your desk, you can still use the
program to emulate parts of its functionality. For example, use the following
command to submit synthetic measurement readings as NMEA-0183 messages::

    calypso-anemometer fake --subscribe --rate=hz_8 --target=udp+broadcast+nmea0183://255.255.255.255:10110

