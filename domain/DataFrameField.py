import mongoengine.fields 
from numpy import generic
from pandas import DataFrame, MultiIndex

class DataFrameField(mongoengine.fields.DictField):
    """A pandas DataFrame field.
    Looks to the outside world like a Pandas.DataFrame, but stores
    in the database as an using Pandas.DataFrame.to_dict("list").
    """
    def __init__(self, orient="list", *args, **kwargs):
        if orient not in ('dict', 'list', 'series', 'split', 'records', 'index'):
            raise ValueError(u"orient must be one of ('dict', 'list', 'series', 'split', 'records', 'index') but got: %s")
        self.orient = orient
        super(DataFrameField, self).__init__(*args, **kwargs)
    def __get__(self, instance, owner):
        print("__get__:",instance, owner)
        return DataFrame.from_dict(_as_native(super(DataFrameField, self).__get__(instance, owner)))
    def __set__(self, instance, value):
        if value is None or isinstance(value, dict):
            return super(DataFrameField, self).__set__(instance, value)
        if not isinstance(value, DataFrame):
            raise ValueError("value is not a pandas.DataFrame instance")
        if isinstance(value.index, MultiIndex):
            self.error(u'value.index is a MultiIndex; MultiIndex objects may not be stored in MongoDB.  Consider using `value.reset_index()` to flatten')
        if isinstance(value.keys(), MultiIndex):
            self.error(u'value.keys() is a MultiIndex; MultiIndex objects may not be stored in MongoDB.  Consider using `value.unstack().reset_index()` to flatten')
        obj = value.to_dict(self.orient)
        # coerce numpy objects into python objects for lack of the BSON-numpy package on windows
        for col in obj.values():
            if len(col) and isinstance(col[0],generic):
                for i in range(len(col)):
                    col[i] = col[i].item()
        return super(DataFrameField, self).__set__(instance, obj)
    def to_python(self, value):
        return value	

# A helper function for coercing nested dicts and lists to python lists
# from mongoengine basedict and baselist (which throw Pandas for a loop)
def _as_native(x):
    if isinstance(x,dict):
        return dict([ (k,_as_native(v)) for k,v in x.items()])
    elif  isinstance(x,list):
        return [ _as_native(v) for v in x]
    else: 
        return x