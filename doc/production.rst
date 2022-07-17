################
Production notes
################


*************************************
Device discovery vs. multiple devices
*************************************

By default, the program will look for any BLE device called ``ULTRASONIC``
and will attempt to connect to the first one discovered.

While this will probably work in most environments, there is still a chance that
multiple devices with the same name are around and you will be connecting to the
wrong device. This scenario also applies when you are using multiple devices on
your own site.

In this case, make sure to shortcut the device discovery procedure by pinning the
BLE peripheral. For that purpose, you can use the ``CALYPSO_ADDRESS`` environment
variable, like::

    # Linux
    export CALYPSO_ADDRESS=F8:C7:2C:EC:13:D0

    # macOS
    export CALYPSO_ADDRESS=0C3E4A46-BFCB-52E5-BC57-DE1D60C3A2B2

In order to activate automatic device discovery again, invoke::

    unset CALYPSO_ADDRESS


*********************
Run as system service
*********************

TODO: ``systemd`` configuration needed.



*******************
Save power at night
*******************

TODO: ``systemd`` configuration snippets which stop the service at night.
