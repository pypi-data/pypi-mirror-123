"""
Decorator for tail recursive calls.


How to use:

- Decorate your function with `@tail_recursive`
- Return a `TailRecursion` instance if you want to do a tail recursive call
  of the function being decorated
- Return anything else will terminate the function


Note:

This package doesn't support non-tail recursive calls.

Sometimes you can add the state to function arguments to make it tail-recursive,
if this cannot be easily done, you still need to use loops.


Example:

```
# The following example returns the cumulative sums of a list.

from typing import List

@tail_recursive
def cum_sum(xs: List[int], sums: List[int], cur_sum: int):
    if not xs:
        # all of xs is consumed, returning the result, i.e. sums.
        # this will terminate the whole function.
        return sums
    else:
        # consume the head of the list
        h = xs[0]
        t = xs[1:]
        cur_sum += h
        sums.append(cur_sum)

        # this return is semantically equivalently to:
        #     return cum_sum(t, sums, cur_sum)
        # the function call is replaced with a TailRecursion instance
        # to avoid overflow the stack, or by-pass the recursion limit
        return TailRecursion(t, sums, cur_sum)

assert cum_sum([2, 3, 5, 7, 11], [], 0) == [2, 5, 10, 17, 28]
```
"""

__version__ = '1.0.1'

from ._impl import TailRecursion
from ._impl import tail_recursive