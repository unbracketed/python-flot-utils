import collections
from functools import partial
from itertools import chain
import inspect
import json
import os
import time


def update(d, u):
    """
    Recursively update nested dicts

    Credit: Alex Martelli
    """
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


class MissingDataException(Exception):
    """Exception raised when a series does not contain
    any data points"""


class DuplicateLabelException(Exception):
    """Exception raised when an attempt is made to 
    label a new series with a label already in use"""


class Flot(object):
    """
    Represents a ``flot`` graph

    This is a Python representation of a flot graph with the
    goal preserving the flot attribute names and organization
    of the options. A Flot instance will allow you to 
    use your Python data structures as is and will handle
    the details of converting to valid JSON with items 
    formatted properly for ``flot``. (Handy for time series
    for example)
    """

    def __init__(self):
        self._series = []
        self._options = {}

        #apply any options specified starting with the top
        #of the inheritance chain
        bases = list(inspect.getmro(self.__class__))
        bases.reverse()
        for base in bases:
            if hasattr(base, 'options'):
                update(self._options, base.options)

    @property
    def series_json(self):
        """
        Returns a string with each data series
        associated with this graph formatted as JSON, 
        suitable for passing to the ``$.plot`` method.
        """
        return json.dumps([self.prepare_series(s) for s in self._series])

    @property
    def options_json(self):
        """
        Returns a JSON string representing the global options
        for this graph in a format suitable for passing to 
        the ``$.plot`` method as the options parameter.
        """
        return json.dumps(self._options)

    def __getattr__(self, value):
        """
        add_bars
        add_line
        add_points
        
        provides shortcut methods for adding series using a particular line type
        """
        if value.startswith('add_'):
            return partial(self.add_series_type, value[4:])

    def add_series_type(self, line_type, series, label=None, **kwargs):
        method = getattr(self, 'add_series')
        return method(series, label, **{line_type: {'show': True}})

    def add_series(self, series, label=None, **kwargs):
        """
        A series is a list of pairs (2-tuples)
        """
        if not series:
            raise MissingDataException
        new_series = {'data': series}
        if label and label in [x.get('label', None) for x in self._series]:
            raise DuplicateLabelException
        elif label:
            new_series.update(label=label)
        for line_type in ('bars', 'line', 'points'):
            if line_type in kwargs:
                new_series.update({line_type: kwargs[line_type]})
        self._series.append(new_series)

    def add_time_series(self, series, label=None, **kwargs):
        """
        A specialized form of ``add_series`` for adding time-series data.

        Flot requires times to be specified in Javascript timestamp format.
        This convenience function lets you pass datetime instances and handles
        the conversion. It also sets the correct option to indicate to ``flot``
        that the graph should be treated as a time series
        """
        _series = [(int(time.mktime(ts.timetuple()) * 1000), val) \
                    for ts, val in series]
        self._options['xaxis'] = {'mode': 'time'}
        return self.add_series(_series, label, **kwargs)

    def calculate_bar_width(self):
        slices = max([len(s['data']) for s in self._series])
        xs = [pair[0] for pair in chain(*[s['data'] for s in self._series])]
        xmin, xmax = (min(xs), max(xs))
        w = xmax - xmin
        return float(w)/slices

    def get_test_page(self):
        """Renders a test page"""
        templatefile = open(os.path.join(
                                os.path.dirname(os.path.abspath(__file__)),
                                'templates', 
                                'test_page.html'))
        template = templatefile.read()
        template = template.replace("{{ graph.series_json|safe }}", 
                                    self.series_json)
        template = template.replace("{{ graph.options_json|safe }}", 
                                    self.options_json)
        out = open(os.path.join(os.getcwd(), 'testgraph.html'), 'w')
        out.write(template)
        out.close()

    def prepare_series(self, series):
        if 'bars' in series:
            w = self.calculate_bar_width()
            if w:
                series['bars']['barWidth'] = w
        return series
