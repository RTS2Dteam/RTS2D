#!/usr/bin/env python
#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror

from rts2d import sprite
from rts2d.pos import Pos

from rts2d.unit import BaseUnit
from rts2d.ability import MoveAbility

import yaml

settings = yaml.load(open("devil.yml"))
# if not pygame.font: print ('Warning, fonts disabled')
# if not pygame.mixer: print ('Warning, sound disabled')
class TestUnit(BaseUnit):
    def __init__(self, **kw):
        super(TestUnit, self).__init__(player="", abilities=[MoveAbility()], **kw)
        self._statusdict["move"] = self._statusdict["normal"]
        self.movspd=100.0
        
sprite.UNITS.update({"test": TestUnit})

class World(): pass


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Jewel Master')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    
#Put Text On The Background, Centered
    # if pygame.font:
        # font = pygame.font.Font(None, 36)
        # text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
        # textpos = text.get_rect(centerx=background.get_width()/2)
        # background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
#Prepare Game Objects
    clock = pygame.time.Clock()
    
    world = World()
    world.time = 0
    world.range = Rect(0,0,800,600)
    devil = sprite.sprite_factory(**settings)(world=world, pos=Pos(200,200))
    
    allsprites = pygame.sprite.RenderPlain((devil,))#(fist, chimp))
    
#Main Loop
    going = True
    while going:
        clock.tick(60)
        # world.time = pygame.time.get_ticks()
        world.deltatime = clock.get_time()
        world.time += world.deltatime
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                pos = Pos(*event.pos)
                devil._abilities[0].use(devil, target_pos=pos)
            # elif event.type == MOUSEBUTTONDOWN:
                # if fist.punch(chimp):
                    # punch_sound.play() #punch
                    # chimp.punched()
                # else:
                    # whiff_sound.play() #miss
            # elif event.type == MOUSEBUTTONUP:
                # fist.unpunch()

        allsprites.update()
        
        #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render("%s"%world.time, 1, (10, 10, 10))
            textpos = text.get_rect(centerx=background.get_width()/2)
            screen.blit(text, textpos)
        pygame.display.flip()
    
    pygame.quit()
    
#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    