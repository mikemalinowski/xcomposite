"""
This holds a series of classes specifically designed to test
results in a deterministic way.
"""
import xcomposite


class DecoratorTesterA(xcomposite.Composition):
    """
    Each decorator is represented by a function. All of which
    will return 1 or 'A' (in whatever expected form).
    """

    @xcomposite.Min
    def min(self):
        return 1

    @xcomposite.Max
    def max(self):
        return 1

    @xcomposite.Sum
    def sum(self):
        return 1

    @xcomposite.First
    def first(self):
        return 'A'

    @xcomposite.Last
    def last(self):
        return 'A'

    @xcomposite.Append
    def append(self):
        return 'A'

    @xcomposite.AppendUnique
    def append_unique(self):
        return 'X'

    @xcomposite.Extend
    def extend_list(self):
        return ['A']

    @xcomposite.Average
    def average(self):
        return 1.0

    @xcomposite.Update
    def update(self):
        return dict(foo=1)


class DecoratorTesterB(xcomposite.Composition):
    """
    Each decorator is represented by a function. All of which
    will return 2 or 'B' (in whatever expected form).
    """

    @xcomposite.Min
    def min(self):
        return 2

    @xcomposite.Max
    def max(self):
        return 2

    @xcomposite.Sum
    def sum(self):
        return 2

    @xcomposite.First
    def first(self):
        return 'B'

    @xcomposite.Last
    def last(self):
        return 'B'

    @xcomposite.Append
    def append(self):
        return 'B'

    @xcomposite.AppendUnique
    def append_unique(self):
        return 'X'

    @xcomposite.Extend
    def extend_list(self):
        return ['B']

    @xcomposite.Average
    def average(self):
        return 2.0

    @xcomposite.Update
    def update(self):
        return dict(bar=1)

class UndecoratedTesterA(xcomposite.Composition):

    def undecorated(self):
        return 1


class UndecoratedTesterB(xcomposite.Composition):

    def undecorated(self):
        return 2


class PartiallyDecoratedTesterA(xcomposite.Composition):

    @xcomposite.Max
    def test(self):
        return 1


class PartiallyDecoratedTesterB(xcomposite.Composition):

    def test(self):
        return 2
