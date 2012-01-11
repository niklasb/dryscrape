"""
Webkit driver for pyscrape. Uses the `webkit_server` module.
"""

import pyscrape.mixins
import webkit_server

class Node(webkit_server.Node, pyscrape.mixins.SelectionMixin,
                               pyscrape.mixins.AttributeMixin):
  def __init__(self, *args):
    super(Node, self).__init__(*args)

  def _create_node(self, id):
    return Node(self.driver, id)

class Driver(webkit_server.Driver, pyscrape.mixins.DriverMixin):
  def __init__(self):
    super(Driver, self).__init__()

  def _create_node(self, id):
    return Node(self, id)
