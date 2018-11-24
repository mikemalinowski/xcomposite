import abc
import uuid


# ------------------------------------------------------------------------------
class CompositeDecorator(object):
    """
    All decorators wanting to base off this should only need to
    re-implement the resolve method. See the resolve method doc
    string for more details.

    resolve is given a list of all the returns. You can then wrangle
    that in any way you want. What you return from 'resolve' is what
    will be returned to the user.

    .. code-block:: python

    >>> class MyCustomDecorator(CompositeDecorator):
    ... 
    ...     @classmethod
    ...     def resolve(cls, items):
    ...         output = list()
    ... 
    ...         for item in items:
    ...             output.extend(item)
    ...
    ...         return output
    """
    __metaclass__ = abc.ABCMeta

    _RESULTS = dict()

    # --------------------------------------------------------------------------
    def __init__(self, method):
        self._method = method

    # --------------------------------------------------------------------------
    def __call__(self, *args, **kwargs):
        return self._method(
            self,
            *args,
            **kwargs
        )

    # --------------------------------------------------------------------------
    @classmethod
    def start(cls):
        """
        This will initialise the internal tracking property
        for cross instance data resolving. This function will
        return a uuid which should be passed to any subsequent
        storage calls.

        :return: uuid
        """
        identifier = str(uuid.uuid4())
        cls._RESULTS[identifier] = list()

        return identifier

    # --------------------------------------------------------------------------
    @classmethod
    def store(cls, item, identifier):
        """
        This will store the item against the giving uuid.

        :param item: The item to store
        :param identifier: The uuid to store against

        :return:
        """
        if identifier not in cls._RESULTS:
            raise Exception('%s is an invalid identifier' % identifier)

        cls._RESULTS[identifier].append(item)

    # --------------------------------------------------------------------------
    @classmethod
    def clear(cls, identifier):
        """
        This clears all the results for the given uuid

        :param identifier:
        :return:
        """
        del cls._RESULTS[identifier]

    # --------------------------------------------------------------------------
    @classmethod
    def results(cls, identifier):
        return cls._RESULTS[identifier]

    # --------------------------------------------------------------------------
    @classmethod
    @abc.abstractmethod
    def resolve(cls, items):
        """
        This is the only function you need to re-implement in most
        cases. It allows you to take the results from all the method
        calls and decide what form to return them in.

        :param items: These are the results from all the method
            calls from the composited object.
        :type items: list(var, var, ...)

        :return:
        """
        return


# ------------------------------------------------------------------------------
class Extend(CompositeDecorator):
    """
    .. decorator:: Extend

    This decorator assumes all returns are lists and will use list.extend
    on each list given resulting in a single list of all results.

    >>> class A(object):
    ...     @xcomposite.Extend
    ...     def items(self):
    ...         return ['a', 'b']
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.Extend
    ...     def items(self):
    ...         return ['x', 'y']
    ['a', 'b', 'x', 'y']
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        output = list()

        for item in items:
            output.extend(item)

        return output


# ------------------------------------------------------------------------------
class Append(CompositeDecorator):
    """
    .. decorator:: Append

    This decorator will append each result - regardless of type - into a
    list.

    >>> class A(object):
    ...     @xcomposite.Append
    ...     def items(self):
    ...         return None
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.Append
    ...     def items(self):
    ...         return ['x', 'y']
    [None, ['x', 'y']]
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return items


# ------------------------------------------------------------------------------
class AppendUnique(CompositeDecorator):
    """
    .. decorator:: AppendUnique

    This decorator will append each result - regardless of type - into a
    list.

    >>> class A(object):
    ...     @xcomposite.AppendUnique
    ...     def items(self):
    ...         return 1
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.AppendUnique
    ...     def items(self):
    ...         return 1
    >>> 
    >>> class B(object):
    ...     @xcomposite.AppendUnique
    ...     def items(self):
    ...         return 2
    [1, 2]
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return list(set(items))


# ------------------------------------------------------------------------------
class Update(CompositeDecorator):
    """
    .. decorator:: Update

    This decorator will update each dictionary results in order

    >>> class A(object):
    ...     @xcomposite.Update
    ...     def items(self):
    ...         return {'foo': 1}
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.Update
    ...     def items(self):
    ...         return {'bar': 2}
    {'foo': 1, 'bar': 2}
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        output = dict()

        for item in items:
            output.update(item)

        return output


# ------------------------------------------------------------------------------
class First(CompositeDecorator):
    """
    .. decorator:: First

    This decorator will return the first item returned from any of the
    composited methods.

    >>> class A(object):
    ...     @xcomposite.First
    ...     def items(self):
    ...         return 10
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.First
    ...     def items(self):
    ...         return 5
    10
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        if items:
            return items[0]

        return None


# ------------------------------------------------------------------------------
class Last(CompositeDecorator):
    """
    .. decorator:: Last

    This decorator will return the last item returned from any of the
    composited methods.

    >>> class A(object):
    ...     @xcomposite.Last
    ...     def items(self):
    ...         return 10
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.Last
    ...     def items(self):
    ...         return 5
    5
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        if items:
            return items[-1]

        return None


