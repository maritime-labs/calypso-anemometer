# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

setup(
    name="calypso-anemometer",
    version="0.5.1",
    author="Andreas Motl",
    author_email="andreas.motl@panodata.org",
    url="https://github.com/maritime-labs/calypso-anemometer",
    description="Python driver for the Calypso UP10 anemometer",
    long_description=README,
    download_url="https://pypi.org/project/calypso-anemometer/",
    packages=find_packages(),
    license="AGPL-3.0, EUPL-1.2",
    keywords=[
        "calypso",
        "up10",
        "ultrasonic",
        "anemometer",
        "ultrasonic-sensor",
        "ultrasonic-anemometry",
        "wind-meter",
        "nmea",
        "nmea-0183",
        "signalk",
        "signalk-plugin",
        "opencpn",
        "openplotter",
        "environmental-monitoring",
        "bluetooth",
        "bluetooth-le",
        "bluetooth-low-energy",
        "ble",
        "solar",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 4 - Beta",
        "Operating System :: Android",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
        "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Communications",
        "Topic :: Education :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Emulators",
        "Topic :: System :: Networking",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "calypso-anemometer = calypso_anemometer.cli:cli",
        ],
    },
    install_requires=[
        "bleak<1",
        "click<9",
    ],
    extras_require={
        "test": [
            "pytest<8",
            "pytest-asyncio<1",
            "pytest-mock<4",
            "pytest-cov<4",
        ],
        "fake": [
            "aiorate>1,<2;python_version>='3.7'",
        ],
    },
)
