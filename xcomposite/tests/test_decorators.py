import unittest
from xcomposite.tests.classes import (
    DecoratorBase,
    DecoratorTesterA,
    DecoratorTesterB,
    UndecoratedTesterA,
    UndecoratedTesterB,
    PartiallyDecoratedTesterA,
    PartiallyDecoratedTesterB,
)


# ------------------------------------------------------------------------------
class CompositionTests(unittest.TestCase):

    # --------------------------------------------------------------------------
    def test_min(self):
        """
        Checks that the smallest value is always returned

        :return:
        """
        bound_class = self._bound_class()

        self.assertEqual(
            1,
            bound_class.min(),
        )

    # --------------------------------------------------------------------------
    def test_max(self):
        """
        Checks that the largest value is always returned

        :return:
        """
        bound_class = self._bound_class()

        self.assertEqual(
            2,
            bound_class.max(),
        )

    # --------------------------------------------------------------------------
    def test_sum(self):
        """
        Checks that the sum of all values is returned

        :return:
        """
        bound_class = self._bound_class()

        self.assertEqual(
            3,
            bound_class.sum(),
        )

    # --------------------------------------------------------------------------
    def test_first(self):
        """
        Checks that the sum of all values is returned

        :return:
        """
        bound_class = self._bound_class()
        print(bound_class.first())
        self.assertEqual(
            'A',
            bound_class.first(),
        )

    # --------------------------------------------------------------------------
    def test_last(self):
        """
        Checks that the sum of all values is returned

        :return:
        """
        bound_class = self._bound_class()

        self.assertEqual(
            'B',
            bound_class.last(),
        )

    # --------------------------------------------------------------------------
    def test_append(self):
        """
        Checks that the sum of all values is returned

        :return:
        """
        bound_class = self._bound_class()
        print(bound_class.append())
        self.assertEqual(
            ['A', 'B'],
            bound_class.append(),
        )

    # --------------------------------------------------------------------------
    def test_append_unique(self):
        """
        Checks that the sum of all values is returned

        :return:
        """
        bound_class = self._bound_class()

        self.assertEqual(
            ['X'],
            bound_class.append_unique(),
        )

    # --------------------------------------------------------------------------
    def test_update(self):
        """
        Checks that the sum of all values is returned

        :return:
        """
        bound_class = self._bound_class()

        self.assertEqual(
            ['foo', 'bar'],
            list(bound_class.update().keys()),
        )

    # --------------------------------------------------------------------------
    def test_extend(self):
        """
        Checks that the sum of all values is returned

        :return:
        """
        bound_class = self._bound_class()

        self.assertEqual(
            ['A', 'B'],
            bound_class.extend_list(),
        )

    # --------------------------------------------------------------------------
    def test_average(self):
        """
        Checks that the sum of all values is returned

        :return:
        """
        bound_class = self._bound_class()

        self.assertEqual(
            1.5,
            bound_class.average(),
        )

    # --------------------------------------------------------------------------
    def test_undecorated(self):
        """
        Checks that the sum of all values is returned

        :return:
        """
        bound_class = self._undecorated_bound_class()

        self.assertEqual(
            1,
            bound_class.undecorated(),
        )

    # --------------------------------------------------------------------------
    def test_partially_decorated_functions(self):
        """
        We expect partially decorated functions to raise an exception as
        that is a situation we do not allow.

        :return:
        """
        first_class = PartiallyDecoratedTesterA()
        second_class = PartiallyDecoratedTesterB()

        # -- Perform the bind
        first_class.bind(second_class)

        try:
            first_class.test()

            self.assertTrue(
                True,
                msg='No assert from a partially deorated function',
            )

        except Exception:
            pass

    # --------------------------------------------------------------------------
    def _bound_class(self):
        """
        Function returns two decorated classes bound together

        :return:
        """
        first_class = DecoratorBase()

        # -- Perform the bind
        first_class.bind(DecoratorTesterA())
        first_class.bind(DecoratorTesterB())

        return first_class

    # --------------------------------------------------------------------------
    def _undecorated_bound_class(self):
        """
        Function returns two decorated classes bound together

        :return:
        """
        first_class = UndecoratedTesterA()
        second_class = UndecoratedTesterB()

        # -- Perform the bind
        first_class.bind(second_class)

        return first_class
