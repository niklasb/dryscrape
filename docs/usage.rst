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
