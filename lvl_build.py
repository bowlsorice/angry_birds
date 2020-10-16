#lvl_build.py
from anger_common import *
from anger_sprites import *

running = True
TRANS = 0, 0
ice = False
BLUE = (165,242,243)
RED = (255,0,0)

class Button:
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

def get_world_pos():
    pos = pygame.mouse.get_pos()
    world_pos = pos[0]/PPM+TRANS[0], (VIEW[1]-pos[1])/PPM+TRANS[1]
    return world_pos


buttons = []
clicked = {}

add_log1 = Button(WHITE,BLACK,"add short log",20,(1220,50,180,40))
buttons.append(add_log1)
add_log2 = Button(WHITE,BLACK,"add med log",20,(1220,100,180,40))
buttons.append(add_log2)
add_log3 = Button(WHITE,BLACK,"add long log",20,(1220,150,180,40))
buttons.append(add_log3)
ice_button = Button(BLUE,WHITE,"ice",20,(1220,200,180,40))
buttons.append(ice_button)

ground = Thing(ground_art, (10, 0), 0, BOX, static=True)
items = []

while running:
    for event in pygame.event.get():
        clicking = False
        for item in items:
            if clicked.get(item):
                clicking = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT:
                if not clicking:
                    if TRANS[0]<5.5:
                        TRANS = TRANS[0]+.5, TRANS[1]
                else:
                    for item in items:
                        if clicked.get(item):
                            item.body.transform = (get_world_pos(),
                                                item.body.angle - pi/6)
            elif event.key == pygame.K_LEFT:
                if not clicking:
                    if TRANS[0]>0.0:
                        TRANS = TRANS[0]-.5, TRANS[1]
                else:
                    for item in items:
                        if clicked.get(item):
                            item.body.transform = (get_world_pos(),
                                                item.body.angle + pi/6)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if (add_log1.rect.left<pos[0]<add_log1.rect.right
                and add_log1.rect.top<pos[1]<add_log1.rect.bottom):
                items.append(Log((1, 5), 0, 0, ice))
            elif (add_log2.rect.left<pos[0]<add_log2.rect.right
                and add_log2.rect.top<pos[1]<add_log2.rect.bottom):
                items.append(Log((1, 5), 0, 1, ice))
            elif (add_log3.rect.left<pos[0]<add_log3.rect.right
                and add_log3.rect.top<pos[1]<add_log3.rect.bottom):
                items.append(Log((1, 5), 0, 2, ice))
            elif (ice_button.rect.left<pos[0]<ice_button.rect.right
                and ice_button.rect.top<pos[1]<ice_button.rect.bottom):
                if ice:
                    ice = False
                    ice_button.colora = BLUE
                    ice_button.colorb = WHITE
                elif not ice:
                    ice = True
                    ice_button.colora = WHITE
                    ice_button.colorb = BLACK
            for item in items:
                if not clicked.get(item):
                    clicked[item] = item.fix.TestPoint(get_world_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            for item in items:
                if clicked.get(item):
                    clicked[item] = False
                    item.body.awake = True
                    item.body.linearVelocity = 0,0
    for item in items:
        if clicked.get(item):
            item.body.transform = get_world_pos(), item.body.angle
            item.body.awake = False


    world.Step(TIME_STEP, 10, 10)

    screen.blit(background_art, (-1 * TRANS[0] * PPM, TRANS[1] * PPM))
    ground.draw(TRANS)
    pygame.draw.line(screen, WHITE, (720-TRANS[0]*PPM,850),
        (720-TRANS[0]*PPM,0))
    for item in items:
        item.draw(TRANS)
    for button in buttons:
        button.draw()
    pygame.display.flip()

log_infos = []
for item in items:
    if type(item)==Log:
        log_infos.append(((item.body.position[0]-7.2,item.body.position[1]),
            item.body.angle*(180/pi), item.shape, item.is_ice))
print(log_infos)
pygame.quit()
