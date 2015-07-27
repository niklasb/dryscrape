from dryscrape.driver.webkit import Driver as DefaultDriver
try:
  import urlparse
except ImportError:
  import urllib
  urlparse = urllib.parse

class Session(object):
  """ A web scraping session based on a driver instance. Implements the proxy
  pattern to pass unresolved method calls to the underlying driver.

  If no `driver` is specified, the instance will create an instance of
  ``dryscrape.session.DefaultDriver`` to get a driver instance (defaults to
  ``dryscrape.driver.webkit.Driver``).

  If `base_url` is present, relative URLs are completed with this URL base.
  If not, the `get_base_url` method is called on itself to get the base URL. """

  def __init__(self,
               driver = None,
               base_url = None):
    self.driver = driver or DefaultDriver()
    self.base_url = base_url

  # implement proxy pattern
  def __getattr__(self, attr):
    """ Pass unresolved method calls to underlying driver. """
    return getattr(self.driver, attr)

  def visit(self, url):
    """ Passes through the URL to the driver after completing it using the
    instance's URL base. """
    return self.driver.visit(self.complete_url(url))

  def complete_url(self, url):
    """ Completes a given URL with this instance's URL base. """
    if self.base_url:
      return urlparse.urljoin(self.base_url, url)
    else:
      return url

  def interact(self, **local):
    """ Drops the user into an interactive Python session with the ``sess`` variable
    set to the current session instance. If keyword arguments are supplied, these
    names will also be available within the session. """
    import code
    code.interact(local=dict(sess=self, **local))
