#FIX HOG DEATH BUG

import pygame
import random
import Box2D
from Box2D.b2 import (world, polygonShape, circleShape,
    staticBody, dynamicBody, pi, globals, contact)


from anger_sprites import *

PPM = 100
VIEW = 1000,600
FPS = 35
TIME_STEP = 1.0/FPS
WHITE = (255,255,255)
MAROON = (128,0,0)
BLACK = (0,0,0)
SLING_COLOR = MAROON
TRANS = 0,0


game = True
running = True
art = True


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
log_looong_art = pygame.image.load("anger_art/log_looong.png").convert_alpha()
log_short_art = pygame.image.load("anger_art/log_short.png").convert_alpha()
slingshot_art = pygame.image.load("anger_art/slingshot.png").convert_alpha()
hedgehog_art = pygame.image.load("anger_art/hedgehog.png").convert_alpha()

world = world(gravity=(0,-10), doSleep=True)

def make_log(pos,rotation,size):
    if size == 0:
        a_log = Thing(world,log_short_art,pos,rotation,BOX,scale=1)
    elif size == 1:
        a_log = Thing(world,log_long_art,pos,rotation,BOX,scale=1)
    elif size == 2:
        a_log = Thing(world,log_looong_art,pos,rotation,BOX,scale=1)
    return a_log

def make_lvl1():
    birds = []
    hogs = []
    logs = []
    base = 8.5

    basic = Bird(world,basic_art,(2.2,5),0)
    birds.append(basic)
    redwing = Bird(world,redwing_art,(.5,.5),0)
    birds.append(redwing)
    bluebird = Bird(world,bluebird_art,(1,.5),0)
    birds.append(bluebird)

    global hedgehog_art
    hedgehog_art = pygame.transform.flip(hedgehog_art,True,False)
    hog_infos = [((0,4),0)]
    for each in hog_infos:
        a_hog = Hog(world,hedgehog_art,(each[0][0]+base,each[0][1]),each[1])
        hogs.append(a_hog)

    log_infos = [((-.5,1),90,1),((.5,1),90,1),((0,2),0,1),((-.3,2.5),90,0),
        ((.2,2.5),90,0),((0,3.0),0,0)]
    logs = []
    for each in log_infos:
        a_log = make_log((each[0][0]+base,each[0][1]),each[1],each[2])
        logs.append(a_log)

    lvl1 = Level(logs,base,hogs,birds)
    return lvl1

def make_lvl2():
    birds = []
    hogs = []
    logs = []
    base = 8

    basic = Bird(world,basic_art,(2.2,5),0)
    birds.append(basic)
    redwing = Bird(world,redwing_art,(.5,.5),0)
    birds.append(redwing)
    bluebird = Bird(world,bluebird_art,(1,.5),0)
    birds.append(bluebird)

    global hedgehog_art
    hedgehog_art = pygame.transform.flip(hedgehog_art,True,False)
    hog_infos = [((0,3),0),((-.75,1),0),((.75,1),0)]
    for each in hog_infos:
        a_hog = Hog(world,hedgehog_art,(each[0][0]+base,each[0][1]),each[1])
        hogs.append(a_hog)

    log_infos = [((-1.5,1.0),90,0),((1.5,1.0),90,0),((0,1.0),90,0),
        ((0,1.5),0,2),((-.25,2.0),90,0),((.25,2.0),90,0),((0,2.5),0,1)]
    for each in log_infos:
        a_log = make_log((each[0][0]+base,each[0][1]),each[1],each[2])
        logs.append(a_log)

    lvl2 = Level(logs,base,hogs,birds)
    return lvl2

def draw_sling(color,slingshot,translation):
    if in_sling!=None:
        pygame.draw.line(screen,color,
            ((slingshot.anchora.position[0]-translation[0])*PPM,
            600-(slingshot.anchora.position[1]-translation[1])*PPM),
            ((in_sling.body.position[0]-translation[0])*PPM,
            600-(in_sling.body.position[1]-translation[1])*PPM),4)
        pygame.draw.line(screen,color,
            ((slingshot.anchorb.position[0]-translation[0])*PPM,
            600-(slingshot.anchorb.position[1]-translation[1])*PPM),
            ((in_sling.body.position[0]-translation[0])*PPM,
            600-(in_sling.body.position[1]-translation[1])*PPM),4)
    else:
        pygame.draw.line(screen,color,
            ((slingshot.anchora.position[0]-translation[0])*PPM,
            600-(slingshot.anchora.position[1]-translation[1])*PPM),
            ((slingshot.anchorb.position[0]-translation[0])*PPM,
            600-(slingshot.anchorb.position[1]-translation[1])*PPM),4)


