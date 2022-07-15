.. image:: https://img.shields.io/pypi/pyversions/calypso-anemometer.svg
    :target: https://pypi.org/project/calypso-anemometer/

.. image:: https://img.shields.io/pypi/status/calypso-anemometer.svg
    :target: https://pypi.org/project/calypso-anemometer/

.. image:: https://img.shields.io/pypi/v/calypso-anemometer.svg
    :target: https://pypi.org/project/calypso-anemometer/

.. image:: https://pepy.tech/badge/calypso-anemometer/month
    :target: https://pypi.org/project/calypso-anemometer/

.. image:: https://img.shields.io/pypi/l/calypso-anemometer.svg
    :target: https://github.com/daq-tools/calypso-anemometer/blob/main/LICENSE

|

#############################################
Python driver for the Calypso UP10 anemometer
#############################################


*****
About
*****

Hardware device
===============

The `Calypso UP10 ultrasonic portable solar wind meter`_ is a Bluetooth, solar-powered,
pocket-sized, ultrasonic anemometer. No power cords or data wires needed.

Resources:

- `Product page <https://calypsoinstruments.com/shop/product/ultrasonic-portable-solar-wind-meter-2>`_
- `Data sheet <https://calypsoinstruments.com/web/content/39971?access_token=09db51b3-1ad2-4900-b687-fae6c996fbd0&unique=293e2d5d7c89c38f45731af5c582a49de51ef64c&download=true>`_
- `Instruction's manual <https://calypsoinstruments.com/web/content/39973?access_token=a4fb3216-7abd-483d-b2d5-129e86d54142&unique=eb0f37d09f58423b9cac15d4dfa2ecd93d7d5bb3&download=true>`_
- `User manual <https://www.r-p-r.co.uk/downloads/calypso/Ultrasonic_Portable_User_Manual_EN.pdf>`_
- `Developer manual <https://www.instrumentchoice.com.au/attachment/download/81440/5f62c29c10d3c987351591.pdf>`_

Software library
================

The device driver library is written in Python and based on the `Bleak`_
library, the *Bluetooth Low Energy platform Agnostic Klient for Python*.
It was verified to work well on a Raspberry Pi / OpenPlotter installation and a
macOS workstation.


********
Features
********

- Device discovery
- Basic conversation
- Acquire device status and readings (one shot)
- Acquire device readings continuously (subscribe/notify)
- Set device data rate
- Telemetry: NMEA-0183 and SignalK over UDP


*****
Setup
*****
::

    pip install calypso-anemometer

To install the latest development version from the repository, invoke::

    pip install git+https://github.com/daq-tools/calypso-anemometer


********
Synopsis
********

Usage
=====

Discover the ``ULTRASONIC`` BLE device and run a conversation on it::

    # Get device information.
    calypso-anemometer info

    # Get device reading.
    calypso-anemometer read

    # Get device readings, continuously at 4 Hz (default).
    calypso-anemometer read --subscribe

    # Get device readings, continuously at 1 Hz.
    calypso-anemometer read --subscribe --rate=hz_1

    # Continuously receive device readings and submit them in SignalK Delta Format via UDP.
    # See section "SignalK telemetry" about how to create an UDP receiver
    # data connection in your Signal K server beforehand.
    calypso-anemometer read --subscribe --rate=hz_1 --target=udp+signalk+delta://openplotter.local:4123

    # Continuously receive device readings and submit them in NMEA-0183 format via UDP.
    # See section "NMEA-0183 telemetry" about how to create an UDP receiver
    # data connection in OpenCPN beforehand.
    calypso-anemometer read --subscribe --rate=hz_1 --target=udp+broadcast+nmea0183://openplotter.local:10110

If you already discovered your device and know its address, use the
``CALYPSO_ADDRESS`` environment variable to skip discovery, saving a few cycles::

    # Linux
    export CALYPSO_ADDRESS=E7:B6:1B:DB:02:DF

    # macOS
    export CALYPSO_ADDRESS=FB2D3935-AEBA-41D4-AB46-CD0C5FB291A1

    # Activate discovery again.
    unset CALYPSO_ADDRESS

Development
===========
::

    # Set device data rate to one of HZ_1, HZ_4, or HZ_8.
    # Note: Works only for the upcoming conversation. Will be back at HZ_4 afterwards.
    calypso-anemometer set-option --rate=hz_1

    # Set device mode to one of SLEEP, LOW_POWER, or NORMAL.
    # Note: Does not work, the setting is read-only.
    calypso-anemometer set-option --mode=normal

    # Explore all services and characteristics. Useful for debugging purposes.
    calypso-anemometer explore


*****************
Pre-flight checks
*****************

You will need a working Bluetooth/BLE stack. This section outlines a few
commands to discover an ``ULTRASONIC`` device nearby.

Enumerate Bluetooth adapters::

    hcitool dev
    Devices:
        hci1    E4:5F:01:BB:71:FC
        hci0    00:1A:7D:DA:71:15

    lsusb
    Bus 001 Device 004: ID 0a12:0001 Cambridge Silicon Radio, Ltd Bluetooth Dongle (HCI mode)

Display information about two Bluetooth adapters::

    hciconfig hci0 name
    hci0:	Type: Primary  Bus: USB
        BD Address: 00:1A:7D:DA:71:15  ACL MTU: 310:10  SCO MTU: 64:8
        Name: 'openplotter #1'

    hciconfig hci1 name
    hci1:   Type: Primary  Bus: UART
        BD Address: E4:5F:01:BB:71:FC  ACL MTU: 1021:8  SCO MTU: 64:1
        Name: 'openplotter'

Run a BLE device scan on a specific adapter::

    sudo hcitool -i hci0 lescan

Run a BLE device scan using Bleak::

    bleak-lescan -i hci0
    bleak-lescan -i hci1


*****************
SignalK telemetry
*****************

The program can optionally submit telemetry data in SignalK Delta Format via UDP.
To make a `SignalK server`_ receive the data, create an "UDP receiver" data
connection on the `Server » Data Connections`_ dialog of your `OpenPlotter`_ instance.

.. figure:: https://user-images.githubusercontent.com/453543/178626096-04fcc1b6-dbfc-4317-815d-4f733fee4b67.png

    SignalK UDP receiver on port 4123.


*******************
NMEA-0183 telemetry
*******************

The program can optionally submit telemetry data in NMEA-0183 format via UDP.
To make `OpenCPN`_ receive the data, create a corresponding data connection
like outlined in this screenshot.

.. figure:: https://user-images.githubusercontent.com/453543/179080301-3244c579-b76f-4ace-b754-44bae8e572a6.png

    NMEA-0183 UDP receiver on port 2000.


***********
Development
***********
::

    git clone https://github.com/daq-tools/calypso-anemometer
    cd calypso-anemometer
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --editable=.


.. _Bleak: https://github.com/hbldh/bleak
.. _Calypso UP10 ultrasonic portable solar wind meter: https://calypsoinstruments.com/shop/product/ultrasonic-portable-solar-wind-meter-2
.. _OpenCPN: https://opencpn.org/
.. _OpenPlotter: https://open-boat-projects.org/en/openplotter/
.. _Server » Data Connections: http://openplotter.local:3000/admin/#/serverConfiguration/connections/-
.. _SignalK server: https://github.com/SignalK/signalk-server
