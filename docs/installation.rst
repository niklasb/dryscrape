.. highlight:: none

Installation
============

First, get a copy of dryscrape_ using Git:

::

  $ git clone https://github.com/niklasb/dryscrape.git dryscrape
  $ cd dryscrape

To install dryscrape, you first need to install its dependencies. These are:

* lxml_
* webkit-server_

You can use pip_ to do this for you (while still in
the dryscrape directory). The ``#`` indicates that you need root privileges for
this:

::

  # pip -r requirements.txt

If you want, you can of course also install the dependencies manually.

Afterwards, you can use the ``setup.py`` script included to install dryscrape:

::

  # python setup.py install

Note that dryscrape is written for Python 2.7+, so make sure that you use both the
``python`` and ``pip`` commands in the right version.

.. _lxml: http://lxml.de/
.. _webkit-server: https://github.com/niklasb/webkit-server/
.. _pip: http://pypi.python.org/pypi/pip
.. _dryscrape: https://github.com/niklasb/dryscrape/