in_sling = None
time_shot = -1000
clicked = False

slingshot = Slingshot(slingshot_art,(1.5,1.4),world)
ground = Thing(world,ground_art,(10,0),0,BOX,static=True)

level = make_lvl2()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos = (pos[0]/PPM)+TRANS[0],(600-pos[1])/PPM+TRANS[1]
            if in_sling != None:
                if in_sling.fix.TestPoint(pos):
                    clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and clicked:
            clicked = False
            in_sling.launch(screen,world,slingshot,TRANS)
            in_sling.shot = True
            in_sling = None
            time_shot = pygame.time.get_ticks()

    if in_sling == None:
        birds_not_shot = 0
        for bird in level.birds:
            if not bird.shot:
                birds_not_shot+=1
        if birds_not_shot>0 and pygame.time.get_ticks()-time_shot >= 1000:
            i = 0
            while in_sling == None:
                if level.birds[i].shot==False:
                    level.birds[i].load(world,slingshot)
                    in_sling = level.birds[i]
                    level.birds[i].body.awake = False
                    level.birds[i].shot = True
                else:
                    i+=1
    else:
        if clicked:
            posa = pygame.mouse.get_pos()
            posa = (posa[0]/PPM)+TRANS[0],(600-posa[1])/PPM+TRANS[1]
            posb = slingshot.rect.centerx,slingshot.rect.y+10
            posb = posb[0]/PPM, (600-posb[1])/PPM
            length = (((posb[0]-posa[0])**2+
                (posb[1]-posa[1])**2)**(1/2))
            if length<=1.0:
                in_sling.body.transform = (posa,0)
            else:
                reduct = 1.0/length
                move = (posb[0]-(posb[0]-posa[0])*reduct,
                    posb[1]-(posb[1]-posa[1])*reduct)
                in_sling.body.transform = (move,in_sling.body.angle)
        else:
            in_sling.body.awake=False

    for each in level.hogs: #check for actual fixture collision, rather than AABB
        if not each.dead:
            v1 = each.getV()
            v1 = (v1[0]**2+v1[1]**2)**(1/2) #correct up to here at leastb
            each.lastv = v1
            ke = (each.lastv**2)*each.body.mass*0.5
            each.ke_pass = False
            for contact in each.body.contacts:
                other = contact.other
                other_v = other.linearVelocity
                other_v = (other_v[0]**2+other_v[1]**2)**(1/2)
                other_ke = (other_v**2)*other.mass*0.5
                ke_collide = ke+other_ke
                if ke_collide>10:
                    each.ke_pass = True


    world.Step(TIME_STEP, 10, 10) #always do before drawing!!

    for each in level.hogs:
        if not each.dead:
            v  = each.getV()
            v = (v[0]**2+v[1]**2)**(1/2)
            if abs(v-each.lastv)>1:
                each.dead = True
                each.time_of = pygame.time.get_ticks()
                each.pos_of = each.body.position
                world.DestroyBody(each.body)



    if art:
        screen.fill((128,216,255))
        screen.blit(background_art,(-1*TRANS[0]*PPM,TRANS[1]*PPM))
        #screen.blit(background_art,(0,0))
        ground.draw(screen,TRANS)
        slingshot.draw(screen,TRANS)
        draw_sling(SLING_COLOR,slingshot,TRANS)
        for each in level.logs:
            each.draw(screen,TRANS)
        for each in level.birds:
            each.draw(screen,TRANS)
        for each in level.hogs:
            if each.dead:
                if pygame.time.get_ticks()-each.time_of<250:
                    each.drawPuff(screen,TRANS)
                else:
                    level.hogs.remove(each)
            elif not each.dead:
                each.draw(screen,TRANS)

    elif not art:
        screen.fill((0,0,0))
        ground.draw_shape(screen,TRANS)
        for each in level.logs:
            each.draw_shape(screen,TRANS)
        for each in level.birds:
            each.draw_shape(screen,TRANS)
        for each in level.hogs:
            if each.dead:
                if pygame.time.get_ticks()-each.time_of>=250:
                    level.hogs.remove(each)
            elif not each.dead:
                each.draw_shape(screen,TRANS)
        draw_sling(WHITE,slingshot,TRANS)

    #TRANS = TRANS[0]+.01,TRANS[1]

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
