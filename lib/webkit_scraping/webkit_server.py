"""
Python bindings for the webkit_server included in capybara-webkit
(https://github.com/niklasb/webkit-server)

Author: Niklas Baumstark (https://github.com/niklasb)
"""

import sys, os
import subprocess
import re
import socket
import atexit
import json

from time import time

import scraping

SERVER_EXEC = os.path.join(os.path.dirname(__file__),
                           "../../webkit_server/src/webkit_server")

class Server(object):
  """ Manages a Webkit server process. Implemented as a singleton,
  because webkit_server can handle multiple connections! """

  # this is a singleton!
  _instance = None
  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      cls._instance = super(Server, cls).__new__(
        cls, *args, **kwargs)
    return cls._instance

  def __init__(self, bin = SERVER_EXEC):
    """ Initializes a new server process by running the binary
    specified or using the default one. """
    self._server = subprocess.Popen([bin],
                                    stdin  = subprocess.PIPE,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
    self._port = int(re.search("port: (\d+)",
                               self._server.stdout.readline())
                       .group(1))

    # on program termination, kill the server instance
    atexit.register(self.kill)

  def kill(self):
    """ Kill the process. """
    self._server.terminate()

  def connect(self):
    """ Returns a new socket connection to this server. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", self._port))
    return sock


class NodeError(Exception):
  """ A problem occured within a Node instance method. """
  pass

class SelectionMixin:
  """ Implements a generic XPath selection for a class
  providing a _get_xpath_id_list and a get_driver
  method """

  def xpath(self, xpath):
    """ Finds another node by XPath originating at the
    current node """

    return [Node(self.get_driver(), id)
            for id in self._get_xpath_id_list(xpath).split(",")
            if id]


class Node(SelectionMixin, scraping.Node):
  """ Represents a DOM node in our Webkit session. """

  BOOL_ATTRIBUTES = ["checked", "disabled", "selected", "multiple"]

  def __init__(self, driver, id):
    """ Initializes a new node with the given driver instance
    (of type CommandsMixin) and a native ID that is used to
    identify the node when communicating with the server """
    self.driver = driver
    self.id = id

  def text(self):
    """ Returns the inner text (no HTML!) """
    return self._invoke("text")

  def get_attr(self, name):
    """ Returns the value of an attribute """
    value = self._invoke("attribute", name)
    if name in self.__class__.BOOL_ATTRIBUTES:
      return value == "true" or value == name
    else:
      return value

  def set_attr(self, name, value):
    """ Sets the value of an attribute """
    self.exec_script("node.setAttribute(%s, %s)" % (repr(name),
                                                    repr(value)))

  def value(self):
    """ Returns the node's value """
    if self.is_multi_select():
      return [opt.value()
              for opt in self.xpath(".//option")
              if opt["selected"]]
    else:
      return self._invoke("value")

  def set(self, value):
    """ Sets the node content to the given value
    (e.g. for input fields) """
    self._invoke("set", value)

  def path(self):
    """ Returns an XPath expression that uniquely
    identifies the current node. """
    return self._invoke("path")

  def submit(self):
    """ Submits a form node """
    self.eval_script("node.submit()")
    self.driver.wait()

  def eval_script(self, js):
    """ Evaluate arbitrary Javascript with the
    "node" variable bound to the current node """
    return self.driver.eval_script(self._build_script(js))

  def exec_script(self, js):
    """ Execute arbitrary Javascript with the
    "node" variable bound to the current node """
    self.driver.exec_script(self._build_script(js))

  def _build_script(self, js):
    return "var node = Capybara.nodes[%s]; %s;" % (self.id, js)

  def select_option(self):
    """ Selects an option node """
    self._invoke("selectOption")

  def unselect_options(self):
    """ Unselects an option node (only possible within a
    multi-select) """
    if self.xpath("ancestor::select")[0].is_multi_select():
      self._invoke("unselectOption")
    else:
      raise NodeError, "Unselect not allowed."

  def click(self):
    """ Clicks the current node """
    self._invoke("click")
    self.driver.wait()

  def drag_to(self, element):
    """ Drag the node to another one """
    self._invoke("dragTo", element.id)

  def tag_name(self):
    """ Returns the tag name of the current node """
    return self._invoke("tagName")

  def is_visible(self):
    """ Checks whether the current node is visible """
    return self._invoke("visible") == "true"

  def is_attached(self):
    """ Checks whether the current node is actually existing
    on the currently active web page """
    return self._invoke("isAttached") == "true"

  def is_selected(self):
    """ is the "selected" attribute set for this node? """
    return self["selected"]

  def is_checked(self):
    """ is the "checked" attribute set for this node? """
    return self["checked"]

  def is_disabled(self):
    """ is the "disabled" attribute set for this node? """
    return self["disabled"]

  def is_multi_select(self):
    """ is this node a multi-select? """
    return self.tag_name() == "select" and self["multiple"]

  def get_driver(self):
    """ Returns which driver should be associated
    with a newly created node. """
    return self.driver

  def _get_xpath_id_list(self, xpath):
    """ Implements a mechanism to get a list
    of node IDs for an relative XPath query """
    return self._invoke("findWithin", xpath)

  def __repr__(self):
    return "<Node #%s>" % self.path()

  def _invoke(self, cmd, *args):
    return self.driver.issue_node_cmd(cmd, self.id, *args)


class CommandsMixin(SelectionMixin, scraping.Driver):
  """ A collection of commands
  that operate on a Webkit client instance exposing a
  "issue_command" function """

  def visit(self, url):
    """ Goes to a given URL """
    self.issue_command("Visit", url)

  def body(self):
    """ Returns the current DOM as HTML """
    return self.issue_command("Body")

  def source(self):
    """ Returns the source of the page as it was originally
    served by the web server """
    return self.issue_command("Source")

  def wait(self):
    """ Wait for the current page to load """
    self.issue_command("Wait")

  def url(self):
    """ Returns the current location """
    return self.issue_command("Url")

  def set_header(self, key, value):
    """ Sets a HTTP header for future requests """
    self.issue_command("Header", key, value)

  def reset(self):
    """ Resets the current web session """
    self.issue_command("Reset")

  def status_code(self):
    """ Returns the numeric HTTP status of the last
    response """
    return int(self.issue_command("Status"))

  def headers(self):
    """ Returns a dict of the last HTTP response headers """
    return dict([tuple(header.split(": ", 1))
                 for header in self.issue_command("Headers")
                                   .split("\n")])

  def eval_script(self, expr):
    """ Evaluates a piece of Javascript in the context
    of the current page and returns its value """
    ret = self.issue_command("Evaluate", expr)
    return json.loads("[%s]" % ret)[0]

  def exec_script(self, script):
    """ Executes a piece of Javascript in the context
    of the current page """
    self.issue_command("Execute", script)

  def render(self, path, width = 1024, height = 1024):
    """ Renders the current page to a file (viewport size
    in pixels) """
    self.issue_command("Render", path, width, height)

  def set_viewport_size(self, width, height):
    """ Sets the viewport size """
    self.issue_command("SetViewportSize", width, height)

  def set_cookie(self, cookie):
    """ Sets a cookie for future requests (must be in correct
    cookie string format) """
    self.issue_command("SetCookie", cookie)

  def clear_cookies(self):
    """ Deletes all cookies """
    self.issue_command("ClearCookies")

  def cookies(self):
    """ Returns a list of all cookies in cookie string format """
    return [line.strip()
            for line in self.issue_command("GetCookies").split("\n")
            if line.strip()]

  def set_attribute(self, attr, value = True):
    """ Sets a custom attribute for our Webkit instance.
    Possible attributes are:

      * auto_load_images
      * dns_prefetch_enabled
      * plugins_enabled
      * private_browsing_enabled
      * javascript_can_open_windows
      * javascript_can_access_clipboard
      * offline_storage_database_enabled
      * offline_web_application_cache_enabled
      * local_storage_enabled
      * local_storage_database_enabled
      * local_content_can_access_remote_urls
      * local_content_can_access_file_urls
      * accelerated_compositing_enabled
      * site_specific_quirks_enabled

    For all those options, `value` must be a boolean.
    """
    value = "true" if value else "false"
    self.issue_command("SetAttribute",
                       self._normalize_attr(attr),
                       value)

  def reset_attribute(self, attr):
    """ Resets a custom attribute. """
    self.issue_command("SetAttribute",
                       self._normalize_attr(attr),
                       "reset")

  def set_html(self, html, url = None):
    """ Sets custom HTML in our Webkit session
    and allows to specify a fake URL. Scripts and CSS
    is dynamically fetched with the given URL as the reference point
    and executed. """
    if url:
      self.issue_command(html, url)
    else:
      self.issue_command(html)

  def set_proxy(self, host     = "localhost",
                      port     = 0,
                      user     = "",
                      password = ""):
    """ Sets a custom HTTP proxy to use for future requests """
    self.issue_command("SetProxy", host, port, user, password)

  def clear_proxy(self):
    """ Resets custom HTTP proxy (use none in future requests)"""
    self.issue_command("ClearProxy")

  def issue_node_cmd(self, *args):
    return self.issue_command("Node", *args)

  def get_driver(self):
    return self

  def _get_xpath_id_list(self, xpath):
    """ implements a mechanism to get a list
    of node IDs for an absolute XPath query """
    return self.issue_command("Find", xpath)

  def _normalize_attr(self, attr):
    """ Transforms a name like auto_load_images into AutoLoadImages
    (allow Webkit option names to blend in with Python naming) """
    return ''.join(x.capitalize() for x in attr.split("_"))


class WebkitNoResponseError(Exception):
  """ Raised when the Webkit server does not respond. """
  pass
class WebkitInvalidResponseError(Exception):
  """ Raised when the Webkit server signaled an error. """
  pass


class Driver(CommandsMixin):
  """ A TCP client for our Webkit server """

  def __init__(self):
    """ Initializes the client by connecting to our
    singleton server (starting it if necessary) """
    self._sock = Server().connect()

  def issue_command(self, cmd, *args):
    """ Send and receive a message to/from the server """
    self._writeline(cmd)
    self._writeline(str(len(args)))
    for arg in args:
      arg = str(arg)
      self._writeline(str(len(arg)))
      self._sock.send(arg)

    return self._read_response()

  def _read_response(self):
    """ Reads a complete response packet from
    the server """
    result = self._readline()
    if not result:
      raise WebkitNoResponseError, "No response received from server."

    if result != "ok":
      raise WebkitInvalidResponseError, self._read_message()

    return self._read_message()

  def _read_message(self):
    """ Reads a single size-annotated message
    from the server """
    size = int(self._readline())
    if size == 0:
      return ""
    else:
      return self._sock.recv(size)

  def _readline(self):
    """ Cheap implementation of a readline function
    that operates on our underlying socket """
    res = []
    while True:
      c = self._sock.recv(1)
      if c == "\n":
        return "".join(res)
      res.append(c)

  def _writeline(self, line):
    """ Writes a line to the underlying socket """
    self._sock.send(line + "\n")


if __name__ == "__main__":
  c = Driver()
  c.set_attribute("auto_load_images", False)
  start_time = time()
  c.visit("http://facebook.com/")
  print >>sys.stderr, time() - start_time
  print c.xpath("//div")[10].path()
