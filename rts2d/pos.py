""" pos is a point tuple definition """

import collections
import numbers
import math

def posify(other):
    if isinstance(other, numbers.Number):
        return Pos(other, other)
    return Pos._make(other)

def distance(pos1, pos2):
    return math.sqrt((pos2.fpos - pos1.fpos) ** 2.0)
    
def direction(origpos, destpos):
    d = (destpos.fpos - origpos.fpos)
    ld = math.sqrt(d ** 2.0)
    return d / ld
    
class Pos(collections.namedtuple("Pos", 'x y')):
    def __new__(_cls, x, y):
        assert isinstance(x, numbers.Number)
        assert isinstance(y, numbers.Number)
        return tuple.__new__(_cls, (x, y))

    def __add__(self, other):
        other = posify(other)
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        other = posify(other)
        return Pos(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """ produce """
        other = posify(other)
        return Pos(self.x * other.x, self.y * other.y)
            
    def __div__(self, other):
        other = posify(other)
        return Pos(self.x / other.x, self.y / other.y)
        
    def __neg__(self):
        return Pos(-self.x, -self.y)
    
    def __pow__(self, other, modulo=None):
        """ modulo not used """
        return pow(self.x, other, modulo) + pow(self.y, other, modulo)
        
    @property
    def ipos(self):
        return Pos(*map(lambda k: int(round(k)), self))

    @property
    def fpos(self):
        return Pos(*map(float, self))
    