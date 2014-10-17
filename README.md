## Note: Update to 0.9

I merged the upstream version of webkit-server, which fixes several
issues with page loading. This has the nice side effect that 
dryscrape is now somewhat more intelligent when it comes to waiting 
for dynamic contents to be loaded.

If you experience any regressions, please 
[open an issue](https://github.com/niklasb/dryscrape/issues/new).

Meanwhile you can always use the old version of webkit-server
and dryscrape using the tag `v0.8`.

# Changelog

* 0.9.1: Changed semantics of the `headers` function in
  a backwards-incompatible way: It now returns a list of (key, value)
  pairs instead of a dictionary.

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

# Supported Platforms

The library has been confirmed to work on the following platforms:

* Mac OS X 10.9 Mavericks
* Ubuntu Linux
* Arch Linux

Other unixoid systems should work just fine.

Windows is not officially supported, although it should work
just fine under [cygwin](https://www.cygwin.com/).

# Installation, Usage, API Docs

Documentation can be found at 
[dryscrape's ReadTheDocs page](http://readthedocs.org/docs/dryscrape/).

# Contact, Bugs, Contributions

If you have any problems with this software, don't hesitate to open an    
issue on [Github](https://github.com/niklasb/dryscrape) or open a pull 
request or write a mail to **niklas baumstark at Gmail**.
