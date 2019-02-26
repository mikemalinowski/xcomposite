from .decorators import CompositeDecorator

from functools import partial


# ------------------------------------------------------------------------------
class Composition(object):
    """
    This should be used as the base class for any class which needs to
    be composited.

    When inheriting this class you must decorate any methods you want
    to utilise the composition mechanism. The decorator you choose
    to use defines the behaviour of how the results will be combined or
    selected.

    If a method is not decorated it will be expected to exist on the
    base class directly.

    >>> import xcomposite
    >>>
    >>>
    >>> # -- Inheriting off the composition class means that your class can
    >>> # -- immediately bind any other class which is of a Composition type.
    >>> # -- You should declare (through composite decorators) what the
    >>> # -- expactation is of any bound methods. This allows you to tailor
    >>> # -- exactly how the results should be combined/returned.
    >>> class A(xcomposite.Composition):
    ...
    ...     @xcomposite.Extend
    ...     def items(self):
    ...         return ['a', 'b']
    >>>
    >>>
    >>> class B(xcomposite.Composition):
    ...
    ...     @xcomposite.Extend
    ...     def items(self):
    ...         return ['x', 'y']
    >>>
    >>>
    >>> # -- Instance any one of the classes, and bind it to the instance
    >>> # -- of the other
    >>> a = A()
    >>> a.bind(B())
    >>>
    >>> # -- Call the items method, noting that the result is the expected
    >>> # -- list of items from the 'items' call of both A and B
    >>> print(a.items())
    """

    # --------------------------------------------------------------------------
    def __init__(self, target=None):
        self._target = target or self
        self._components = list()
        self._bound_items = list()

    # --------------------------------------------------------------------------
    def __getattribute__(self, item):
        """
        We override this to intercept all attribute requests. If the
        attribute exists and it is not decorated with a CompositeDecorator
        it will be returned.

        Any decorated method which is intercepted will trigger an
        equivalent call of each composite added. The decorated is then
        utilised to determine how the value should be returned.

        :param item: Item being requested

        :return: melded result if it is a decorated function otherwise
            it will just return the expected value.
        """
        # -- Ask for forgiveness rather than permission for the
        # -- sake of performance. If we're able to access the
        # -- attribute directly, and if it is not a composite
        # -- decorator we return it as it is.
        try:
            matched_item = object.__getattribute__(
                self,
                item
            )

            if not isinstance(matched_item, CompositeDecorator):
                return matched_item

        except AttributeError:
            pass

        # -- To get here we're dealing either with no attribute on the
        # -- base class, or a decorated attribute. Therefore we need
        # -- to look for decorated methods.
        methods_to_composite = list()

        composites = [self._target]
        composites.extend(self._components)

        for composite in composites:

            # -- Ask for the item from the composite
            try:
                matched_item = object.__getattribute__(
                    composite,
                    item
                )

            except AttributeError:
                continue

            # -- Check if we're dealing with a method or a
            # -- property
            if callable(matched_item):

                # -- We're working with a method, so we add
                # -- it to our collection of composited methods
                methods_to_composite.append(matched_item)

            else:

                # -- If we're dealing with a property we always
                # -- return the first - as we assume a priority
                # -- order
                return matched_item

        # -- If no matches were found we have nothing to do, so we
        # -- simply return None
        if not methods_to_composite:
            raise AttributeError('Could not find %s' % item)

        # -- A request was made for a function, so we need to
        # -- return a function. The returned function is always
        # -- our propogation call.
        return partial(
            self._propogate_call,
            methods_to_composite,
        )

    # --------------------------------------------------------------------------
    def __repr__(self):
        """
        Printing only the class is not enough if this is made up of multiple
        components. Therefore we override the representation to show what
        the class is made up of.

        :return: str
        """
        # -- If we have no components we return the class name
        if not self._components:
            return self.__class__.__name__

        # -- We construct a label containing the class name plus
        # -- all the components
        return '[%s (%s)]' % (
            self.__class__.__name__,
            '; '.join(
                [
                    component.__class__.__name__
                    for component in self._components
                ]
            )
        )

    # --------------------------------------------------------------------------
    #@classmethod
    def _propogate_call(self, methods, *args, **kwargs):
        """
        This method is responsible for call the listed methods from
        all the composited classes.

        There is an implicit understanding of the constructor structure
        within this method to allow for the combining of results.

        :param methods: list of methods to be called
        :param args: Arguments to be passed to each method
        :param kwargs: Key word arguments to pass to the calls

        :return: The result from the assigned decorator
        """
        # -- Check if our methods are decorated with composite
        # -- decorators. They either must all be decorated with the
        # -- same type or not decorated at all
        decorated = [
            type(method)
            for method in methods
            if isinstance(method, CompositeDecorator)
        ]

        # -- If they are decorated we need to check that they
        # -- are all decorated with teh same types
        # if len(decorated) != len(methods) or len(set(decorated)) != 1:
        #     raise Exception('Not all functions are decorated equally')
        if not decorated:
            raise Exception('No decorated functions given')

        # -- At this point we can use any of the methods as an accessor
        # -- to the decorator. For the sake of readability we store the
        # -- first method under decoration name
        decorator = methods[0]

        # -- We need to 'start' the decorators storage mechanism. This
        # -- gives us an identifier which we must use when asking the
        # -- decorator to store or retrieve results for us
        identifier = decorator.start()

        # -- Now we can call the methods sequentially
        for method in methods:

            # -- Call the method with all the given arguments
            result = method(
                self,
                *args,
                **kwargs
            )

            # -- If this result is specifically our composite.Ignore
            # -- class we ignore it. The ignore class is typically used
            # -- when defining a wrapper
            if result == Ignore:
                continue

            # -- Store the result of the method call and give
            # -- the identifer to ensure the decorator can resolve
            # -- one set of results from another
            decorator.store(
                result,
                identifier,
            )

        # -- Finally we just need to resolve the results. This is the
        # -- part where the decorator takes all the return statements
        # -- and decides what to do with them
        resolved_results = decorator.resolve(
            decorator.results(identifier),
        )

        # -- Now that we're done we ask the decorator to clean
        # -- itself up a little
        decorator.clear(identifier)

        return resolved_results

    # --------------------------------------------------------------------------
    def components(self):
        """
        Accessor for the component list

        :return: list(instance, instance, ...)
        """
        return self._components

    # --------------------------------------------------------------------------
    def bind(self, component):
        """
        Adds a component to the class. From the point a component is added
        it is melded to this class and all decorated calls will incorporate
        this component.

        :param component: Component to meld
        :type component: Class

        :return: None
        """
        self._components.append(component)

    # --------------------------------------------------------------------------
    def unbind(self, component_type):
        """
        Removes a components of a given type from the component
        list.

        :param component_type: Class Type to remove

        :return:
        """
        for component in self._components[:]:
            if isinstance(component, component_type):
                self._components.remove(component)


