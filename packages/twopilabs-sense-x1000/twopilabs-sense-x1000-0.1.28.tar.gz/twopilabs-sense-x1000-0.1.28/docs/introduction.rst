Introduction
============


License
-------
The 2πSENSE X1000 series control packages are release under a free software license (LGPLv3) which grants you the following rights:
  - Install and use this package by installing from the Python Packaging Index (PyPI, e.g. via ``pip``)
  - Distribute your own (possibly closed-source) application using this package as long as the package is not included with it
In addition these are your obligations:
  - When you distribute the package with your application (or on its own), you need to include source code for the library.
  - In case you modify (and redistribute) the package, We would like you to feed-back your modifications upstream to 2π-LABS GmbH.

You can find more information on the websites of the FSF `here <https://www.gnu.org/licenses/lgpl-3.0.en.html>`_.

Requirements
------------
This package is tested under Windows, MacOS and Linux operating systems and requires Python 3.6 or later.

Installation
------------
Use ``pip`` to install the package from the Python Packaging Index (PyPI) on the command line::

    python -m pip install twopilabs-sense-x1000 # or 'python3'

Basic Usage
-----------
The package is imported as follows:

    >>> from twopilabs.sense.x1000 import SenseX1000

Discover and open the first found device:


    >>> devices = SenseX1000.find_devices() # Discover devices using mDNS, USB, etc...
    >>> with SenseX1000.open_device(devices[0]) as device:
    >>>     print(device.core.idn()) # Print the SCPI *IDN? output

See :ref:`section-examples` for more complex usage patterns and the :ref:`API reference <section-apiref>`.
