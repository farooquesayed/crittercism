import inspect
import json
import os
from functools import wraps

__version__ = '0.7.1'

# These attributes will not conflict with any real python attribute
# They are added to the decorated tests method and processed later
# by the `ddt` class decorator.

DATA_ATTR = '%values'           # store the data the tests must run with
FILE_ATTR = '%file_path'        # store the path to JSON file
UNPACK_ATTR = '%unpack'         # remember that we have to unpack values
DDT_LIST_ATTR = '%ddt_list'     # remember that we have to unpack values


def unpack(func):
    """
    Method decorator to add unpack feature.

    """
    setattr(func, UNPACK_ATTR, True)
    return func


def ddt_list(func):
    """
    Method decorator to add lists, tuples and discts feature.

    """
    setattr(func, DDT_LIST_ATTR, True)
    return func


def data(*values):
    """
    Method decorator to add to your tests methods.

    Should be added to methods of instances of ``unittest.TestCase``.

    """
    def wrapper(func):
        setattr(func, DATA_ATTR, values)
        return func
    return wrapper


def file_data(value):
    """
    Method decorator to add to your tests methods.

    Should be added to methods of instances of ``unittest.TestCase``.

    ``value`` should be a path relative to the directory of the file
    containing the decorated ``unittest.TestCase``. The file
    should contain JSON encoded data, that can either be a list or a
    dict.

    In case of a list, each value in the list will correspond to one
    tests case, and the value will be concatenated to the tests method
    name.

    In case of a dict, keys will be used as suffixes to the name of the
    tests case, and values will be fed as tests data.

    """
    def wrapper(func):
        setattr(func, FILE_ATTR, value)
        return func
    return wrapper


def mk_test_name(name, value):
    """
    Generate a new name for the tests named ``name``, appending ``value`` according to value type

    """
    try:
        value_name = ""
        if isinstance(value, list) or isinstance(value, tuple):
            for item in value:
                value_name += str(item) + "_"  # make func name contain all data in the list or tuple
            value_name = value_name[:-1]  # ignore last '_'
        elif isinstance(value, dict):
            # in case of tests dict add only first key+value to the tests name
            value_name = "%s" % str(value.keys()[0])
        else:
            # in case of any other type use value as a string
            value_name = str(value)
        return "{0}_{1}".format(name, value_name)
    except UnicodeEncodeError:
        # fallback for python2
        return "{0}_{1}".format(
            name, value_name.encode('ascii', 'backslashreplace')
        )


def data_driven_test(cls):
    """
    Class decorator for subclasses of ``unittest.TestCase``.

    Apply this decorator to the tests case class, and then
    decorate tests methods with ``@data``.

    For each method decorated with ``@data``, this will effectively create as
    many methods as data items are passed as parameters to ``@data``.

    The names of the tests methods follow the pattern ``test_func_name
    + "_" + str(data)``. If ``data.__name__`` exists, it is used
    instead for the tests method name.

    For each method decorated with ``@file_data('test_data.json')``, the
    decorator will try to load the test_data.json file located relative
    to the python file containing the method that is decorated. It will,
    for each ``test_name`` key create as many methods in the list of values
    from the ``data`` key.

    The names of these tests methods follow the pattern of
    ``test_name`` + str(data)``

    """

    def feed_data(func, new_name, *args, **kwargs):
        """
        This internal method decorator feeds the tests data item to the tests.

        """
        @wraps(func)
        def wrapper(self):
            return func(self, *args, **kwargs)
        wrapper.__name__ = new_name
        return wrapper

    def add_test(test_name, func, *args, **kwargs):
        """
        Add a tests case to this class.

        The tests will be based on an existing function but will give it a new
        name.

        """
        setattr(cls, test_name, feed_data(func, test_name, *args, **kwargs))

    def process_file_data(name, func, file_attr):
        """
        Process the parameter in the `file_data` decorator.

        """
        cls_path = os.path.abspath(inspect.getsourcefile(cls))
        data_file_path = os.path.join(os.path.dirname(cls_path), file_attr)

        def _raise_ve(*args):
            raise ValueError("%s does not exist" % file_attr)

        if os.path.exists(data_file_path) is False:
            test_name = mk_test_name(name, "error")
            add_test(test_name, _raise_ve, None)
        else:
            data = json.loads(open(data_file_path).read())
            for elem in data:
                if isinstance(data, dict):
                    key, value = elem, data[elem]
                    test_name = mk_test_name(name, key)
                elif isinstance(data, list):
                    value = elem
                    test_name = mk_test_name(name, value)
                add_test(test_name, func, value)

    for name, func in list(cls.__dict__.items()):
        if hasattr(func, DATA_ATTR):
            for v in getattr(func, DATA_ATTR):
                test_name = mk_test_name(name, getattr(v, "__name__", v))
                if hasattr(func, UNPACK_ATTR):
                    if isinstance(v, tuple) or isinstance(v, list):
                        add_test(test_name, func, *v)
                    else:
                        # unpack dictionary
                        add_test(test_name, func, **v)
                elif hasattr(func, DDT_LIST_ATTR):
                    if isinstance(v, tuple) or isinstance(v, list):
                        for i in v:
                            test_name = mk_test_name(name, getattr(v, "__name__", i))
                            if isinstance(i, tuple) or isinstance(i, list):
                                add_test(test_name, func, *i)
                            elif isinstance(i, dict):
                                add_test(test_name, func, **i)
                            else:
                                add_test(test_name, func, i)
                else:
                    add_test(test_name, func, v)
            delattr(cls, name)
        elif hasattr(func, FILE_ATTR):
            file_attr = getattr(func, FILE_ATTR)
            process_file_data(name, func, file_attr)
            delattr(cls, name)
    return cls
