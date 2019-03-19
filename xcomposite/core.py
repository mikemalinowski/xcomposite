

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
    >>> # -- Instance any one of the classes, and bind it to the instance
    >>> # -- of the other
    >>> definition = Definition()
    >>> definition.bind(MyObject())
    >>>
    >>> # -- Call the items method, noting that the result is the expected
    >>> # -- list of items from the 'items' call of both A and B
    >>> print(definition.items())
    ['a', 'b', 'x', 'y']
    """

    # --------------------------------------------------------------------------
    def __init__(self):
        self._components = []

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
                    if component != self
                ]
            )
        )

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
    """
    pass
