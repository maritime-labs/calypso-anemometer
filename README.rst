.. image:: https://github.com/maritime-labs/calypso-anemometer/workflows/Tests/badge.svg
    :target: https://github.com/maritime-labs/calypso-anemometer/actions?workflow=Tests

.. image:: https://codecov.io/gh/maritime-labs/calypso-anemometer/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/maritime-labs/calypso-anemometer
    :alt: Test suite code coverage

.. image:: https://pepy.tech/badge/calypso-anemometer/month
    :target: https://pypi.org/project/calypso-anemometer/

.. image:: https://img.shields.io/pypi/v/calypso-anemometer.svg
    :target: https://pypi.org/project/calypso-anemometer/

.. image:: https://img.shields.io/pypi/status/calypso-anemometer.svg
    :target: https://pypi.org/project/calypso-anemometer/

.. image:: https://img.shields.io/pypi/pyversions/calypso-anemometer.svg
    :target: https://pypi.org/project/calypso-anemometer/

.. image:: https://img.shields.io/pypi/l/calypso-anemometer.svg
    :target: https://github.com/maritime-labs/calypso-anemometer/blob/main/LICENSE

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

Pictures:

.. figure:: https://user-images.githubusercontent.com/453543/182049443-385c2a79-621e-41a3-b5ef-ee61f9c14b11.png
    :alt: Calypso UP10
    :target: `Calypso UP10 full size images`_

    Calypso UP10.

Resources:

- `Product page <https://calypsoinstruments.com/shop/product/ultrasonic-portable-solar-wind-meter-2>`_
- `Data sheet <https://calypsoinstruments.com/web/content/39971?access_token=09db51b3-1ad2-4900-b687-fae6c996fbd0&unique=293e2d5d7c89c38f45731af5c582a49de51ef64c&download=true>`_
- `Instruction's manual <https://calypsoinstruments.com/web/content/39973?access_token=a4fb3216-7abd-483d-b2d5-129e86d54142&unique=eb0f37d09f58423b9cac15d4dfa2ecd93d7d5bb3&download=true>`_
- `User manual <https://www.r-p-r.co.uk/downloads/calypso/Ultrasonic_Portable_User_Manual_EN.pdf>`_
- `Developer manual <https://www.instrumentchoice.com.au/attachment/download/81440/5f62c29c10d3c987351591.pdf>`_


Software library
================

The device driver library is written in Python, based on the `Bleak`_ library.
It was verified to work well on an OpenPlotter installation on a Raspberry Pi,
as well as a macOS workstation.


********
Features
********

- Run device discovery
- Acquire device status and readings (one shot)
- Acquire device readings continuously (subscribe/notify)
- Set device data rate
- Telemetry with NMEA-0183 and SignalK over UDP


*****
Setup
*****
::

    pip install --upgrade calypso-anemometer

To install the latest development version from the repository, invoke::

    pip install --upgrade git+https://github.com/maritime-labs/calypso-anemometer


*****************
Pre-flight checks
*****************

We have some documentation about investigating and configuring your Bluetooth/BLE
stack and about simulating the telemetry messaging. On this matter, you might want
to run through a sequence of `preflight checks`_ before going into `production`_.


*****
Usage
*****


Command line
============

Discover the ``ULTRASONIC`` BLE device and run a conversation on it. By
default, the Bluetooth adapter ``hci0`` will be used.

::

    # Get device information with discovery.
    calypso-anemometer info

    # Get device reading.
    calypso-anemometer read

    # Get device readings, continuously at 4 Hz (default).
    calypso-anemometer read --subscribe

    # Get device readings, continuously at 1 Hz.
    calypso-anemometer read --subscribe --rate=hz_1

    # Generate fake device readings, continuously at 8 Hz.
    pip install --upgrade calypso-anemometer[fake]
    calypso-anemometer fake --subscribe --rate=hz_8

If you already discovered your device, know its address, and want to connect
directly without automatic device discovery, see `skip discovery`_.

Likewise, when your system has multiple Bluetooth adapters, you may want to
choose a specific one, see `select Bluetooth adapter`_.

::

    # Get device information w/o discovery.
    calypso-anemometer info --ble-address=F8:C7:2C:EC:13:D0

    # Get device information w/o discovery, using a specific Bluetooth adapter.
    calypso-anemometer info --ble-adapter=hci1 --ble-address=F8:C7:2C:EC:13:D0


Library
=======

In order to use the library API, please consult the programs in the
``examples`` folder.

Synopsis::

    from calypso_anemometer.core import CalypsoDeviceApi

    async with CalypsoDeviceApi() as calypso:
        reading = await calypso.get_reading()
        reading.print()



***************
Telemetry setup
***************

The program can optionally submit telemetry messages in different formats.


SignalK telemetry
=================

Continuously receive device readings and submit them in SignalK Delta Format via UDP::

    calypso-anemometer read --subscribe --rate=hz_1 --target=udp+signalk+delta://openplotter.local:4123

