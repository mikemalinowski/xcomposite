import abc
import uuid


# ------------------------------------------------------------------------------
class CompositeDecorator(object):
    """
    All decorators wanting to base off this should only need to
    re-implement the resolve method. See the resolve method doc
    string for more details.

    Internally this method utilises a tracking uuid to match
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
    This decorator assumes all returns are lists and will use list.extend
    on each list given resulting in a single list of all results.
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
    This decorator will append each result - regardless of type - into a
    list.
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return items


# ------------------------------------------------------------------------------
class AppendUnique(CompositeDecorator):
    """
    This decorator will append each result - regardless of type - into a
    list.
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return list(set(items))


# ------------------------------------------------------------------------------
class Update(CompositeDecorator):
    """
    This decorator will update each dictionary results in order
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
    This decorator will return the first item returned from any of the
    composited methods.
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
        This decorator will return the last item returned from any of the
        composited methods.
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
    This decorator assumes that all methods will return dictionaries
    and the resulting value will be the equivalent of a dict.update
    from each method call.
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
    This decorator assumes a numeric return from each method and will
    return the smallest value.
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return min(items)


# ------------------------------------------------------------------------------
class Max(CompositeDecorator):
    """
    This decorator assumes a numeric return from each method and will
    return the highest value.
    """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return max(items)


# ------------------------------------------------------------------------------
class Sum(CompositeDecorator):
    """
        This decorator assumes a numeric return from each method and will
        return the sum of all the values.
        """

    # --------------------------------------------------------------------------
    @classmethod
    def resolve(cls, items):
        return sum(items)


# ------------------------------------------------------------------------------
class Average(CompositeDecorator):
    """
        This decorator assumes a numeric return from each method and will
        return the average (mean) of all the values.
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
