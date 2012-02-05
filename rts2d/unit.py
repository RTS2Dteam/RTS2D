from sprite import AnimatedSprite
class BaseUnit(AnimatedSprite):
    """ hp mp kinds of resources
        hit, damage calculations?
    """
    def __init__(self, world, player, **kw):
        """ player not only mean side of the unit, also show resources
        can be used """
        self._world = world
        self._player = player
        # XXX: register the sprite to player group
    
    def update(self, *args):
        status = self.status
        behavior = self.behavior
        assert status in behavior, "can't determine behavior callback"
        behavior[status]()
    
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
            dict(
                "normal": self.normal,
            )
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
    
    