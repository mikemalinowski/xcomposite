from . import classes

import os
import json
import xcomposite


# ------------------------------------------------------------------------------
def demo():
    """
    This demo aims to show a situation where there is no clear inheritence
    structure, so standard top down inheritence is not a viable option.

    It also demonstrates the composition wrapping - which is an approach to
    using the composite module in situations where you do not own directly
    the classes you want to wrap. Therefore, for the sake of this demo we
    consider all the base game classes to be 'third party' - meaning all
    our binding must be done outside of those classes.

    :return:
    """

    # -- We start by looking over all our game data. For each
    # -- game data set we need to create a game object which
    # -- represents those properties.
    game_objects = load_game_objects()

    # -- Lets print what game objects we have...
    for game_object in game_objects:
        print('\nWe have a %s - %s' % (game_object.name, game_object))

        print('\tProperties:')
        for name, value in game_object.properties().items():
            print('\t\t%s = %s' % (name, value))

        print('\tPlayer Actions')
        for name in game_object.user_actions():
            print('\t\t' + name)

    # -- Given from the output we can see that we're dynamically attributing
    # -- behaviours to game objects based on data. The behaviours are not
    # -- hierarchial - in that an arrow is projectile just as an apple is
    # -- yet neither of those two would fit above or below the other in a
    # -- hierarchy.
    print('')

    # -- We can also invoke actions for each
    for game_object in game_objects:
        for name, action in game_object.user_actions().items():
            print('%s : %s' % (name, game_object.name))
            print('\t%s' % action())


# ------------------------------------------------------------------------------
def load_game_objects():
    """
    This will cycle over all the game data and generate game objects
    from the game data.

    The game objects are compositions of all the properties defined
    in the game data files.

    :return: list(Composition, ...)
    """

    # -- Get a list of all the properties our game objects can
    # -- be made up from
    all_behaviours = [
        classes.Flame,
        classes.Edible,
        classes.Weapon,
        classes.Consumable,
        classes.Projectile,
    ]

    game_data_path = os.path.join(
        os.path.dirname(__file__),
        'data',
    )

    game_objects = list()

    for root, _, files in os.walk(game_data_path):
        for filename in files:

            # -- Construct an absolute path
            filepath = os.path.join(
                root,
                filename
            )

            # -- Parse the file
            with open(filepath, 'r') as f:
                data = json.load(f)

            behaviours = list()

            for behaviour in all_behaviours:
                if behaviour.has_property(data):
                    behaviours.append(behaviour)

            if not behaviours:
                continue

            game_object = CompositeGameObject()

            for behaviour in behaviours:
                instanced_behaviour = behaviour(data)
                game_object.bind(instanced_behaviour)

            game_objects.append(game_object)

    return game_objects


# ------------------------------------------------------------------------------
class CompositeGameObject(xcomposite.Composition):
    """
    We define a definition of how we want different methods to bind together.

    The classes themselves do not need to know anything about the binding
    meaning they can stay entirely encapsulated. This class then defines the
    rules and behaviour for how return values are combined.
    """

    @xcomposite.Update
    def properties(self):
        return dict()

    @xcomposite.Update
    def user_actions(self):
        return dict()

    @xcomposite.Extend
    def affected_by(self):
        return 0

    @xcomposite.Extend
    def invulnerable_to(self):
        return 0
