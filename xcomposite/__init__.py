# MIT License
# Copyright (c) 2018 Michael Malinowski
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
"""
This module exposes the composite design pattern in an easy to use way
which attempts to minimalise the repetitive overhead.

The composite design pattern is an alternative to top-down inheritance
when there is no clear hierarchical chain. Examples might include assigning
roles to entities - where an entity can have any variation of roles.

You can utilise this pattern like this:

    ..code-block:: python

        >>> import xcomposite
        >>>
        >>>
        >>> # -- Inheriting off the composition class means that your class can
        >>> # -- immediately bind any other class of a Composition type.
        >>> # -- You should declare (through composite decorators) what the
        >>> # -- expactation is of any bound methods. This allows you to tailor
        >>> # -- exactly how the results should be combined/returned.
        >>> class A(xcomposite.Composition):
        ...
        ...     @xcomposite.Extend
        ...     def items(self):
        ...         return ['a', 'b']
        >>>
        >>>
        >>> class B(xcomposite.Composition):
        ...
        ...     @xcomposite.Extend
        ...     def items(self):
        ...         return ['x', 'y']
        >>>
        >>>
        >>> # -- Instance any one of the classes, and bind it to the instance
        >>> # -- of the other
        >>> a = A()
        >>> a.bind(B())
        >>>
        >>> # -- Call the items method, noting that the result is the expected
        >>> # -- list of items from the 'items' call of both A and B
        >>> print(a.items())

The above example shows how this module can be used when you have the
ability to structure your classes with the composition module in mind. However
if you are using classes which you can only use passively you can take the
following approach:

    ..code-block:: python

        >>> import xcomposite
        >>>
        >>>
        >>> # -- Define a class which we do not want to have inheriting
        >>> # -- from composites. We also do not want to alter methods
        >>> # -- with decorators. This examplifies a situation where the
        >>> # -- classes to be bound are third-party.
        >>> class A(object):
        ...     def items(self):
        ...         return ['a', 'b']
        >>>
        >>>
        >>> class B(object):
        ...     def items(self):
        ...         return ['x', 'y']
        >>>
        >>>
        >>> # -- Because we cannot bind directly within the A or B class
        >>> # -- we instead define a composition wrapper. This is much like
        >>> # -- an abstract - it has no functionality but declares which
        >>> # -- methods should be considered bound and how they should be
        >>> # -- handled.
        >>> class Wrapper(xcomposite.Composition):
        ...
        ...     @xcomposite.Extend
        ...     def items(self):
        ...         return xcomposite.Ignore
        >>>
        >>>
        >>> # -- Instance our wrapper and bind an instance of A and B to it
        >>> inst = Wrapper()
        >>> inst.bind(A())
        >>> inst.bind(B())
        >>>
        >>> # -- Call the items method, noting that the result is the expected
        >>> # -- list of items from the 'items' call of both A and B
        >>> print(inst.items())

There are two examples which come packaged with the module which attempt to
demonstrate simple use-cases which just print output for inspection. You can
run these demos with the following code:

..code-block:: python

    >>> from xcomposite.examples import game
    >>>
    >>> game.demo()

..code-block:: python

    >>> from xcomposite.examples import personnel
    >>>
    >>> personnel.demo()
"""
__author__ = "Michael Malinowski"
__copyright__ = "Copyright (C) 2018 Michael Malinowski"
__license__ = "MIT"
__version__ = "0.9.5"

from .core import (
    Ignore,
    Composition,
)

from .decorators import (
    Min,
    Max,
    Sum,
    Last,
    First,
    Append,
    Update,
    Extend,
    Average,
    AnyTrue,
    AnyFalse,
    AbsoluteTrue,
    AbsoluteFalse,
    AppendUnique,
)
