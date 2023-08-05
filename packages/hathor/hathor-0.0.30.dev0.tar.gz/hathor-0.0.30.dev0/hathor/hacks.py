def _endpoint_from_view_func(view_func):
    """Internal helper that returns the default endpoint for a given
    function.  This always is the function name.
    """
    assert view_func is not None, "expected view func if endpoint is not provided."
    return view_func.__name__


# noinspection SpellCheckingInspection
def patch_restx(endpoint_from_view_func: bool = True) -> None:
    """
    Nasty hacks are here

    :param endpoint_from_view_func: Add missing function into flask for backward compatibility with `flask-restx`
    """
    if endpoint_from_view_func:
        func_name = "_endpoint_from_view_func"
        try:
            import pkg_resources
            packages = pkg_resources.working_set.by_key
            if "flask" in packages and "flask-restx" in packages:
                flask_version = tuple(map(int, packages["flask"].version.split(".")))
                flask_restx_version = tuple(map(int, packages["flask-restx"].version.split(".")))
                if (2, 0, 0) <= flask_version and (1, 0, 0) > flask_restx_version:
                    import flask
                    if not hasattr(flask.helpers, func_name):
                        setattr(flask.helpers, func_name, _endpoint_from_view_func)
        except ImportError:
            print(f"skipping monkey patch of {func_name}")