# ------------------------------------------------------------------------------
class Ignore(object):
    """
    This class can be used as a return item when you specifically do not
    want the value of a function to contribute a bound result. This is
    particularly useful when wanting to apply the composite pattern to
    classes without altering hierarchy or applying decorators directly.

    An example of this would be:

    >>> import xcomposite
    >>>
    >>>
    >>> # -- Define a class which we do not want to have inheriting
    >>> # -- from composites. We also do not want to alter methods
    >>> # -- with decorators. This examplifies a situation where the
    >>> # -- classes to be bound are third-party.
    >>> class A(object):
    ...     def items(self):
    ...         return ['a', 'b']
    >>>
    >>>
    >>> class B(object):
    ...     def items(self):
    ...         return ['x', 'y']
    >>>
    >>>
    >>> # -- Because we cannot bind directly within the A or B class
    >>> # -- we instead define a composition wrapper. This is much like
    >>> # -- an abstract - it has no functionality but declares which
    >>> # -- methods should be considered bound and how they should be
    >>> # -- handled.
    >>> class Wrapper(xcomposite.Composition):
    ...
    ...     @xcomposite.Extend
    ...     def items(self):
    ...         return xcomposite.Ignore
    >>>
    >>>
    >>> # -- Instance our wrapper and bind an instance of A and B to it
    >>> inst = Wrapper()
    >>> inst.bind(A())
    >>> inst.bind(B())
    >>>
    >>> # -- Call the items method, noting that the result is the expected
    >>> # -- list of items from the 'items' call of both A and B
    >>> print(inst.items())
    """
    pass
