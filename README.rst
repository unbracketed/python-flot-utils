python-flot-utils
=================

Utilities for generating flot_ graphs within Python.

For example::

    >>> import pyflot 
    >>> f = pyflot.Flot() 
    >>> f.add_series([(1, 1), (2, 2), (3, 3)]) 
    >>> print f.series_json 
    [{"data": [[1, 1], [2, 2], [3, 3]]}]

In this simple example the ``series_json`` is a JSON string
in the format expected by ``flot``.

.. _flot: http://code.google.com/p/flot/
