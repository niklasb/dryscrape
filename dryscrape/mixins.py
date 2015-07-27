"""
Mixins for use in dryscrape drivers.
"""

import time
import lxml.html

class SelectionMixin(object):
  """ Mixin that adds different methods of node selection to an object that
  provides an ``xpath`` method returning a collection of matches. """

  def css(self, css):
    """ Returns all nodes matching the given CSSv3 expression. """
    return self.css(css)

  def at_css(self, css):
    """ Returns the first node matching the given CSSv3
    expression or ``None``. """
    return self._first_or_none(self.css(css))

  def at_xpath(self, xpath):
    """ Returns the first node matching the given XPath 2.0 expression or ``None``.
    """
    return self._first_or_none(self.xpath(xpath))

  def parent(self):
    """ Returns the parent node. """
    return self.at_xpath('..')

  def children(self):
    """ Returns the child nodes. """
    return self.xpath('*')

  def form(self):
    """ Returns the form wherein this node is contained or ``None``. """
    return self.at_xpath("ancestor::form")

  def _first_or_none(self, list):
    return list[0] if list else None


class AttributeMixin(object):
  """ Mixin that adds ``[]`` access syntax sugar to an object that supports a
  ``set_attr`` and ``get_attr`` method. """

  def __getitem__(self, attr):
    """ Syntax sugar for accessing this node's attributes """
    return self.get_attr(attr)

  def __setitem__(self, attr, value):
    """ Syntax sugar for setting this node's attributes """
    self.set_attr(attr, value)


class HtmlParsingMixin(object):
  """ Mixin that adds a ``document`` method to an object that supports a ``body``
  method returning valid HTML. """

  def document(self):
    """ Parses the HTML returned by ``body`` and returns it as an lxml.html
    document. If the driver supports live DOM manipulation (like webkit_server
    does), changes performed on the returned document will not take effect. """
    return lxml.html.document_fromstring(self.body())


# default timeout values
DEFAULT_WAIT_INTERVAL = 0.5
DEFAULT_WAIT_TIMEOUT = 10
DEFAULT_AT_TIMEOUT = 1

class WaitTimeoutError(Exception):
  """ Raised when a wait times out """

class WaitMixin(SelectionMixin):
  """ Mixin that allows waiting for conditions or elements. """

  def wait_for(self,
               condition,
               interval = DEFAULT_WAIT_INTERVAL,
               timeout  = DEFAULT_WAIT_TIMEOUT):
    """ Wait until a condition holds by checking it in regular intervals.
    Raises ``WaitTimeoutError`` on timeout. """

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
    raise WaitTimeoutError("wait_for timed out")

  def wait_for_safe(self, *args, **kw):
    """ Wait until a condition holds and return
    ``None`` on timeout. """
    try:
      return self.wait_for(*args, **kw)
    except WaitTimeoutError:
      return None

  def wait_while(self, condition, *args, **kw):
    """ Wait while a condition holds. """
    return self.wait_for(lambda: not condition(), *args, **kw)

  def at_css(self, css, timeout = DEFAULT_AT_TIMEOUT, **kw):
    """ Returns the first node matching the given CSSv3 expression or ``None``
    if a timeout occurs. """
    return self.wait_for_safe(lambda: super(WaitMixin, self).at_css(css),
                              timeout = timeout,
                              **kw)

  def at_xpath(self, xpath, timeout = DEFAULT_AT_TIMEOUT, **kw):
    """ Returns the first node matching the given XPath 2.0 expression or ``None``
    if a timeout occurs. """
    return self.wait_for_safe(lambda: super(WaitMixin, self).at_xpath(xpath),
                              timeout = timeout,
                              **kw)
