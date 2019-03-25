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

    .. code-block:: python

        >>> import xcomposite
        >>>
        >>>
        >>> # -- The composition class defines the decoration rules for
        >>> # -- each method which requires compositing. This must inherit
        >>> # -- from the xcomposite.Composition class.
        >>> class A(xcomposite.Composition):
        ...
        ...     @xcomposite.extend_results
        ...     def items(self):
        ...         return ['a', 'b']
        >>>
        >>>
        >>> # -- The class(es) being bound to the composition do not need
        >>> # -- to inherit from the composition. Equally their functions
        >>> # -- do not need to be decorated either
        >>> class B(object):
        ...
        ...     def items(self):
        ...         return ['x', 'y']
        >>>
        >>>
        >>> # -- We instance the composition, then bind any amount of classes
        >>> # -- to that composition. All classes being bound to a composition
        >>> # -- *must* be class instances.
        >>> a = A()
        >>> a.bind(B())
        >>>
        >>> # -- Call the items method, noting that the result is the expected
        >>> # -- list of items from the 'items' call of both A and B
        >>> # -- The composition cycles through all the bound classes, and 
        >>> # -- where it finds a class with the same method name it will be
        >>> # -- called.
        >>> print(a.items())

# Restrictions

Version 2.0.0 onward is significantly different to version 1.x, and is therefore
not compatible without changes. 

All methods decorated with xcomposite decorators are expected to be instance
methods and not class methods.

Functions which are decorated with xcomposite decorators may be decorated
with other decorators, but any additional decorators should sit atop of the
xcomposite decorator.
"""
from .core import (
    Ignore,
    Composition,
)

from .decorators import (
    take_min,
    take_max,
    take_sum,
    take_range,
    take_average,
    take_first,
    first_true,
    take_last,
    any_true,
    any_false,
    absolute_true,
    absolute_false,
    append_unique,
    append_results,
    extend_results,
    extend_unique,
    update_dictionary,


)
__author__ = "Michael Malinowski"
__copyright__ = "Copyright (C) 2019 Michael Malinowski"
__license__ = "MIT"
__version__ = "2.0.5"
