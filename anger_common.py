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
