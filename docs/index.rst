.. Python Flot Utils documentation master file, created by
   sphinx-quickstart on Thu Feb 17 16:27:52 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Easily Generate Flot Graphs Using Python
========================================

PyFlot makes it easy to generate flot_ graphs. Its primary goal is to
allow one to specify data inputs and options in a Python application 
and generate the appropriate JSON. Common uses of this will be rendering
into a template as flot() arguments or as the payload of an XHR response.
PyFlot takes care of all the annoying details of converting types to match
up with how `flot` expects them.


For example::

    >>> import pyflot 
    >>> graph = pyflot.Flot() 
    >>> graph.add_line([(1, 1), (2, 2), (3, 3)]) 
    >>> print graph.series_json 
    [{"data": [[1, 1], [2, 2], [3, 3]]}]

In this simple example the ``series_json`` is a JSON string
in the format expected by ``flot``.

The following Django template snippet shows how you might use 
it in a Django template:

.. code-block:: HTML+Django/Jinja

    <script id="source" language="javascript" type="text/javascript"> 
    $(function () {
        $.plot($("#linear-graph"), {{ graph.series_json|safe }}, {{ graph.options_json|safe }});
    });
    </script>     


.. _flot: http://code.google.com/p/flot/


.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

