#lvl_build.py
from anger_common import *
from anger_sprites import *

running = True
TRANS = 0, 0
ice = False
sleep = False



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
add_log4 = Button(WHITE,BLACK,"add tri log",20,(1220,350,180,40))
buttons.append(add_log4)
ice_button = Button(BLUE,WHITE,"ice",20,(1220,200,180,40))
buttons.append(ice_button)
add_hog = Button(WHITE,BLACK,"add hog",20,(1220,250,180,40))
buttons.append(add_hog)
all_sleep = Button(WHITE, BLACK, "sleep",20,(1220,300,180,40))
buttons.append(all_sleep)

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
            elif event.key == pygame.K_BACKSPACE:
                for item in items:
                    if clicked.get(item):
                        world.DestroyBody(item.body)
                        items.remove(item)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if add_log1.isClicked():
                items.append(Log((1, 5), 0, 0, ice))
            elif add_log2.isClicked():
                items.append(Log((1, 5), 0, 1, ice))
            elif add_log3.isClicked():
                items.append(Log((1, 5), 0, 2, ice))
            elif add_log4.isClicked():
                items.append(Log((1,5), 0, 3, ice))
            elif ice_button.isClicked():
                if ice:
                    ice = False
                    ice_button.colora = BLUE
                    ice_button.colorb = WHITE
                    ice_button.text = "ice"
                elif not ice:
                    ice = True
                    ice_button.colora = WHITE
                    ice_button.colorb = BLACK
                    ice_button.text = "wood"
            elif add_hog.isClicked():
                items.append(Hog((1, 5), 0))
            elif all_sleep.isClicked():
                if not sleep:
                    sleep = True
                    all_sleep.text = "wake"
                elif sleep:
                    sleep = False
                    all_sleep.text = "sleep"
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
        if item.body.position[1]<0:
            world.DestroyBody(item.body)
            items.remove(item)
        if sleep:
            for item in items:
                item.body.awake = False
        else:
            for item in items:
                item.body.awake = True
    for item in items:
        if clicked.get(item):
            angle = item.body.angle
            angle = angle/(pi/6)
            angle = round(angle,0)
            angle = angle*(pi/6)
            item.body.transform = get_world_pos(), angle
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
hog_infos = []
for item in items:
    if type(item) == Log:
        log_infos.append(((round(item.body.position[0]-7.2,4),
                        round(item.body.position[1],4)),
                        item.body.angle*(180/pi), item.log_shape, item.is_ice))
    elif type(item) == Hog:
        hog_infos.append(((round(item.body.position[0]-7.2,4),
                        (round(item.body.position[1],4))),0))
print("logs: "+str(log_infos))
print("hogs: "+str(hog_infos))
pygame.quit()
