from .core import Ignore


# ------------------------------------------------------------------------------
def _methods(composition_class, method_name):
    """
    Convenience function for getting a list of all the methods
    which require calling.
    """
    return [
        getattr(component, method_name)
        for component in composition_class.components()
    ]


# ------------------------------------------------------------------------------
def _results(composition_class, method_name, *args, **kwargs):
    """
    Convenience function for return all teh results for the methods
    with the given name on the class.

    :param composition_class: xcomposite.Composition 
    :param method_name: Name of method to call
    :param args: Args to pass to call
    :param kwargs: Keyword arguments to pass

    :return: List of results 
    """
    results = list()

    for method in _methods(composition_class, method_name):
        result = method(*args[1:], **kwargs)

        if not isinstance(result, Ignore):
            results.append(result)

    return results


# ------------------------------------------------------------------------------
def take_min(func):
    """
    This decorator assumes a numeric return from each method and will
    return the smallest value.
    """

    def inner(*args, **kwargs):
        return min(
            _results(
                args[0],
                func.__name__,
                *args,
                **kwargs
            )
        )

    return inner


# ------------------------------------------------------------------------------
def take_max(func):
    """
    This decorator assumes a numeric return from each method and will
    return the highest value.
    """

    def inner(*args, **kwargs):
        return max(
            _results(
                args[0],
                func.__name__,
                *args,
                **kwargs
            )
        )

    return inner


# ------------------------------------------------------------------------------
def take_sum(func):
    """
    This decorator assumes a numeric return from each method and will
    return the sum of all the values. 
    """

    def inner(*args, **kwargs):
        return sum(
            _results(
                args[0],
                func.__name__,
                *args,
                **kwargs
            )
        )

    return inner


# ------------------------------------------------------------------------------
def take_average(func):
    """
    This decorator assumes a numeric return from each method and will
    return the average (mean) of all the values.
    """

    def inner(*args, **kwargs):
        results = _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

        sum_of_results = sum(results)

        if sum_of_results == 0:
            return sum_of_results

        return sum_of_results / len(results)

    return inner


# ------------------------------------------------------------------------------
def take_first(func):
    """
    This decorator will return the first item returned from any of the
    composited methods.
    """
    def inner(*args, **kwargs):
        print('In Decorator')
        for method in _methods(args[0], func.__name__):
            result = method(*args[1:], **kwargs)

            if not isinstance(result, Ignore):
                return result

        return None

    return inner


# ------------------------------------------------------------------------------
def take_last(func):
    """
    This decorator will return the last item returned from any of the
    composited methods.
    """

    def inner(*args, **kwargs):
        for method in reversed(_methods(args[0], func.__name__)):
            result = method(*args[1:], **kwargs)

            if not isinstance(result, Ignore):
                return result

        return None

    return inner


# ------------------------------------------------------------------------------
def extend_results(func):
    """
    This decorator assumes all returns are lists and will use list.extend
    on each list given resulting in a single list of all results.
    """

    def inner(*args, **kwargs):
        extended_results = list()
        results = _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

        for result in results:
            if not isinstance(result, Ignore):
                extended_results.extend(result)

        return extended_results

    return inner


# ------------------------------------------------------------------------------
def extend_unique(func):
    """
    This decorator assumes all returns are lists and will use list.extend
    on each list given resulting in a single list of all results.
    """

    def inner(*args, **kwargs):
        extended_results = list()
        results = _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

        for result in results:
            if not isinstance(result, Ignore):
                extended_results.extend(result)

        return list(set(extended_results))

    return inner


# ------------------------------------------------------------------------------
def update_dictionary(func):
    """
    This decorator will update each dictionary results in order
    """

    def inner(*args, **kwargs):
        output = dict()
        results = _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

        for result in results:
            if not isinstance(result, Ignore):
                output.update(result)

        return output

    return inner


# ------------------------------------------------------------------------------
def absolute_false(func):
    """
    Returns False if all elements evaluate to False, otherwise True
    is returned.
    """

    def inner(*args, **kwargs):
        results = _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

        for result in results:
            if result:
                return True
        return False

    return inner


# ------------------------------------------------------------------------------
def absolute_true(func):
    """
    Returns True if all elements evaluate to True, otherwise False
    is returned.
    """

    def inner(*args, **kwargs):
        results = _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

        for result in results:
            if not result:
                return False
        return True

    return inner


# ------------------------------------------------------------------------------
def any_false(func):
    """
    If any items are False, then false is returned.
    """

    def inner(*args, **kwargs):
        results = _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

        for result in results:
            if not result:
                return False
        return True

    return inner


# ------------------------------------------------------------------------------
def any_true(func):
    """
    If any items are True, then True is returned.
    """

    def inner(*args, **kwargs):
        results = _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

        for result in results:
            if result:
                return True
        return False

    return inner


# ------------------------------------------------------------------------------
def append_results(func):
    """
    This decorator will append each result - regardless of type - into a
    list.
    """

    def inner(*args, **kwargs):
        return _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

    return inner


# ------------------------------------------------------------------------------
def append_unique(func):
    """
    This decorator will append each result - regardless of type - into a
    list. 
    """

    def inner(*args, **kwargs):
        return list(
            set(
                _results(
                    args[0],
                    func.__name__,
                    *args,
                    **kwargs
                )
            )
        )

    return inner


# ------------------------------------------------------------------------------
def take_range(func):
    """
    Returns the range of all the values (max - min). If only one value
    is given the range will be zero.
    """

    def inner(*args, **kwargs):
        results = _results(
            args[0],
            func.__name__,
            *args,
            **kwargs
        )

        return float(max(results)) - float(min(results))

    return inner
