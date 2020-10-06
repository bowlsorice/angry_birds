#common stuff for angry birds CreatePolygonFixture
import pygame
import Box2D
from Box2D.b2 import world

CIRCLE = 0
BOX = 1

WHITE = (255,255,255)
BLACK = (0,0,0)
MAROON = (128,0,0)

PPM = 100
VIEW = 1440,900

FPS = 60
TIME_STEP = 1.0/FPS

SLING_COLOR = MAROON

pygame.init()

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN) # for fs, set TRANS[1] to 3
clock = pygame.time.Clock()

world = world(gravity=(0,-10), doSleep=True)

#add art imports
background_art = pygame.image.load("anger_art/background.png").convert_alpha()
redwing_art = pygame.image.load("anger_art/redwing.png").convert_alpha()
bluebird_art = pygame.image.load("anger_art/bluebird.png").convert_alpha()
basic_art = pygame.image.load("anger_art/basic_bird.png").convert_alpha()
ground_art = pygame.image.load("anger_art/ground.png").convert_alpha()
log_long_art = pygame.image.load("anger_art/log_long.png").convert_alpha()
log_looong_art = pygame.image.load("anger_art/log_looong.png").convert_alpha()
log_short_art = pygame.image.load("anger_art/log_short.png").convert_alpha()
slingshot_art = pygame.image.load("anger_art/slingshot.png").convert_alpha()
hedgehog_art = pygame.image.load("anger_art/hedgehog.png").convert_alpha()
