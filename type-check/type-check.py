#!/usr/bin/env python
# coding=utf-8
import inspect
from functools import wraps

def type_check(func):
    _version = "0.2"
    """
    A decorator for type checking via getting func's type notes of params.

    #version: 0.2
    Add type check support for typing,Union
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        spec = inspect.getfullargspec(func)
        arg_names = spec.args
        annotations = spec.annotations

        # Check type for kwargs
        for kwarg_name, kwarg_value in kwargs.items():
            if kwarg_name in annotations:
                if hasattr(annotations[kwarg_name], "__origin__") and annotations[kwarg_name].__origin__ == typing.Union:
                    for _type in annotations[kwarg_name].__args__:
                        if isinstance(kwarg_value, _type):
                            break
                    else:
                        raise TypeError(
                            f"{kwarg_name} should be an instance of {annotations[kwarg_name]}, but get an instance of {type(kwarg_value)}")
                elif not isinstance(kwarg_value, annotations[kwarg_name]):
                    raise TypeError(
                        f"{kwarg_name} should be an instance of {annotations[kwarg_name]}, but get an instance of {type(kwarg_value)}.")
                # Remove this key argument from annotations
                annotations.pop(kwarg_name)

        # Get type of arguments
        arg_types = [annotations[arg_name]
                     for arg_name in arg_names if arg_name in annotations]

        # Check types for args
        for arg_value, arg_type in zip(args, arg_types):
            if hasattr(arg_type, "__origin__") and arg_type.__origin__ == typing.Union:
                for _type in arg_type.__args__:
                    if isinstance(arg_value, _type):
                        break
                else:
                    raise TypeError(
                        f"{arg_value} should be an instance of {arg_type}, but get an instance of {type(arg_value)}.")
            elif not isinstance(arg_value, arg_type):
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
        elif return_type is not None:
            if hasattr(return_type, "__origin__") and return_type.__origin__ == typing.Union:
                for _type in return_type.__args__:
                    if isinstance(res, _type):
                        break
                else:
                    raise TypeError(f"return should be one kind of instance of {return_type} but get an instance of {type(res)}")
            elif not isinstance(res, return_type):
                raise TypeError(
                    f"return should be an instance of {return_type} but get an instance of {type(res)}.")
        return res

    return wrapper


if __name__ == "__main__":
    import typing
    @type_check
    def foo(a: int,b: str,c: typing.Union[str, int]) -> typing.Union[typing.Tuple, typing.AnyStr]:
        if a == 1:
            return a,b,c
        return "123"
    foo(1,'2',3)