# ------------------------------------------------------------------------------
class UpdateDict(CompositeDecorator):
    """
    .. decorator:: UpdateDict

    This decorator assumes that all methods will return dictionaries
    and the resulting value will be the equivalent of a dict.update
    from each method call.

    >>> class A(object):
    ...     @xcomposite.UpdateDict
    ...     def items(self):
    ...         return {'foo': 1}
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.UpdateDict
    ...     def items(self):
    ...         return {'bar': 2}
    {'foo': 1, 'bar': 2}
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        output = dict()

        for item in items:
            output.update(item)

        return output


# ------------------------------------------------------------------------------
class Min(CompositeDecorator):
    """
    .. decorator:: Min

    This decorator assumes a numeric return from each method and will
    return the smallest value.

    >>> class A(object):
    ...     @xcomposite.Min
    ...     def items(self):
    ...         return 10
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.Min
    ...     def items(self):
    ...         return 5
    5
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return min(items)


# ------------------------------------------------------------------------------
class Max(CompositeDecorator):
    """
    .. decorator:: Max

    This decorator assumes a numeric return from each method and will
    return the highest value.

        >>> class A(object):
        ...     @xcomposite.Max
        ...     def items(self):
        ...         return 10
        >>>
        >>>
        >>> class B(object):
        ...     @xcomposite.Max
        ...     def items(self):
        ...         return 5
        10
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return max(items)


# ------------------------------------------------------------------------------
class Sum(CompositeDecorator):
    """
    .. decorator:: Sum

    This decorator assumes a numeric return from each method and will
    return the sum of all the values.

    >>> class A(object):
    ...     @xcomposite.Sum
    ...     def items(self):
    ...         return 10
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.Sum
    ...     def items(self):
    ...         return 5
    15
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return sum(items)


# ------------------------------------------------------------------------------
class Average(CompositeDecorator):
    """
    .. decorator:: Average

    This decorator assumes a numeric return from each method and will
    return the average (mean) of all the values.

    >>> class A(object):
    ...     @xcomposite.Sum
    ...     def items(self):
    ...         return 0
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.Sum
    ...     def items(self):
    ...         return 10
    5
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        if not items:
            return None

        sum_of_items = sum(items)

        if sum_of_items == 0:
            return sum_of_items

        return sum_of_items / len(items)


# ------------------------------------------------------------------------------
class Range(CompositeDecorator):
    """
    Returns the range of all the values (max - min). If only one value
    is given the range will be zero.

    Note: This expects numeric values
    
    >>> class A(object):
    ...     @xcomposite.Range
    ...     def items(self):
    ...         return 5
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.Range
    ...     def items(self):
    ...         return 20
    15
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return max(items) - min(items)


# ------------------------------------------------------------------------------
class AbsoluteTrue(CompositeDecorator):
    """
    Returns True if all elements evaluate to True, otherwise False
    is returned.
    
    >>> class A(object):
    ...     @xcomposite.AbsoluteTrue
    ...     def items(self):
    ...         return True
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.AbsoluteTrue
    ...     def items(self):
    ...         return False
    False
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        for item in items:
            if not item:
                return False

        return True


# ------------------------------------------------------------------------------
class AbsoluteFalse(CompositeDecorator):
    """
    Returns False if all elements evaluate to False, otherwise True
    is returned.
    
    >>> class A(object):
    ...     @xcomposite.AbsoluteFalse
    ...     def items(self):
    ...         return True
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.AbsoluteFalse
    ...     def items(self):
    ...         return False
    True
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        for item in items:
            if item:
                return True

        return False


# ------------------------------------------------------------------------------
class AnyFalse(CompositeDecorator):
    """
    If any items are False, then false is returned.
    
    >>> class A(object):
    ...     @xcomposite.AnyFalse
    ...     def items(self):
    ...         return True
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.AnyFalse
    ...     def items(self):
    ...         return False
    False
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        for item in items:
            if not item:
                return False

        return True


# ------------------------------------------------------------------------------
class AnyTrue(CompositeDecorator):
    """
    If any items are True, then True is returned.
    
    >>> class A(object):
    ...     @xcomposite.AnyTrue
    ...     def items(self):
    ...         return True
    >>>
    >>>
    >>> class B(object):
    ...     @xcomposite.AnyTrue
    ...     def items(self):
    ...         return False
    True
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        for item in items:
            if item:
                return True

        return False
