"""
This holds a series of classes specifically designed to test
results in a deterministic way.
"""
import xcomposite


class DecoratorBase(xcomposite.Composition):
    """
    Each decorator is represented by a function. All of which
    will return 1 or 'A' (in whatever expected form).
    """

    @xcomposite.take_min
    def min(self):
        return 1

    @xcomposite.take_max
    def max(self):
        return 1

    @xcomposite.take_sum
    def sum(self):
        return 1

    @xcomposite.take_first
    def first(self):
        return 'A'

    @xcomposite.take_last
    def last(self):
        return 'A'

    @xcomposite.append_results
    def append(self):
        return 'A'

    @xcomposite.append_unique
    def append_unique(self):
        return 'X'

    @xcomposite.extend_results
    def extend_list(self):
        return ['A']

    @xcomposite.take_average
    def average(self):
        return 1.0

    @xcomposite.update_dictionary
    def update(self):
        return dict(foo=1)


class DecoratorTesterA(DecoratorBase):
    """
    Each decorator is represented by a function. All of which
    will return 1 or 'A' (in whatever expected form).
    """

    def min(self):
        return 1

    def max(self):
        return 1

    def sum(self):
        return 1

    def first(self):
        return 'A'

    def last(self):
        return 'A'

    def append(self):
        return 'A'

    def append_unique(self):
        return 'X'

    def extend_list(self):
        return ['A']

    def average(self):
        return 1.0

    def update(self):
        return dict(foo=1)


class DecoratorTesterB(xcomposite.Composition):
    """
    Each decorator is represented by a function. All of which
    will return 2 or 'B' (in whatever expected form).
    """

    def min(self):
        return 2

    def max(self):
        return 2

    def sum(self):
        return 2

    def first(self):
        return 'B'

    def last(self):
        return 'B'

    def append(self):
        return 'B'

    def append_unique(self):
        return 'X'

    def extend_list(self):
        return ['B']

    def average(self):
        return 2.0

    def update(self):
        return dict(bar=1)


# ------------------------------------------------------------------------------
class UndecoratedTesterA(xcomposite.Composition):

    def undecorated(self):
        return 1


# ------------------------------------------------------------------------------
class UndecoratedTesterB(xcomposite.Composition):

    def undecorated(self):
        return 2


# ------------------------------------------------------------------------------
class PartiallyDecoratedTesterA(xcomposite.Composition):

    @xcomposite.take_max
    def test(self):
        return 1


# ------------------------------------------------------------------------------
class PartiallyDecoratedTesterB(xcomposite.Composition):

    def test(self):
        return 2
