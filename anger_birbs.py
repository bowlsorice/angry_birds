import pygame
import random
import Box2D
from Box2D.b2 import (world, polygonShape, circleShape,
    staticBody, dynamicBody, pi, globals)


from anger_sprites import *

PPM = 100
VIEW = 1000,600
FPS = 40
TIME_STEP = 1.0/FPS
WHITE = (255,255,255)
MAROON = (128,0,0)
BLACK = (0,0,0)
SLING_COLOR = MAROON


game = True
running = True
art = True

rotate = 0

pygame.init()

screen = pygame.display.set_mode((VIEW[0],VIEW[1]),0,32)
pygame.display.set_caption("anger birbs")
clock = pygame.time.Clock()

#need to redo all art at the end
background_art = pygame.image.load("anger_art/background.png").convert_alpha()
redwing_art = pygame.image.load("anger_art/redwing.png").convert_alpha()
bluebird_art = pygame.image.load("anger_art/bluebird.png").convert_alpha()
basic_art = pygame.image.load("anger_art/basic_bird.png").convert_alpha()
ground_art = pygame.image.load("anger_art/ground.png").convert_alpha()
log_long_art = pygame.image.load("anger_art/log_long.png").convert_alpha()
log_short_art = pygame.image.load("anger_art/log_short.png").convert_alpha()
slingshot_art = pygame.image.load("anger_art/slingshot.png").convert_alpha()
hedgehog_art = pygame.image.load("anger_art/hedgehog.png").convert_alpha()

world = world(gravity=(0,-10), doSleep=True)

things = []
birds = []

ground = Thing(world,ground_art,(5,0),0,BOX,static=True)
things.append(ground)
slingshot = Slingshot(slingshot_art,(1.5,1.4),world)
basic = Bird(world,basic_art,(2.2,5),0)
things.append(basic)
birds.append(basic)
redwing = Bird(world,redwing_art,(.5,.5),0)
things.append(redwing)
birds.append(redwing)
bluebird = Bird(world,bluebird_art,(1,.5),0)
things.append(bluebird)
birds.append(bluebird)
hedgehog_art = pygame.transform.flip(hedgehog_art,True,False)
hedgehog = Hog(world,hedgehog_art,(8.5,3.2),0)
things.append(hedgehog)


def draw_sling(color,slingshot):
    if in_sling!=None:
        pygame.draw.line(screen,color,(slingshot.anchora.position[0]*PPM,
            600-slingshot.anchora.position[1]*PPM),
            (in_sling.body.position[0]*PPM,
            600-in_sling.body.position[1]*PPM),4)
        pygame.draw.line(screen,color,(slingshot.anchorb.position[0]*PPM,
            600-slingshot.anchorb.position[1]*PPM),
            (in_sling.body.position[0]*PPM,
            600-in_sling.body.position[1]*PPM),4)
    else:
        pygame.draw.line(screen,color,(slingshot.anchora.position[0]*PPM,
            600-slingshot.anchora.position[1]*PPM),
            (slingshot.anchorb.position[0]*PPM,
            600-slingshot.anchorb.position[1]*PPM),4)


def make_log(pos,rotation,size):
    if size == 0:
        a_log = Thing(world,log_short_art,pos,rotation,BOX,scale=.8)
    elif size == 1:
        a_log = Thing(world,log_long_art,pos,rotation,BOX,scale=.8)
    things.append(a_log)

logs = [((8.0,1),90,1),((9.0,1),90,1),((8.5,2),0,1),((8.2,2.5),90,0),
    ((8.7,2.5),90,0),((8.5,3.0),0,0)]
for log in logs:
    make_log(log[0],log[1],log[2])


in_sling = None
time_shot = -1000
clicked = False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos = pos[0]/PPM,(600-pos[1])/PPM
            if in_sling != None:
                if in_sling.fix.TestPoint(pos):
                    clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and clicked:
            clicked = False
            in_sling.launch(screen,world,slingshot)
            birds.remove(in_sling)
            in_sling = None
            time_shot = pygame.time.get_ticks()

    if in_sling == None:
        if len(birds)>0 and pygame.time.get_ticks()-time_shot >= 1000:
            birds[0].load(world,slingshot)
            in_sling = birds[0]
            birds[0].body.awake = False
    else:
        if clicked:
            posa = pygame.mouse.get_pos()
            posa = posa[0]/PPM,(600-posa[1])/PPM
            posb = slingshot.rect.centerx,slingshot.rect.y
            posb = posb[0]/PPM, (600-posb[1])/PPM
            length = (((posb[0]-posa[0])**2+
                (posb[1]-posa[1])**2)**(1/2))
            if length<=1.0:
                in_sling.body.transform = (posa,in_sling.body.angle)
            else:
                reduct = 1.0/length
                move = (posb[0]-(posb[0]-posa[0])*reduct,
                    posb[1]-(posb[1]-posa[1])*reduct)
                in_sling.body.transform = (move,in_sling.body.angle)

        else:
            in_sling.body.awake=False


    world.Step(TIME_STEP, 10, 10) #always do before drawing!!
    if art:
        screen.fill((147,211,246))
        screen.blit(background_art,(0,0))
        slingshot.draw(screen)
        draw_sling(SLING_COLOR,slingshot)
        for each in things:
            each.draw(screen)
    elif not art:
        screen.fill((0,0,0))
        for each in things:
            each.draw_shape(screen)
        draw_sling(WHITE,slingshot)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
