import urlparse

class Session(object):
  """ A web scraping session based on a driver
  instance. Implements the proxy pattern to pass
  unresolved method calls to the underlying driver.

  If the `driver` argument is None, the instance
  will call the `get_default_driver` method on itself
  to get a driver instance (should be implemented by
  subclasses).

  If the `base_url` is present, relative URLs are
  completed with this URL base. If not, the `get_base_url`
  method is called on itself to get the base URL. """

  def __init__(self,
               driver = None,
               base_url = None):
    self.driver = driver or self.get_default_driver()

    try:
      self.base_url = base_url or self.get_base_url()
    except AttributeError:
      self.base_url = None

  # implement proxy pattern
  def __getattr__(self, attr):
    """ Pass unresolved method calls to underlying driver """
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
