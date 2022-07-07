# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

setup(
    name="calypso-anemometer",
    version="0.0.0",
    author="Andreas Motl",
    author_email="andreas.motl@panodata.org",
    url="https://github.com/daq-tools/calypso-anemometer",
    description="Python driver for Calypso UP10 anemometer",
    long_description=README,
    download_url="https://pypi.org/project/calypso-anemometer/",
    packages=find_packages(),
    license="AGPL-3.0, EUPL-1.2",
    keywords=[
        "calypso",
        "up10",
        "anemometer",
        "wind-meter",
        "environmental-monitoring",
        "bluetooth",
        "bluetooth-le"
        "bluetooth-low-energy",
        "ble",
        "solar",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
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
        ],
    },
    install_requires=[
        "bleak<1",
    ],
    extras_require={
    },
)
