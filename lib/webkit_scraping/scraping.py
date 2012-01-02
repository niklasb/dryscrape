"""
Simple syntax sugar for web scraping drivers.

Author: Niklas Baumstark (https://github.com/niklasb)
"""

import urlparse
import time
from lxml.cssselect import css_to_xpath

class NodeSet(object):
  """ Base class for a collection of nodes that
  provides an xpath method returning a collection
  of Nodes """

  def css(self, css):
    """ Returns all nodes matching the given CSSv3
    expression """
    return self.xpath(css_to_xpath(css))

  def at_css(self, css):
    """ Returns the first node matching the given CSSv3
    expression or None """
    return self._first_or_none(self.css(css))

  def at_xpath(self, xpath):
    """ Returns the first node matching the given XPath 2.0
    expression or None """
    return self._first_or_none(self.xpath(xpath))

  def _first_or_none(self, list):
    return list[0] if list else None


class Node(NodeSet):
  """ Base class for a DOM node in our scraping framework """

  def __getitem__(self, attr):
    """ Syntax sugar for accessing this node's attributes """
    return self.get_attr(attr)

  def __setitem__(self, attr, value):
    """ Syntax sugar for setting this node's attributes """
    self.set_attr(attr, value)

  def form(self):
    """ Returns the form wherein this node is contained
    or None """
    return self.at_xpath("ancestor::form")


DEFAULT_WAIT_INTERVAL = 0.5
DEFAULT_WAIT_TIMEOUT = 10
DEFAULT_AT_TIMEOUT = 1

class WaitTimeoutError(Exception):
  """ Raised when a wait times out """

class Driver(NodeSet):
  """ Base class for a scraping driver """

  def wait_for(self,
               condition,
               interval = DEFAULT_WAIT_INTERVAL,
               timeout  = DEFAULT_WAIT_TIMEOUT):
    """ Wait until a condition holds """

    start = time.time()

    # at least execute the check once!
    while True:
      res = condition()
      if res:
        return res

      # timeout?
      if time.time() - start > timeout:
        break

      # wait a bit
      time.sleep(interval)

    # timeout occured!
    raise WaitTimeoutError, "wait_for timed out"

  def wait_for_safe(self, *args, **kw):
    """ Wait until a condition holds and return
    None on timeout """
    try:
      return self.wait_for(*args, **kw)
    except WaitTimeoutError:
      return None

  def wait_while(self, condition, *args, **kw):
    """ Wait while a condition holds """
    return self.wait_for(lambda: not condition(),
                         *args, **kw)

  def at_css(self, css, timeout = DEFAULT_AT_TIMEOUT, **kw):
    """ Returns the first node matching the given CSSv3
    expression or None if a timeout occurs """
    return self.wait_for_safe(lambda: super(Driver, self).at_css(css),
                              timeout = timeout,
                              **kw)

  def at_xpath(self, xpath, timeout = DEFAULT_AT_TIMEOUT, **kw):
    """ Returns the first node matching the given XPath 2.0
    expression or None if a timeout occurs """
    orig = super(Driver, self).at_xpath
    return self.wait_for_safe(lambda: super(Driver, self).at_xpath(xpath),
                              timeout = timeout,
                              **kw)


class Session(object):
  """ A web scraping session based on a driver
  instance. Realizes the proxy pattern to pass
  through messages it cannot handle by itself """

  def __init__(self,
               driver = None,
               base_url = None):
    """ Initializes a session object.

    If the `driver` argument is None, the instance
    will call the `get_default_driver` method on itself
    to get a driver instance (should be implemented by
    subclasses)

    If the `base_url` is present, relative URLs are
    completed with this URL base. If not, the `get_base_url`
    method is called on itself to get the base URL """
    self.driver = driver or self.get_default_driver()

    try:
      self.base_url = base_url or self.get_base_url()
    except AttributeError:
      self.base_url = None

  # implement proxy pattern
  def __getattr__(self, attr):
    return getattr(self.driver, attr)

  def visit(self, url):
    """ Passes through the URL to the driver
    after completing it using the instance's URL base. """
    return self.driver.visit(self.complete_url(url))

  def complete_url(self, url):
    """ Completes a given URL with this
    instances URL base """
    if self.base_url:
      return urlparse.urljoin(self.base_url, url)
    else:
      return url

  def interact(self):
    """ Drops the user into an interactive Python session
    with the "sess" variable set to the current session
    instance """
    import code
    code.interact(local={ 'sess' : self })
