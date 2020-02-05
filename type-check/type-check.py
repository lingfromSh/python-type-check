#!/usr/bin/env python
# coding=utf-8

def type_check(func):
    _version = "0.1"
    """
    A decorator for type checking via getting func's type notes of params.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        spec = inspect.getfullargspec(func)
        arg_names = spec.args
        annotations = spec.annotations

        # Check type for kwargs
        for kwarg_name, kwarg_value in kwargs.items():
            if kwarg_name in annotations:
                if not isinstance(kwarg_value, annotations[kwarg_name]):
                    raise TypeError(
                        f"{kwarg_name} should be an instance of {annotations[kwarg_name]} but get an instance of {type(kwarg_value)}.")
                # Remove this key argument from annotations
                annotations.pop(kwarg_name)

        # Get type of arguments
        arg_types = [annotations[arg_name]
                     for arg_name in arg_names if arg_name in annotations]

        # Check types for args
        for arg_value, arg_type in zip(args, arg_types):
            if not isinstance(arg_value, arg_type):
                raise TypeError(
                    f"{arg_value} should be an instance of {arg_type}, but get an instance of {type(arg_value)}.")

        # Get type of return
        return_type = annotations.get("return", "Any")
        res = func(*args, **kwargs)
        # Ensure the result of func valid.
        if return_type == "Any":
            # do nothing
            ...
        elif return_type is None and res is not None:
            raise TypeError("return should be None.")
        elif return_type is not None and not isinstance(res, return_type):
            raise TypeError(
                f"return should be an instance of {return_type} but get an instance of {type(res)}.")
        return res

    return wrapper
