from typing import Union, get_type_hints, Callable


def typecheck(func) -> Callable:
    """Type check functions with args/ kwargs and (optional) return type."""

    type_hints = get_type_hints(func)
    return_type = type_hints.get("return", type)
    if type_hints.get("return", None):
        del type_hints["return"]

    def inner(*args, **kwargs) -> return_type:
        args_c = len(args)

        return_kwargs: dict = {}
        return_args: set = set()
        # check for args and kwargs types #
        for i, (var, type_of) in enumerate(type_hints.items()):
            if i >= args_c:
                if isinstance(kwargs[var], type_of):
                    return_kwargs[var] = kwargs[var]
                    continue
            else:
                arg = args[i]
                if isinstance(arg, type_of):
                    return_args.add(arg)
                    continue
            raise TypeError(f"Wrong type for {var} with type {type_of}")

        function_return = func(*return_args, **return_kwargs)

        if not type_hints.get("return", None) and not isinstance(function_return, return_type):
            raise TypeError("Wrong return type of function")
        return function_return
    return inner


@typecheck
def main(y: str | int, x: str = "nice") -> None:
    print(">> main", x, y)


if __name__ == '__main__':
    main("1", x="50")
