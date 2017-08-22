
**NOTE: This package is not actively maintained. It uses QtWebkit, which is end-of-life and probably doesn't get security fixes backported. Consider using a similar package like [Spynner](https://github.com/makinacorpus/spynner) instead.**


# Overview

**Author:** Niklas Baumstark



dryscrape is a lightweight web scraping library for Python. It uses a 
headless Webkit instance to evaluate Javascript on the visited pages. This 
enables painless scraping of plain web pages as well as Javascript-heavy 
“Web 2.0” applications like
Facebook.

It is built on the shoulders of
[capybara-webkit](https://github.com/thoughtbot/capybara-webkit)'s 
[webkit-server](https://github.com/niklasb/webkit-server). A big thanks goes 
to thoughtbot, inc. for building this excellent piece of software!

# Changelog

* 1.0: Added Python 3 support, small performance fixes, header names are now
  properly normalized. Also added the function `dryscrape.start_xvfb()` to
  easily start Xvfb.
* 0.9.1: Changed semantics of the `headers` function in
  a backwards-incompatible way: It now returns a list of (key, value)
  pairs instead of a dictionary.

# Supported Platforms

The library has been confirmed to work on the following platforms:

* Mac OS X 10.9 Mavericks and 10.10 Yosemite
* Ubuntu Linux
* Arch Linux

Other unixoid systems should work just fine.

Windows is not officially supported, although dryscrape should work
with [cygwin](https://www.cygwin.com/).

### A word about Qt 5.6

The 5.6 version of Qt removes the Qt WebKit module in favor of the new module Qt WebEngine. So far webkit-server has not been ported to WebEngine (and likely won't be in the near future), so Qt <= 5.5 is a requirement.

# Installation, Usage, API Docs

Documentation can be found at 
[dryscrape's ReadTheDocs page](http://dryscrape.readthedocs.io/).

Quick installation instruction for Ubuntu:

    # apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb
    # pip install dryscrape

# Contact, Bugs, Contributions

If you have any problems with this software, don't hesitate to open an
issue on [Github](https://github.com/niklasb/dryscrape) or open a pull
request or write a mail to **niklas baumstark at Gmail**.
