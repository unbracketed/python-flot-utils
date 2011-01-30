from functools import partial, wraps
import json


def as_json(fn):
    "Decorator that converts output of function to JSON string"
    import ipdb; ipdb.set_trace()
    @wraps(fn)
    def _json(fn):
        return json.dumps(fn())
    return _json


class DuplicateLabelException(Exception):
    """Exception raised when an attempt is made to 
    label a new series with a label already in use"""



class Flot(object):

    def __init__(self):
        self._series = []
        self._options = {}

    @property
#    @as_json
    def series_list(self):
        return json.dumps(self._series)

#    @property
#    @as_json
    def options(self):
        pass

    #add_bars
    #add_line
    #add_points
    def __getattr__(self, value):
        if value.startswith('add_'):
            return partial(self.add_series_type, value[4:])

    def add_series_type(self, type, series, label=None, **kwargs):
        method = getattr(self, 'add_series')
        return method(series, label, **{type: {'show': True}})

    def add_series(self, series, label=None, **kwargs):
        """
        A series is a list of pairs (2-tuples)
        """
        s = {'data': series}
        if label and label in [x.get('label', None) for x in self._series]:
            raise DuplicateLabelException
        elif label:
            s.update(label=label)
        for lt in ('bars', 'lines', 'points'):
            if lt in kwargs:
                s.update({lt: kwargs[lt]})
        self._series.append(s)


