import unittest
from xcomposite.tests.classes import (
    DecoratorTesterA,
    DecoratorTesterB,
)


# ------------------------------------------------------------------------------
class CompositionTests(unittest.TestCase):

    # --------------------------------------------------------------------------
    def test_binding_classes(self):
        """
        Checks that we can bind two classes

        :return:
        """
        # -- Instance both classes
        first_class = DecoratorTesterA()
        second_class = DecoratorTesterB()

        # -- Perform the bind
        first_class.bind(second_class)

        self.assertIn(
            second_class,
            first_class.components(),
        )

    # --------------------------------------------------------------------------
    def test_unbinding_classes(self):
        """
        Checks that we can unbind two classes

        :return:
        """
        # -- Instance both classes
        first_class = DecoratorTesterA()
        second_class = DecoratorTesterB()

        # -- Perform the bind
        first_class.bind(second_class)

        self.assertIn(
            second_class,
            first_class.components(),
        )

        # -- Perform the unbind
        first_class.unbind(DecoratorTesterB)

        self.assertNotIn(
            second_class,
            first_class.components(),
        )

    # --------------------------------------------------------------------------
    def test_components_can_be_accessed(self):
        """
        Tests whether the component list is being returned as expected

        :return:
        """
        # -- Instance both classes
        first_class = DecoratorTesterA()
        second_class = DecoratorTesterB()

        # -- Perform the bind
        first_class.bind(second_class)

        self.assertIn(
            second_class,
            first_class.components(),
        )

        self.assertEqual(
            len(first_class.components()),
            1,
        )

    # --------------------------------------------------------------------------
    def test_bound_representation_is_correct(self):
        """
        Tests whether the component list is being returned as expected

        :return:
        """
        # -- Instance both classes
        first_class = DecoratorTesterA()
        second_class = DecoratorTesterB()

        # -- Perform the bind
        first_class.bind(second_class)

        self.assertEqual(
            '[DecoratorTesterA (DecoratorTesterB)]',
            str(first_class),
        )

    # --------------------------------------------------------------------------
    def test_unbound_representation_is_correct(self):
        """
        Tests whether the component list is being returned as expected

        :return:
        """
        # -- Instance both classes
        first_class = DecoratorTesterA()

        self.assertEqual(
            'DecoratorTesterA',
            str(first_class),
        )

    # --------------------------------------------------------------------------
    def test_unaccessible_method(self):
        """
        Tests whether the component list is being returned as expected

        :return:
        """
        # -- Instance both classes
        first_class = DecoratorTesterA()

        try:
            first_class.foo()

            self.assertTrue(
                False,
                msg='Did not assert when accessing an inaccessible attribute',
            )

        except AttributeError:
            pass
