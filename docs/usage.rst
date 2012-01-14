Usage
======

First demonstration
------------------------

A code sample tells more than thousand words:

.. literalinclude:: /../examples/google.py

In this sample, we use dryscrape to do a simple web search on Google.
Note that we set up a Webkit driver instance here and pass it to a dryscrape
:py:class:`~dryscrape.session.Session` in the constructor. The session instance
then passes every method call it cannot resolve -- such as
:py:meth:`~webkit_server.CommandsMixin.visit`, in this case -- to the
underlying driver.

On my system and with a 16k downstream connection, this runs in under a second.

A more complex example
-------------------------

There was nothing much special about the example above. Let's look at a more
advanced example that actually works on a Javascript-only application: GMail.

.. literalinclude:: /../examples/gmail.py

This *just works*.

There are some things to note about it, though:

* :py:meth:`~dryscrape.mixins.DriverMixin.at_xpath` and
  :py:meth:`~dryscrape.mixins.DriverMixin.at_css` take an optional
  `timeout` argument that can be used to leave the application a bit of time
  to load content
* XPath_ is really useful, you should make yourself familiar with it. You can
  also use CSS, however.

.. _XPath: http://www.w3schools.com/xpath/
