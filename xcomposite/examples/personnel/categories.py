"""
Here we define all the roles in a company. Note that an employee can
fulfill multiple roles. They could be promoted, or demoted etc which
would ultimately have a bearing on the roles they play.

For this reason all the roles base of Employee, but from that point on
the roles are not hierarchical. Each role serves its own purpose after all!
"""
import xcomposite


# ------------------------------------------------------------------------------
class Employee(xcomposite.Composition):
    """
    This contains all the requirements and expectations of
    all employees.

    Note that some functions are decorated whilst others are not. Decorated
    methods (using a CompositionDecorator) will always combine their results
    through the composition  class whilst undecorated methods will be
    called 'as-is'.
    """

    # --------------------------------------------------------------------------
    def __init__(self, name=None):
        super(Employee, self).__init__()

        self.name = name

        # -- Define a list of people this employee manages
        self.manages = list()

    # --------------------------------------------------------------------------
    @xcomposite.Extend
    def responsibilities(self):
        """
        This returns a list of responsibilities for any employee regardless
        of the roles they serve
        """
        return [
            'get to work on time',
            'adhere to pep8',
        ]

    # --------------------------------------------------------------------------
    @xcomposite.Min
    def start_time(self):
        """
        Based on a 24 hour clock, what hour do normal employees
        start?

        :return: int
        """
        return 9

    # --------------------------------------------------------------------------
    @xcomposite.Max
    def end_time(self):
        """
        Based on a 24 hour clock, what hour do normal employees
        finish?

        :return: int
        """
        return 17

    # --------------------------------------------------------------------------
    @xcomposite.Sum
    def critical_standing(self):
        """
        Returns a rating as to how critical this employee to the
        company based on what the employee does

        :return: int
        """
        return 1

    # --------------------------------------------------------------------------
    def roles(self):
        """
        Conveniance function which uses the class names of the components
        to output an easy-to-read list of roles

        :return:
        """
        return [
            role.__class__.__name__
            for role in self.components()
        ]

    # --------------------------------------------------------------------------
    def add_subordinate(self, employee):
        """
        Adds a sub-ordinate, making this employee a manager.

        :param employee:
        :return:
        """
        # -- If we're not a manager already we need to
        # -- define ourselves as one!
        if not self.manages:
            self.bind(Manager())

        self.manages.append(employee)

    # --------------------------------------------------------------------------
    def remove_subordinate(self, employee):
        """
        Removes a sub-ordinate. If this employee has nobody to manage then
        their manager role will be revoked.

        :param employee:
        :return:
        """
        self.manages.remove(employee)

        # -- If we no longer have any subordinates we're not
        # -- a manager!
        if not self.manages:
            self.unbind(Manager)


# ------------------------------------------------------------------------------
class Manager(Employee):

    @xcomposite.Extend
    def responsibilities(self):
        return [
            'Keep the project running',
            'Ensure everyone has what they need',
        ]

    @xcomposite.Min
    def start_time(self):
        return 8

    @xcomposite.Sum
    def critical_standing(self):
        return 2


# ------------------------------------------------------------------------------
class Coder(Employee):

    @xcomposite.Extend
    def responsibilities(self):
        return [
            'Writes awesome code',
            'Fixes their managers bugs',
        ]

    @xcomposite.Sum
    def critical_standing(self):
        return 1


# ------------------------------------------------------------------------------
class Artist(Employee):

    @xcomposite.Extend
    def responsibilities(self):
        return [
            'Creates beautiful artwork',
            'doodles pictures of their colleague',
        ]

    @xcomposite.Sum
    def critical_standing(self):
        return 1


# ------------------------------------------------------------------------------
class Author(Employee):

    @xcomposite.Extend
    def responsibilities(self):
        return [
            'Writes engaging content',
        ]

    @xcomposite.Sum
    def critical_standing(self):
        return 1


# ------------------------------------------------------------------------------
class SocialMediaExpert(Employee):

    @xcomposite.Extend
    def responsibilities(self):
        return [
            'Engages with the audience',
            'Makes all the bugs sound like features',
        ]

    @xcomposite.Min
    def start_time(self):
        return 10

    @xcomposite.Max
    def end_time(self):
        return 22

    @xcomposite.Sum
    def critical_standing(self):
        return 1
