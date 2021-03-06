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
        self.contact_impulse = 0
        self.min_impulse = 2.0
        if static:
            self.body = world.CreateStaticBody(position=(pos),angle=angle,
                        userData=self)
        else:
            self.body = world.CreateDynamicBody(position=(pos),
                        fixedRotation=False,angle=angle, userData = self)
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
        elif shape == RIGHT_TRIANGLE:
                rect = self.img.get_rect()
                width = rect.width/PPM
                height = rect.height/PPM
                vertices = [(-width/2,-height/2),(width/2,-height/2),(-width/2,height/2)]
                self.fix = self.body.CreatePolygonFixture(density = density,
                            vertices = vertices,friction=0.3,
                            restitution=.5)
    def draw(self,translation):
        angle = self.body.angle * (180/pi)
        r_img = pygame.transform.rotate(self.img,angle)
        center = ((self.body.position[0]-translation[0])*PPM,
            VIEW[1]-((self.body.position[1]-translation[1])*PPM))
        rect = r_img.get_rect(center = center) #edit here
        screen.blit(r_img,(rect.topleft))
    def draw_shape(self,translation):
        pos = ((self.body.position[0]-translation[0])*PPM,
            VIEW[1]-((self.body.position[1]-translation[1])*PPM))
        if self.shape == BOX or self.shape == RIGHT_TRIANGLE:
            vertices = [(self.body.transform * v)
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



class Bird(Thing):
    def __init__(self,pos,angle,tag):
        self.tag = tag
        self.impulse_cap = 8
        self.use_ability = False
        if tag == "basic":
            img = basic_art
        elif tag == "redwing":
            img = redwing_art
            self.use_ability = True
        elif tag == "bluebird":
            img = bluebird_art
        elif tag == "gold":
            img = gold_art
            self.use_ability = True
            self.impulse_cap = 4
        super().__init__(img,pos,angle,CIRCLE,density=4)#CIRCLE,density=4)
        self.shot = False
    def launch(self,screen,slingshot,translation):
        posa = self.body.position
        posb = slingshot.rect.centerx,slingshot.rect.y
        posb = (posb[0]/PPM), (VIEW[1]-posb[1])/PPM
        reduct = self.impulse_cap
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
        self.anchora = world.CreateStaticBody(position=(anchora),angle=0,
                        userData=self)
        self.anchorb = world.CreateStaticBody(position=(anchorb),angle=0,
                        userData=self)
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

class Scene(Thing):
    def kill(self):
        self.dead = True
        self.time_of = pygame.time.get_ticks()
        self.pos_of = self.body.position
        world.DestroyBody(self.body)
        self.body = None
    def drawDeath(self, translation, frame):
        rect = self.frames[frame].get_rect(
            center=((self.pos_of[0] - translation[0]) * PPM,
            VIEW[1]-(self.pos_of[1] - translation[1]) * PPM))
        screen.blit(self.frames[frame], rect.topleft)

class Hog(Scene):
    def __init__(self, pos, angle):
        self.dead  = False
        self.min_impulse = .6
        super().__init__(hedgehog_art, pos, angle, CIRCLE, density=4)
        self.frames = [puff1, puff2, puff3]
    def kill(self):
        super().kill()
        pygame.mixer.Sound.play(snort)



class Log(Scene):
    def __init__(self, pos, angle, log_shape, is_ice):
        self.dead = False
        self.is_ice = is_ice
        if log_shape == 0:
            if is_ice:
                img = ice_short_art
            else:
                img = log_short_art
        elif log_shape == 1:
            if is_ice:
                img = ice_long_art
            else:
                img = log_long_art
        elif log_shape == 2:
            if is_ice:
                img = ice_looong_art
            else:
                img = log_looong_art
        elif log_shape == 3:
            if is_ice:
                img = ice_triangle_art
            else:
                img = log_triangle_art
        if 0<=log_shape<=2:
            super().__init__(img,pos,angle,BOX)
        elif log_shape == 3:
            super().__init__(img,pos,angle,RIGHT_TRIANGLE)
        if is_ice:
            self.frames = [ice_shatter1, ice_shatter2, ice_shatter3]
            self.min_impulse = .8
        else:
            self.frames = [shatter1, shatter2, shatter3]
        self.log_shape = log_shape
    def kill(self):
        super().kill()
        if not self.is_ice:
            pygame.mixer.Sound.play(smash)
        else:
            pygame.mixer.Sound.play(smash_ice)


class Level():
    def __init__(self,logs,base,hogs,birds,background,ground_art):
        self.background = background
        self.base = base
        self.logs = logs
        self.hogs = hogs
        self.birds = birds
        self.num_hogs = len(hogs)
        self.ground = Thing(ground_art, (10, 0), 0, BOX, static=True)

class Button():
    def __init__(self,colora,colorb,text,textsize,rect):
        self.rect = pygame.Rect(rect)
        self.colora = colora
        self.colorb = colorb
        self.text = text
        self.size = textsize
    def draw(self):
        pygame.draw.rect(screen,self.colora,self.rect)
        show_text(self.text,self.rect[0]+self.rect[2]/2,
                    self.rect[1]+self.size,self.colorb,self.size)
    def isClicked(self):
        pos = pygame.mouse.get_pos()
        clicked = (self.rect.left<pos[0]<self.rect.right
            and self.rect.top<pos[1]<self.rect.bottom)
        if clicked:
            pygame.mixer.Sound.play(click)
        return clicked

class IconButton(Button):
    def __init__(self,img,x,y):
        self.img = img
        self.rect = img.get_rect()
        self.rect = pygame.rect.Rect(x-self.rect.width/2, y-self.rect.height/2,
                    self.rect[2], self.rect[3])
    def draw(self):
        screen.blit(self.img, self.rect.topleft)

class SelectButton(Button):
    def __init__(self, level_num):
        super().__init__(WHITE,SKY,str(level_num),30,
                (470+70*(level_num-1),350,60,60))
        if level_num!=1:
            self.unlocked = False
        else:
            self.unlocked = True
    def draw(self):
        if self.unlocked:
            super().draw()
        else:
            pygame.draw.rect(screen,self.colora,self.rect)
            pygame.draw.rect(screen,self.colorb,
                            (self.rect[0]+10,self.rect[1]+20,40,30))
            pygame.draw.circle(screen, self.colorb,
                                (self.rect.centerx,self.rect.y+20), 10, 2)
            pygame.draw.rect(screen, self.colora,
                            (self.rect.x+30,self.rect.y+30,2,10))


def show_text(text, x, y, color, size):
    text_list = text.split('*')
    lines = 0
    for line in text_list:
        lines += 1
    size = int(size * (.9 ** (lines -1)))
    if lines == 2:
        y = y - size // 2
    elif lines == 3:
        y = y - size * 1.1
    font = pygame.font.Font("pixels.ttf", size)
    for line in text_list:
        text_surf, text_rect = ((font.render(line, True, color)),
                              (font.render(line, True, color)).get_rect())
        text_rect.center = (x, y)
        screen.blit(text_surf, text_rect)
        y += size
