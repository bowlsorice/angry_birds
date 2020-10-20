#common stuff for angry birds CreatePolygonFixture
import pygame
import Box2D
from Box2D.b2 import world
from Box2D import b2ContactListener

CIRCLE = 0
BOX = 1

WHITE = (255,255,255)
BLACK = (0,0,0)
MAROON = (128,0,0)
YELLOW = (255, 255, 102)
BLUE = (165,242,243)
RED = (255,0,0)
SKY = (128, 216, 255)

PPM = 100
VIEW = 1440,900

FPS = 60
TIME_STEP = 1.0/FPS

SLING_COLOR = MAROON

pygame.init()

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()

class myContactListener(b2ContactListener):
    def __init__(self):
        b2ContactListener.__init__(self)
    def PostSolve(self, contact, impulse):
        thing_a = contact.fixtureA.body.userData
        thing_b = contact.fixtureB.body.userData
        if impulse.normalImpulses[0]>.5:
            thing_a.contact_impulse = impulse.normalImpulses[0]
            thing_b.contact_impulse = impulse.normalImpulses[0]


world = world(gravity=(0,-10), doSleep=True, contactListener=myContactListener())

#add art imports
redwing_art = pygame.image.load("anger_art/redwing.png").convert_alpha()
bluebird_art = pygame.image.load("anger_art/bluebird.png").convert_alpha()
basic_art = pygame.image.load("anger_art/basic_bird.png").convert_alpha()

log_long_art = pygame.image.load("anger_art/log_long.png").convert_alpha()
log_looong_art = pygame.image.load("anger_art/log_looong.png").convert_alpha()
log_short_art = pygame.image.load("anger_art/log_short.png").convert_alpha()

ice_long_art = pygame.image.load("anger_art/ice_long.png").convert_alpha()
ice_looong_art = pygame.image.load("anger_art/ice_looong.png").convert_alpha()
ice_short_art = pygame.image.load("anger_art/ice_short.png").convert_alpha()

hedgehog_art = pygame.image.load("anger_art/hedgehog.png").convert_alpha()
hedgehog_art = pygame.transform.flip(hedgehog_art, True, False)

ground_art = pygame.image.load("anger_art/ground.png").convert_alpha()
slingshot_art = pygame.image.load("anger_art/slingshot.png").convert_alpha()
background_art = pygame.image.load("anger_art/background.png").convert_alpha()
back_fall_art = pygame.image.load("anger_art/back_fall.png").convert_alpha()
back_sunset_art = pygame.image.load("anger_art/back_sunset.png").convert_alpha()

pause_art = pygame.image.load("anger_art/pause.png").convert_alpha()


puff1, puff2, puff3 = (pygame.image.load("anger_art/puff1.png").convert_alpha(),
        pygame.image.load("anger_art/puff2.png").convert_alpha(),
        pygame.image.load("anger_art/puff3.png").convert_alpha())
shatter1, shatter2, shatter3 = (pygame.image.load("anger_art/"+
        "shatter1.png").convert_alpha(),
        pygame.image.load("anger_art/shatter2.png").convert_alpha(),
        pygame.image.load("anger_art/shatter3.png").convert_alpha())
ice_shatter1, ice_shatter2, ice_shatter3 = (pygame.image.load("anger_art/"+
        "ice_shatter1.png").convert_alpha(),
        pygame.image.load("anger_art/ice_shatter2.png").convert_alpha(),
        pygame.image.load("anger_art/ice_shatter3.png").convert_alpha())
