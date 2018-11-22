"""
In here we define our game behaviours. Behaviours are encapsulated
chunks of functionality which can be bound together to create interesting
and varying higher level game objects
"""


class GameObjectBehaviour(object):
    """
    Serves as a base class for all our behaviours
    """
    PropertyType = ''

    def __init__(self, game_data):
        self.data = game_data
        self.name = self.data['name']

    def properties(self):
        return dict()

    def user_actions(self):
        return dict()

    def affected_by(self):
        return 0

    def invulnerable_to(self):
        return 0

    @classmethod
    def has_property(cls, game_data):
        return cls.__name__ in game_data['properties']


class Consumable(GameObjectBehaviour):

    def properties(self):
        return dict(
            ConsumptionRate=10,
            ConsumptionValue=5,
        )

    def user_actions(self):
        return dict(
            Use=self._use,
            Discard=self._discard,
        )

    def affected_by(self):
        return [
            'Age',
        ]

    def invulnerable_to(self):
        return []

    def _use(self):
        return 'using %s' % self.name

    def _discard(self):
        return 'Throwing %s away' % self.name


class Edible(GameObjectBehaviour):

    def properties(self):
        return dict(
            Tastiness=10,
            HealingPower=1,
        )

    def user_actions(self):
        return dict(
            Use=self._eat,
        )

    def affected_by(self):
        return [
            'Age',
            'Temperature'
        ]

    def invulnerable_to(self):
        return []

    def _eat(self):
        return 'Eating %s' % self.name


class Projectile(GameObjectBehaviour):

    def properties(self):
        return dict(
            Distance=1,
        )

    def user_actions(self):
        return dict(
            Throw=self._throw,
        )

    def affected_by(self):
        return [
            'Wind',
        ]

    def invulnerable_to(self):
        return [
            'Age',
        ]

    def _throw(self):
        return 'Throwing %s %sm' % (
            self.name,
            self.properties()['Distance'],
        )


class Weapon(GameObjectBehaviour):

    def properties(self):
        return dict(
            Damage=10,
        )

    def user_actions(self):
        return dict(
            Attack=self._attack,
        )

    def affected_by(self):
        return [
            'Wear',
        ]

    def invulnerable_to(self):
        return [
            'Age',
        ]

    def _attack(self):
        return 'Attacking with %s doing %s damage' % (
            self.name,
            self.properties()['Damage'],
        )


class Flame(GameObjectBehaviour):

    def properties(self):
        return dict(
            Heat=10,
        )

    def user_actions(self):
        return dict()

    def affected_by(self):
        return [
            'Water',
        ]

    def invulnerable_to(self):
        return [
            'Heat',
        ]
