.. highlight:: none

Installation
============

Prerequisites
-------------

Before installing dryscrape_, you need to install some software it depends on:

* Qt_, QtWebKit_
* lxml_
* pip_
* xvfb_ (necessary only if no other X server is available)

On Ubuntu you can do that with one command (the ``#`` indicates that you need
root privileges for this):

::

  # apt-get install qt5-default libqt5webkit5-dev build-essential \
                    python-lxml python-pip xvfb

Please note that Qt4 is also supported.

On Mac OS X, you can use Homebrew_ to install Qt and
easy_install_ to install pip_:

::

  # brew install qt
  # easy_install pip

On other operating systems, you can use pip_ to install lxml (though you might
have to install libxml and the Python headers first).

Recommended: Installing dryscrape from PyPI
-------------------------------

This is as simple as a quick

::

  # pip install dryscrape

Note that dryscrape supports Python 2.7 and 3 as of version 1.0.

Installing dryscrape from Git
-------------------------------

First, get a copy of dryscrape_ using Git:

::

  $ git clone https://github.com/niklasb/dryscrape.git dryscrape
  $ cd dryscrape

To install dryscrape, you first need to install webkit-server_. You can use
pip_ to do this for you (while still in the dryscrape directory).

::

  # pip install -r requirements.txt

If you want, you can of course also install the dependencies manually.

Afterwards, you can use the ``setup.py`` script included to install dryscrape:

::

  # python setup.py install

.. _Qt: http://www.qt.io
.. _QtWebKit: http://doc.qt.io/qt-5/qtwebkit-index.html
.. _lxml: http://lxml.de/
.. _webkit-server: https://github.com/niklasb/webkit-server/
.. _pip: http://pypi.python.org/pypi/pip
.. _dryscrape: https://github.com/niklasb/dryscrape/
.. _Homebrew: http://brew.sh/
.. _easy_install: https://pypi.python.org/pypi/setuptools
