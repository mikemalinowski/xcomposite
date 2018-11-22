from . import categories


# ------------------------------------------------------------------------------
def demo():
    """
    This runs some code which walks through the process of instancing an
    employee and defining a series of roles. We then print some information
    relating to that empoyee which demonstrates how our composition class
    is managing the combining of all the resulting calls from each role
    for us and bringing it together in a result which makes sense contextually.

    We then add a second employee - and therefore remove roles from ella and
    add roles to the employee. By doing this we're getting different results
    from the same method calls without changing the inheritance tree.

    This short demo aims to show how the Composition class can be used to
    unite classes together dynamically. This is not a replacement for
    inheritence, but an alternative when top-down structure makes less
    sense.

    :return:
    """

    # -- Create our first employee!
    ella = categories.Employee('Ella Anderson')

    # -- Ella is the first person in the company, so she inevitably
    # -- ends up doing a lot of work!
    ella.bind(categories.Coder())
    ella.bind(categories.Artist())
    ella.bind(categories.SocialMediaExpert())

    # -- Lets print out some information about what ella is doing!
    print('Ella whilst she is the sole employee:')
    print_employee_info(ella)

    # -- Clearly ella is a dedicated employee! By her art work leaves
    # -- a lot to be desired! So lets hire an artist
    jack = categories.Employee('Jack Grayfield')
    jack.bind(categories.Artist())

    # -- Now we have a dedicated artist we dont need ella
    # -- to do any more art, we'll also have ella manage jack
    ella.unbind(categories.Artist)
    ella.add_subordinate(jack)

    # -- Now lets look at ella again
    print('Ella now she has a dedicated artist on the team:')
    print_employee_info(ella)

    # -- We can now see that her responsibilities to do any art
    # -- have gone. Though as she now manages other people her
    # -- time in-the-office has increased a bit!
    # -- Lets take a look at Jack
    print('Our new Artist:')
    print_employee_info(jack)

    # -- As we can see from the output, Jack has one main role in
    # -- the company, compared to ella who has three. But we can
    # -- interact and query each of them in the same way - getting
    # -- the combined information in a way which makes sense.
    pass

    # -- For instance, Coders, Social Media Exports and Managers
    # -- all have very different start and end times for their
    # -- working hours. But we do not have to worry about calculating
    # -- it, because the compition does that for us:
    print('Ella finished work at %shrs' % ella.end_time())


# ------------------------------------------------------------------------------
def print_employee_info(employee):
    """
    function to print some information about the given
    employee.

    :param employee: xcomposite.examples.personel.Employee

    :return:
    """
    data = """
    Employee Name : %s
        Roles : %s
        Repsonsibilities : %s
        Hours worked each day : %shrs
        Importance to the company : %s
    """ % (
        employee.name,
        '; '.join(employee.roles()),
        '; '.join(employee.responsibilities()),
        employee.end_time() - employee.start_time(),
        employee.critical_standing(),
    )

    print(data)
