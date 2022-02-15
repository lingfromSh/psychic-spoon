import importlib
from inspect import getfullargspec
from functools import update_wrapper


def import_string(path: str):
    module_path, attr_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)


def multipledispatch(func):
    dispatch_cache = {}

    def get_cache_token(annotations):
        import copy
        annotations = copy.deepcopy(annotations)
        annotations.pop("return", None)
        return tuple(annotations.values())

    def register(cls, f=None):
        if f is not None:
            annotations = f.__annotations__
        else:
            annotations = cls.__annotations__
            f = cls

        cache_token = get_cache_token(annotations)
        dispatch_cache[cache_token] = f

    def dispatch(*args, **kwargs):
        cache_token = tuple(type(arg) for arg in args[1:]) + tuple(type(kwarg) for kwarg in kwargs.values())
        print(cache_token)
        print(dispatch_cache)
        if cache_token not in dispatch_cache:
            return dispatch_cache['default'](*args, **kwargs)
        return dispatch_cache[cache_token](*args, **kwargs)

    def wrapper(*args, **kwargs):
        return dispatch(*args, **kwargs)

    dispatch_cache['default'] = func
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.dispatch_cache = dispatch_cache
    update_wrapper(wrapper, func)
    return wrapper
