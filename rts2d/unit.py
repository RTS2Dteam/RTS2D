from .sprite import AnimatedSprite
class BaseUnit(AnimatedSprite):
    """ hp mp kinds of resources
        hit, damage calculations?
    """
    def __init__(self, player, abilities, **kw):
        """ player not only mean side of the unit, also show resources
        can be used """
        super(BaseUnit, self).__init__(**kw)
        self._player = player
        # XXX: register the sprite to player group
        self._abilities = abilities
        # initial abilities
        for ability in abilities:
            ability.initial(self)
        
    
    def add_ability(self, ability):
        self._abilities.append(ability)
        
    def remove_ability(self, ability):
        self._abilities.remove(ability)
    
    def update(self, *args):
        for ability in self._abilities:
            ability.update(self, *args)
    
    def b_normal(self):
        """basic react for each unit"""
        pass
        
class Building(BaseUnit):
    """
    Buildings do not move
    Buildings' pos always fetches grid
    have skills(for building things)
    """
    def __init__(self, cell, ):
        BaseUnit.__init__(self, )
        self.behavior.update(
            {
                "normal": self.normal,
            }
        )
        
    def normal(self):
        pass

class AirUnit(BaseUnit):
    """
    air movement
    skills
    
    movement basics:
        lowlevel move: just move to a pos
        waypointed move: move through waypoints
        grouped move: move with a group
        options:
            attack-aware? when attack range, stop move(temporary) and attack
            move->checkvisualrange->move2attackrange->attack->leaveattackcondition->move
            
    """
    pass
    
class GroundUnit(BaseUnit):
    pass
    
    