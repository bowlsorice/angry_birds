import pygame
import Box2D
import math
from Box2D.b2 import (world, polygonShape, circleShape,
    staticBody, dynamicBody, pi)
from anger_common import *

class Thing():
    def __init__(self,img,pos,rotation,
        shape,static=False,scale=1,density=1):
        img = pygame.transform.rotozoom(img,0,scale)
        self.img = img
        angle = rotation * (pi/180)
        self.shape = shape
        if static:
            self.body = world.CreateStaticBody(position=(pos),angle=angle)
        else:
            self.body = world.CreateDynamicBody(position=(pos),
                fixedRotation=False,angle=angle)
        if shape == CIRCLE:
                radius = self.img.get_rect().width*.6/2/PPM
                self.fix = self.body.CreateCircleFixture(radius=radius,
                    density=density,friction=0.3,restitution=.5)
                self.radius = radius
        elif shape == BOX:
                dimensions = (self.img.get_rect().width/(2*PPM),
                    self.img.get_rect().height/(2*PPM))
                self.fix = self.body.CreatePolygonFixture(box=dimensions,
                    density=density,friction=0.3,restitution=.5)
    def draw(self,translation):
        angle = self.body.angle * (180/pi)
        r_img = pygame.transform.rotate(self.img,angle)
        center = ((self.body.position[0]-translation[0])*PPM,
            VIEW[1]-((self.body.position[1]-translation[1])*PPM))
        rect = r_img.get_rect(center = center)
        screen.blit(r_img,(rect.topleft))
    def draw_shape(self,translation):
        pos = ((self.body.position[0]-translation[0])*PPM,
            VIEW[1]-((self.body.position[1]-translation[1])*PPM))
        if self.shape == BOX:
            vertices = [(self.body.transform * v) #here!! STILL BAD
                for v in self.fix.shape.vertices]
            vertices = [((v[0]-translation[0])*PPM,
                VIEW[1]-(v[1]-translation[1])*PPM) for v in vertices]
            pygame.draw.polygon(screen,WHITE,vertices)
        elif self.shape == CIRCLE:
            radius = int(self.radius*PPM)
            pos = int(pos[0]),int(pos[1])
            pygame.draw.circle(screen,(255,255,255),pos,radius)
            x = pos[0]+radius*math.cos(self.body.angle)
            y = pos[1]-radius*math.sin(self.body.angle)
            point = x,y
            pygame.draw.line(screen,(0,0,0),pos,point)
    def getV(self):
        return (self.body.linearVelocity[0],self.body.linearVelocity[1])


class Bird(Thing):
    def __init__(self,img,pos,angle):
        super().__init__(img,pos,angle,CIRCLE,density=4)
        self.shot = False
    def launch(self,screen,slingshot,translation):
        posa = self.body.position
        posb = slingshot.rect.centerx,slingshot.rect.y
        posb = (posb[0]/PPM), (VIEW[1]-posb[1])/PPM
        length = (((posb[0]-posa[0])**2+
            (posb[1]-posa[1])**2)**(1/2))
        reduct = 8#/length
        vector = ((posb[0]-posa[0])*reduct,
            (posb[1]-posa[1])*reduct)
        self.body.ApplyLinearImpulse(vector,self.body.position,True)
    def load(self,slingshot):
        pos = (slingshot.rect.centerx,slingshot.rect.y+10)
        pos = (pos[0]/PPM),((VIEW[1]-pos[1])/PPM)
        self.body.transform = (pos,0)

class Slingshot():
    def __init__(self,img,pos,scale=1):
        img = pygame.transform.rotozoom(img,0,scale)
        self.img = img
        self.rect = img.get_rect(center = (pos[0]*PPM, VIEW[1]-pos[1]*PPM))
        anchora = ((self.rect.topleft[0]+10)/PPM,
            (VIEW[1]-self.rect.topleft[1]-10)/PPM)
        anchorb = ((self.rect.topright[0]-10)/PPM,
            (VIEW[1]-self.rect.topright[1]-10)/PPM)
        self.anchora = world.CreateStaticBody(position=(anchora),angle=0)
        self.anchorb = world.CreateStaticBody(position=(anchorb),angle=0)
    def draw(self,translation):
        screen.blit(self.img,(self.rect.x-(translation[0]*PPM),
            (self.rect.y+(translation[1]*PPM))))
    def draw_shape(self):
        pygame.draw.circle(screen,WHITE,
            (int((self.anchora.position[0]-translation[0])*PPM),
            int(VIEW[1]-(self.anchora.position[1]-translation[1])*PPM)),5)
        pygame.draw.circle(screen,WHITE,
            (int((self.anchorb.position[0]-translation[0])*PPM),
            int(VIEW[1]-(self.anchorb.position[1]-translation[1])*PPM)),5)

class Hog(Thing):
    def __init__(self,img,pos,angle):
        self.dead  = False
        super().__init__(img,pos,angle,CIRCLE,density=4)
        self.puffs = [pygame.image.load("anger_art/puff1.png").convert_alpha(),
            pygame.image.load("anger_art/puff2.png").convert_alpha(),
            pygame.image.load("anger_art/puff3.png").convert_alpha()]
    def drawPuff(self,translation,frame):
        rect = self.puffs[frame].get_rect(
            center=((self.pos_of[0]-translation[0])*PPM,
            VIEW[1]-(self.pos_of[1]-translation[1])*PPM))
        screen.blit(self.puffs[frame],rect.topleft)
class Log(Thing):
    def __init__(self,img,pos,angle,scale=1):
        self.dead = False
        super().__init__(img,pos,angle,BOX,density=1,scale=scale)
        self.shatters = [
            pygame.image.load("anger_art/shatter1.png").convert_alpha(),
            pygame.image.load("anger_art/shatter2.png").convert_alpha(),
            pygame.image.load("anger_art/shatter3.png").convert_alpha()]
    def drawShatter(self,translation,frame):
        rect = self.shatters[frame].get_rect(
            center=((self.pos_of[0]-translation[0])*PPM,
            VIEW[1]-(self.pos_of[1]-translation[1])*PPM))
        screen.blit(self.shatters[frame],rect.topleft)


class Level():
    def __init__(self,logs,base,hogs,birds):
        self.base = base
        self.logs = logs
        self.hogs = hogs
        self.birds = birds
        self.num_hogs = len(hogs)
