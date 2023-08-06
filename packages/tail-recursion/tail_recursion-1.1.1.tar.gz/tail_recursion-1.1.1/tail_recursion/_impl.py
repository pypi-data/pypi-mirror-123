


class TailRecursion:
    """
    Return an instance of this class to signal that you want to do a tail-recursive call.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_recursive(f):
    """
    Decorate the function you want to do tail-recursive calls in with this decorator.

    Use `return TailRecursion(your_args)` to do a tail recursion.
    """

    def wrapped(*args, **kwargs):
        args = args
        kwargs = kwargs
        while True:
            res = f(*args, **kwargs)
            if isinstance(res, TailRecursion):
                args = res.args
                kwargs = res.kwargs
            else:
                return res

    return wrapped
