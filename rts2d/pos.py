""" pos is a point tuple definition """

import collections
import numbers

def posify(other):
    if isinstance(other, numbers.Number):
        return Pos(other, other)
    return Pos._make(other)

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
    
    def __pow__(self, other, *args, **kwargs):
        """ modulo not used """
        return self.x**other + self.y**other
        
    @property
    def ipos(self):
        return Pos(*map(lambda k: int(round(k)), self))

    @property
    def fpos(self):
        return Pos(*map(float, self))
    