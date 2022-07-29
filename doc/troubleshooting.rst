##################################
calypso-anemometer troubleshooting
##################################


************************************************
Submitting telemetry data to ``255.255.255.255``
************************************************

Problem
=======
When using the option ``--target=udp+signalk+delta://255.255.255.255:4123``,
the program croaks with::

    PermissionError: [Errno 13] Permission denied

Solution
========
Currently, UDP broadcast is only supported for submitting NMEA-0183 sentences
to the network. So, when you are aiming to use UDP broadcast, you should
probably be using ``--target=udp+broadcast+nmea0183://255.255.255.255:10110``.
