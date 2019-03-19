# XComposite Overview
This module exposes the composite design pattern in an easy to use way
which attempts to minimalise the repetitive overhead.

The composite design pattern is an alternative to top-down inheritance
when there is no clear hierarchical chain. Examples might include assigning
roles to entities - where an entity can have any variation of roles.

Methods between composite parts can return all manor of variable types, 
therefore xcomposite gives you a library of decorators which you can utilise
to define how the collective set of results should be wrangled and returned.


## Installation
You can install this using pip:
```commandline
pip install xcomposite
```


Alternatively you can get the source from:
https://github.com/mikemalinowski/xcomposite


# Examples

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

Another, similiar example might be:

```python

    >>> import xcomposite
    >>>
    >>>
    >>> # -- Inheriting off the composition class means that your class can
    >>> # -- immediately bind any other class which is of a Composition type.
    >>> # -- You should declare (through composite decorators) what the
    >>> # -- expactation is of any bound methods. This allows you to tailor
    >>> # -- exactly how the results should be combined/returned.
    >>> class Definition(xcomposite.Composition):
    ...
    ...     @xcomposite.extend_results
    ...     def items(self):
    ...         return ['a', 'b']
    >>>
    >>>
    >>> class MyObject(object):
    ...
    ...     def items(self):
    ...         return ['x', 'y']
    >>>
    >>> 
    >>> class MyOtherObject(object):
    ...
    ...     def items(self):
    ...         return [1, 2]
    >>>
    >>>
    >>> # -- Instance any one of the classes, and bind it to the instance
    >>> # -- of the other
    >>> definition = Definition()
    >>> definition.bind(MyObject())
    >>> definition.bind(MyOtherObject())
    >>>
    >>> # -- Call the items method, noting that the result is the expected
    >>> # -- list of items from the 'items' call of both A and B
    >>> print(definition.items())
    ['a', 'b', 'x', 'y', 1, 2]
```

# Decorators

All composition rules are defined as decorators which you can apply to your
methods on your classes. The following decorators:


    take_min
    take_max
    take_sum
    take_range
    take_average
    take_first
    take_last
    any_true
    any_false
    absolute_true
    absolute_false
    append_unique
    append_results
    extend_results
    extend_unique
    update_dictionary
    
# Restrictions

 * Version 2.0.0 onward is significantly different to version 1.x, and is therefore
not compatible without changes. 

 * All methods decorated with xcomposite decorators are expected to be instance
methods and not class methods.

* Functions which are decorated with xcomposite decorators may be decorated
with other decorators, but any additional decorators should sit atop of the
xcomposite decorator.


## Testing and Stability
There are currently unittests which cover most of composite's core, but it is not yet exhaustive.


## Compatability
This has been tested under Python 2.7.13 and Python 3.6.6 on both Ubuntu and Windows.


## Contribute
If you would like to contribute thoughts, ideas, fixes or features please get in touch! mike@twisted.space
