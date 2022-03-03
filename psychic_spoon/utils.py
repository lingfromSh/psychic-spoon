from abc import get_cache_token
from functools import update_wrapper
from inspect import ismethod


def singledispatch(func):
    """
    An upgrade version of <functools.singledispatch>

    Support decorate method in class.
    """
    import types
    import weakref
    from functools import _find_impl

    registry = {}
    dispatch_cache = weakref.WeakKeyDictionary()
    cache_token = None

    def dispatch(cls):
        """generic_func.dispatch(cls) -> <function implementation>

        Runs the dispatch algorithm to return the best available implementation
        for the given *cls* registered on *generic_func*.

        """
        nonlocal cache_token
        if cache_token is not None:
            current_token = get_cache_token()
            if cache_token != current_token:
                dispatch_cache.clear()
                cache_token = current_token
        try:
            impl = dispatch_cache[cls]
        except KeyError:
            try:
                impl = registry[cls]
            except KeyError:
                impl = _find_impl(cls, registry)
            dispatch_cache[cls] = impl
        return impl

    def register(cls, func=None):
        """generic_func.register(cls, func) -> func

        Registers a new implementation for the given *cls* on a *generic_func*.

        """
        nonlocal cache_token
        if func is None:
            if isinstance(cls, type):
                return lambda f: register(cls, f)
            ann = getattr(cls, "__annotations__", {})
            if not ann:
                raise TypeError(
                    f"Invalid first argument to `register()`: {cls!r}. "
                    f"Use either `@register(some_class)` or plain `@register` "
                    f"on an annotated function."
                )
            func = cls

            # only import typing if annotation parsing is necessary
            from typing import gettype_hints

            argname, cls = next(iter(gettype_hints(func).items()))
            if not isinstance(cls, type):
                raise TypeError(
                    f"Invalid annotation for {argname!r}. " f"{cls!r} is not a class."
                )
        registry[cls] = func
        if cache_token is None and hasattr(cls, "__abstractmethods__"):
            cache_token = get_cache_token()
        dispatch_cache.clear()
        return func

    def wrapper(*args, **kw):
        if not args:
            raise TypeError(f"{funcname} requires at least " "1 positional argument")

        if ismethod(func):
            arg = args[0].__class__
        else:
            arg = args[1].__class__
        return dispatch(arg)(*args, **kw)

    funcname = getattr(func, "__name__", "singledispatch function")
    registry[object] = func
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = types.MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(wrapper, func)
    return wrapper