To make a `SignalK server`_ receive the data, create an "UDP receiver" data
connection on the `Server » Data Connections`_ dialog of your `OpenPlotter`_ instance.

.. figure:: https://user-images.githubusercontent.com/453543/178626096-04fcc1b6-dbfc-4317-815d-4f733fee4b67.png

    SignalK UDP receiver on port 4123.

NMEA-0183 telemetry
===================

Continuously receive device readings and submit them in NMEA-0183 format via UDP broadcast::

    calypso-anemometer read --subscribe --rate=hz_1 --target=udp+broadcast+nmea0183://255.255.255.255:10110

.. note::

    If you don't have **any** networking configured on your machine, just use
    ``localhost`` as target address.

To make `OpenCPN`_ receive the data, create a corresponding data connection
like outlined in those screenshots.

.. figure:: https://user-images.githubusercontent.com/453543/179416658-abb831b8-8e5a-46e1-8f82-4eb5655c7e0b.png

    Add NMEA-0183 UDP receiver on port 10110.

.. figure:: https://user-images.githubusercontent.com/453543/179367303-14e1b958-16ae-4bf8-b077-4f96d929e8b0.png

    Configured NMEA-0183 UDP receiver on port 10110.

An example NMEA-0183 sentence emitted is::

    $IIVWR,154.0,L,11.06,N,5.69,M,20.48,K*65


**************
Other projects
**************

- `signalk-calypso-ultrasonic`_ is a Signal K server plugin for the Calypso
  Ultrasonic wireless anemometer, written in JavaScript.

- `CalypsoUltrasonicAPI`_ is a library for the Calypso Ultrasonic Anemometer,
  written in Visual Basic .NET and Java, (also) for Android.


***************
Troubleshooting
***************

For helping you to find solutions for known problems, we are maintaining
a dedicated page at `troubleshooting`_. The topic range is from permission
errors to BLE timeouts.


****************
Acknowledgements
****************

- Kudos to `Henrik Blidh`_, `David Lechner`_, and contributors for conceiving
  and maintaining the excellent `Bleak`_ library.
- Special thanks to `Fabian Tollenaar`_ for creating `signalk-calypso-ultrasonic`_.


*******************
Project information
*******************

Contributions
=============

Every kind of contribution, feedback, or patch, is much welcome. `Create an
issue`_ or submit a patch if you think we should include a new feature, or to
report or fix a bug.

Development
===========

In order to setup a development environment on your workstation, please head over
to the `development sandbox`_ documentation. When you see the software tests succeed,
you should be ready to start hacking.

Resources
=========

- `Source code repository <https://github.com/maritime-labs/calypso-anemometer>`_
- `Documentation <https://github.com/maritime-labs/calypso-anemometer/blob/main/README.rst>`_
- `Python Package Index (PyPI) <https://pypi.org/project/calypso-anemometer/>`_

License
=======

The project is licensed under the terms of the GNU AGPL license.



.. _Bleak: https://github.com/hbldh/bleak
.. _Calypso UP10 full size images: https://user-images.githubusercontent.com/453543/182049424-9a249add-c94b-4077-91bf-c864f2ed0e95.png
.. _Calypso UP10 ultrasonic portable solar wind meter: https://calypsoinstruments.com/shop/product/ultrasonic-portable-solar-wind-meter-2
.. _CalypsoUltrasonicAPI: https://github.com/volkerpetersen/CalypsoUltrasonicAPI
.. _create an issue: https://github.com/maritime-labs/calypso-anemometer/issues
.. _David Lechner: https://github.com/dlech
.. _development sandbox: https://github.com/maritime-labs/calypso-anemometer/blob/main/doc/sandbox.rst
.. _Fabian Tollenaar: https://github.com/fabdrol
.. _Henrik Blidh: https://github.com/hbldh
.. _OpenCPN: https://opencpn.org/
.. _OpenPlotter: https://open-boat-projects.org/en/openplotter/
.. _preflight checks: https://github.com/maritime-labs/calypso-anemometer/blob/main/doc/preflight.rst
.. _production: https://github.com/maritime-labs/calypso-anemometer/blob/main/doc/production.rst
.. _select Bluetooth adapter: https://github.com/maritime-labs/calypso-anemometer/blob/main/doc/production.rst#multiple-bluetooth-adapters
.. _Server » Data Connections: http://openplotter.local:3000/admin/#/serverConfiguration/connections/-
.. _signalk-calypso-ultrasonic: https://github.com/decipherindustries/signalk-calypso-ultrasonic
.. _SignalK server: https://github.com/SignalK/signalk-server
.. _skip discovery: https://github.com/maritime-labs/calypso-anemometer/blob/main/doc/production.rst#device-discovery-vs-multiple-devices
.. _troubleshooting: https://github.com/maritime-labs/calypso-anemometer/blob/main/doc/troubleshooting.rst
