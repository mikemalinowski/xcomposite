# XComposite Overview
This module exposes the composite design pattern in an easy to use way
which attempts to minimalise the repetitive overhead.

The composite design pattern is an alternative to top-down inheritance
when there is no clear hierarchical chain. Examples might include assigning
roles to entities - where an entity can have any variation of roles.

Methods between composite parts can return all manor of variable types, 
therefore xcomposite gives you a library of decorators which you can utilise
to define how the collective set of results should be wrangled and returned.

__Note: This is currently pre-release__

## Installation
You can install this using pip:
```commandline
pip install xcomposite
```

Alternatively you can get the source from:
https://github.com/mikemalinowski/xcomposite

## Code Documentation:
https://mikemalinowski.github.io/xcomposite/

## Composition Inheritence
You can utilise this pattern like this:


```python
import xcomposite

# -- Inheriting off the composition class means that your class can
# -- immediately bind any other class of a Composition type.
# -- You should declare (through composite decorators) what the
# -- expactation is of any bound methods. This allows you to tailor
# -- exactly how the results should be combined/returned.
class A(xcomposite.Composition):

    @xcomposite.Extend
    def items(self):
        return ['a', 'b']


class B(xcomposite.Composition):

    @xcomposite.Extend
    def items(self):
        return ['x', 'y']


# -- Instance any one of the classes, and bind it to the instance
# -- of the other
a = A()
a.bind(B())

# -- Call the items method, noting that the result is the expected
# -- list of items from the 'items' call of both A and B
print(a.items()) # Prints ['a', 'b', 'x', 'y']
```
# Non-Intrusive Composition 
The above example shows how this module can be used when you have the
ability to structure your classes with the composition module in mind. However
if you are using classes which you can only use passively you can take the
following approach:

```python

import xcomposite


# -- Define a class which we do not want to have inheriting
# -- with decorators. This examplifies a situation where the
# -- classes to be bound are third-party.
class A(object):
    def items(self):
        return ['a', 'b']
    
    def count(self):
        return 2

class B(object):
    def items(self):
        return ['x', 'y']
    
    def count(self):
        return 3 


# -- Because we cannot bind directly within the A or B class
# -- we instead define a composition wrapper. This is much like
# -- an abstract - it has no functionality but declares which
# -- methods should be considered bound and how they should be
# -- handled.
class Wrapper(xcomposite.Composition):

    @xcomposite.Extend
    def items(self):
        # -- Note that this wrapper forms part of the composite
        # -- but we do not want its return values passed through
        xcomposite
        return xcomposite.Ignore
    
    @xcomposite.Sum
    def count(self):
        return xcomposite.Ignore

# -- Instance our wrapper and bind an instance of A and B to it
inst = Wrapper()
inst.bind(A())
inst.bind(B())

# -- Call the items method, noting that the result is the expected
# -- list of items from the 'items' call of both A and B
print(inst.items()) # Prints ['a', 'b', 'x', 'y']

# -- Printing count gives us 5, because we decorate with a Sum
# -- decorator meaning all the values will be added together
print(inst.count()) # Prints 5

```
## Examples
There are two examples which come packaged with the module which attempt to
demonstrate simple use-cases which just print output for inspection. You can
run these demos with the following code:

```python

from xcomposite.examples import game

game.demo()
```

```python

from xcomposite.examples import personnel

personnel.demo()
```
## Testing and Stability

There are currently unittests which cover most of composite's core, but it is not yet exhaustive.

## Compatability

This has been tested under Python 2.7.13 and Python 3.6.6 on both Ubuntu and Windows.

## Contribute

If you would like to contribute thoughts, ideas, fixes or features please get in touch! mike@twisted.space
