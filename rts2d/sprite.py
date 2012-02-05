""" sprite classes """

from collections import namedtuple
import pygame
from pygame.locals import *
from .pos import Pos

class FactoryData(namedtuple("FactoryData", ["cls", "kw"])):
    def new(self, *args, **kw):
        newkw = self.kw.copy()
        newkw.update(kw)
        return self.cls(*args, **newkw)
        
    __call__ = new

class AnimatedSprite(pygame.sprite.Sprite):
    """ AnimatedSprite is a sprite that uses a list of images and change the
    img in a time-aware fasion. so basically, this class manipulate self.image
    fpstimer is a static-timed timer which designed to be a global time-watch
    
    images should be a dict, every status with a image array
    """
    
    def __init__(self, world, pos, statusdict, *args, **kw):
        """ default pos anchor is "center"
        """
        pygame.sprite.Sprite.__init__(self, *args, **kw)
        self._statusdict = statusdict
        self.status = "normal"
        self._pos = pos
        self._world = world

    @property
    def world(self):
        return self._world
        
    @property
    def pos(self):
        return self._pos
        
    @pos.setter
    def pos(self, val):
        self._pos = val
    
    @property
    def status(self):
        return self._status
        
    @status.setter
    def status(self, val):
        statusdict = self._statusdict
        assert val in statusdict, "%s is Not a valid status" % val
        self._status = val
        self._action = statusdict[val]()
    
    @property
    def image(self):
        return self._action.image(self._world.time).image
        
    @property
    def rect(self):
        return self._action.image(self._world.time).anchor2rect("center", self.pos)

class Action():
    pass
        
class ActionNormal(Action):
    """ the default loop action imp """
    
    def __init__(self, imgarr, fps, **kw):
        self.fps = float(fps)
        self._imgarr = imgarr
        self._stime = None
        
    def image(self, gtime):
        """ calculate current time, return a image, return None if finished """
        if not self._stime:
            self._stime = gtime
        
        dtime = gtime - self._stime
        imgarr = self._imgarr
        imgid = int((self.fps / 1000.) * dtime) % len(imgarr)
        return imgarr[imgid]
        
class ActionTimed(Action):
    """ timed loop, without fps(?) """
    def __init__(self, imgarr, timing, **kw):
        self.timing = timing # in second
        self._imgarr = imgarr
        self._stime = None
        
    def image(self, gtime):
        """ calculate current time, return a image, return None if finished """
        if not self._stime:
            self._stime = gtime
            
        i = int((gtime - self._stime) / (self.timing * 1000. / len(imgarr)))
        return imgarr[i]
        
ActionDict = {
    "normal": ActionNormal,
    "timed": ActionTimed,
}

def action_factory(imgarr, fps, loop="normal", **kw):
    return FactoryData(ActionDict[loop], dict(imgarr=imgarr, fps=fps, **kw))
                    
                    
class SpriteImage():
    def __init__(self, surf, anchors, **kw):
        self._surf = surf
        self._anchors = anchors
        
    def anchor2rect(self, anchorname, anchorpos):
        """ return the image rect with anchorpos setted """
        anchors = self._anchors
        assert anchorname in anchors, "No such anchor!"
        anchorpixel = anchors[anchorname]
        lt = anchorpos - anchorpixel
        return self._surf.get_rect(topleft=lt.ipos)

    @property
    def image(self):
        return self._surf
    
UNITS = {}
    
def packmethod_simple(unittype, image, size, offset, anchors, actions, fps, 
        splitter=(0,0), **kw):
    """ scheme:
        image: (image filename)
        size: [x,y]
        offset: [x,y]
        anchors: {aname(allow float, but in pixel): [ax, ay], aname2: [ax, ay]}
        actions:
            - name: name
              count: 12
              loop(optional, default normal): normal
            - ...
        fps(allow float): 23.8
        
        splitter(optional): [x, y]
    """
    # print image, size, offset, anchors, actions, fps, splitter
    (size, splitter, offset) = map(lambda x: Pos(*x), (size, splitter, offset))
    # anchors
    anchors = dict((aname, Pos(*apos)) for aname, apos in anchors.iteritems())
    # get image surface XXX: default path not yet considered
    # performance surf with alpha
    imagesurf = pygame.image.load(image).convert_alpha()
    actiondict = {}
    for line, action in enumerate(actions):
        surfs = []
        cnt = action["count"] # tile count
        name = action["name"]
        for i in range(cnt): # grab each picture
            lt = offset + (Pos(i, line) * (size + splitter))
            simg = SpriteImage(imagesurf.subsurface(Rect(lt, size)), anchors)
            surfs.append(simg)
        
        actionparams = action.copy()
        actionparams.update(dict(imgarr=surfs, fps=fps))
        actiondict[name] = action_factory(**actionparams)
        
    # return FactoryData(AnimatedSprite, dict(statusdict=actiondict, **kw)) # this is a false usage, use units instead
    return FactoryData(UNITS[unittype], dict(statusdict=actiondict, **kw)) # this is a false usage, use units instead

PACK_METHODS = {
    "simple": packmethod_simple,
}

def sprite_factory(packmethod, spritename, description="", **kw):
    """ scheme:
            packmethod: (method to pack)
            spritename: (name of sprite)
            description(optional): ""
            (datas in sheet)
    """
    sheet = kw
    assert packmethod in PACK_METHODS, "Invalid pack method!"
    return PACK_METHODS[packmethod](**sheet)
    
    