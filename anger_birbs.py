

from anger_common import *
from anger_sprites import *

TRANS = 0, 0

game = True
running = True
art = True

pygame.init()


def show_text(text, x, y, color, size):
    text_list = text.split('*')
    lines = 0
    for line in text_list:
        lines+=1
    size = int(size*((.9)**(lines-1)))
    if lines == 2:
        y = y-size//2
    elif lines == 3:
        y = y-size*1.1
    font = pygame.font.Font("pixels.ttf", size)
    for line in text_list:
        TextSurf,  TextRect = ((font.render(line, True, color)),
            (font.render(line, True, color)).get_rect())
        TextRect.center = (x, y)
        screen.blit(TextSurf, TextRect)
        y+=size

def make_log(pos, rotation, size):
    if size == 0:
        a_log = Log(log_short_art, pos, rotation, BOX)
    elif size == 1:
        a_log = Log(log_long_art, pos, rotation, BOX)
    elif size == 2:
        a_log = Log(log_looong_art, pos, rotation, BOX)
    return a_log


def make_lvl1():
    birds = []
    hogs = []
    logs = []
    base = 12

    basic = Bird(basic_art, (1.5, .5), 0)
    birds.append(basic)
    redwing = Bird(redwing_art, (.5, .5), 0)
    birds.append(redwing)
    bluebird = Bird(bluebird_art, (1, .5), 0)
    birds.append(bluebird)

    global hedgehog_art
    hedgehog_art = pygame.transform.flip(hedgehog_art, True, False)
    hog_infos = [((0, 3.75), 0)]
    for info in hog_infos:
        a_hog = Hog(hedgehog_art, (info[0][0]+base, info[0][1]), info[1])
        hogs.append(a_hog)

    log_infos = [((-.5, 1), 90, 1), ((.5, 1), 90, 1),
        ((0, 2), 0, 1), ((-.3, 3), 90, 0),
        ((.2, 3), 90, 0), ((0, 3.5), 0, 0)]
    for info in log_infos:
        a_log = make_log((info[0][0]+base, info[0][1]), info[1], info[2])
        logs.append(a_log)

    lvl1 = Level(logs, base, hogs, birds)
    return lvl1


def make_lvl2():
    birds = []
    hogs = []
    logs = []
    base = 12

    basic = Bird(basic_art, (1.5, .5), 0)
    birds.append(basic)
    redwing = Bird(redwing_art, (.5, .5), 0)
    birds.append(redwing)
    bluebird = Bird(bluebird_art, (1, .5), 0)
    birds.append(bluebird)

    global hedgehog_art
    hedgehog_art = pygame.transform.flip(hedgehog_art, True, False)
    hog_infos = [((0, 3), 0), ((-.75, 1), 0), ((.75, 1), 0)]
    for info in hog_infos:
        a_hog = Hog(hedgehog_art, (info[0][0]+base, info[0][1]), info[1])
        hogs.append(a_hog)

    log_infos = [((-1.5, 1.0), 90, 0), ((1.5, 1.0), 90, 0), ((0, 1.0), 90, 0),
        ((0, 1.5), 0, 2), ((-.25, 2.0), 90, 0), ((.25, 2.0), 90, 0),
        ((0, 2.5), 0, 1)]
    for info in log_infos:
        a_log = make_log((info[0][0]+base, info[0][1]), info[1], info[2])
        logs.append(a_log)

    lvl2 = Level(logs, base, hogs, birds)
    return lvl2

def make_lvl3():
    birds = []
    hogs = []
    logs = []
    base = 12

    basic = Bird(basic_art, (1.5, .5), 0)
    birds.append(basic)
    redwing = Bird(redwing_art, (.5, .5), 0)
    birds.append(redwing)
    bluebird = Bird(bluebird_art, (1, .5), 0)
    birds.append(bluebird)

    global hedgehog_art
    hedgehog_art = pygame.transform.flip(hedgehog_art, True, False)
    hog_infos = [((0, 2.5), 0)]
    for info in hog_infos:
        a_hog = Hog(hedgehog_art, (info[0][0]+base, info[0][1]), info[1])
        hogs.append(a_hog)

    log_infos = [((-1, 1.0), 90, 0), ((0, 1.2), 90, 1), ((1, 2), 90, 2)]
    for info in log_infos:
        a_log = make_log((info[0][0]+base, info[0][1]), info[1], info[2])
        logs.append(a_log)

    lvl3 = Level(logs, base, hogs, birds)
    return lvl3


def draw_sling(color, slingshot, translation):
    if in_sling is not None:
        pygame.draw.line(screen, color,
            ((slingshot.anchora.position[0]-translation[0])*PPM,
            VIEW[1]-(slingshot.anchora.position[1]-translation[1])*PPM),
            ((in_sling.body.position[0]-translation[0])*PPM,
            VIEW[1]-(in_sling.body.position[1]-translation[1])*PPM), 4)
        pygame.draw.line(screen, color,
            ((slingshot.anchorb.position[0]-translation[0])*PPM,
            VIEW[1]-(slingshot.anchorb.position[1]-translation[1])*PPM),
            ((in_sling.body.position[0]-translation[0])*PPM,
            VIEW[1]-(in_sling.body.position[1]-translation[1])*PPM), 4)
    else:
        pygame.draw.line(screen, color,
            ((slingshot.anchora.position[0]-translation[0])*PPM,
            VIEW[1]-(slingshot.anchora.position[1]-translation[1])*PPM),
            ((slingshot.anchorb.position[0]-translation[0])*PPM,
            VIEW[1]-(slingshot.anchorb.position[1]-translation[1])*PPM), 4)


in_sling = None
time_shot = -1000
clicked = False
pan_to = False
pan_back = False
pan_stop = 0

slingshot = Slingshot(slingshot_art, (1.5, 1.4))
ground = Thing(ground_art, (10, 0), 0, BOX, static=True)

levels = [make_lvl3, make_lvl1, make_lvl2]
level = levels[0]()
level_num = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos = (pos[0]/PPM)+TRANS[0], (VIEW[1]-pos[1])/PPM+TRANS[1]
            if in_sling != None:
                if in_sling.fix.TestPoint(pos):
                    clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and clicked:
            clicked = False
            in_sling.launch(screen, slingshot, TRANS)
            in_sling.shot = True
            in_sling = None
            time_shot = pygame.time.get_ticks()
            pan_to = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if in_sling == None:
        birds_not_shot = 0
        for bird in level.birds:
            if not bird.shot:
                birds_not_shot+=1
        if birds_not_shot>0 and pygame.time.get_ticks()-time_shot >= 1000:
            i = 0
            while in_sling == None:
                if not level.birds[i].shot:
                    level.birds[i].load(slingshot)
                    in_sling = level.birds[i]
                    level.birds[i].body.awake = False
                    level.birds[i].shot = True
                else:
                    i+=1
    else:
        if clicked:
            posa = pygame.mouse.get_pos()
            posa = (posa[0]/PPM)+TRANS[0], (VIEW[1]-posa[1])/PPM+TRANS[1]
            posb = slingshot.rect.centerx, slingshot.rect.y+10
            posb = posb[0]/PPM,  (VIEW[1]-posb[1])/PPM
            length = (((posb[0]-posa[0])**2+
                (posb[1]-posa[1])**2)**(1/2))
            if length<=1.0:
                in_sling.body.transform = (posa, 0)
            else:
                reduct = 1.0/length
                move = (posb[0]-(posb[0]-posa[0])*reduct,
                    posb[1]-(posb[1]-posa[1])*reduct)
                in_sling.body.transform = (move, in_sling.body.angle)
        else:
            in_sling.body.awake=False

    for item in level.hogs+level.logs:
        if not item.dead:
            v1 = item.getV()
            v1 = (v1[0]**2+v1[1]**2)**(1/2)
            item.lastv = v1

    world.Step(TIME_STEP/2, 5, 5)
    world.Step(TIME_STEP/2, 5, 5)

    for item in level.hogs+level.logs:
        if not item.dead:
            v  = item.getV()
            v = (v[0]**2+v[1]**2)**(1/2)
            if type(item)==Hog:
                if abs(v-item.lastv)>1.5:
                    item.dead = True
                    item.time_of = pygame.time.get_ticks()
                    item.pos_of = item.body.position
                    world.DestroyBody(item.body)
            else:
                if abs(v-item.lastv)>4:
                    item.dead = True
                    item.time_of = pygame.time.get_ticks()
                    item.pos_of = item.body.position
                    world.DestroyBody(item.body)

    for hog in level.hogs:
        if hog.body.position[1]<0:
            level.hogs.remove(hog)
            world.DestroyBody(hog.body)
    for bird in level.birds:
        if bird.body.position[1]<0:
            level.birds.remove(bird)
            world.DestroyBody(bird.body)
    for log in level.logs:
        if log.body.position[1]<0:
            level.logs.remove(log)
            world.DestroyBody(log.body)

    for hog in level.hogs:
        if hog.dead and pygame.time.get_ticks()-hog.time_of>=300:
            level.hogs.remove(hog)
    for log in level.logs:
        if log.dead and pygame.time.get_ticks()-log.time_of>=300:
            level.logs.remove(log)


    if (pan_back == False and TRANS[0]==level.base-VIEW[0]/PPM//2
        and pygame.time.get_ticks()-pan_stop>5000):
        pan_back = True
        all = []
        for log in level.logs:
            all.append(log)
        for hog in level.hogs:
            all.append(hog)
        for each in all:
            v1 = each.getV()
            v1 = (v1[0]**2+v1[1]**2)**(1/2)
            if abs(v1)>.2:
                pan_back = False

    if pan_to:
        pan_back=False
        if TRANS[0]!=level.base-VIEW[0]/PPM//2:
            TRANS = TRANS[0]+.25, TRANS[1]
        else:
            pan_to = False
            pan_stop = pygame.time.get_ticks()
    elif pan_back:
        if TRANS[0]!=0:
            TRANS = TRANS[0]-.25, TRANS[1]
        else:
            pan_back = False

    hogs_down = level.num_hogs-len(level.hogs)
    if hogs_down == level.num_hogs:
        for item in level.hogs+level.logs+level.birds:
            world.DestroyBody(item.body)
        in_sling = None
        TRANS = 0, 0
        if level_num+1<=len(levels):
            level = levels[level_num+1]()
            level_num +=1

    if art:
        screen.fill((128, 216, 255))
        screen.blit(background_art, (-1*TRANS[0]*PPM, TRANS[1]*PPM))
        ground.draw(TRANS)
        slingshot.draw(TRANS)
        draw_sling(SLING_COLOR, slingshot, TRANS)
        for bird in level.birds:
            bird.draw(TRANS)
        for hog in level.logs:
            if hog.dead:
                if pygame.time.get_ticks()-hog.time_of<100:
                    hog.drawShatter(TRANS, 0)
                elif pygame.time.get_ticks()-hog.time_of<200:
                    hog.drawShatter(TRANS, 1)
                elif pygame.time.get_ticks()-hog.time_of<300:
                    hog.drawShatter(TRANS, 2)
            elif not hog.dead:
                hog.draw(TRANS)
        for hog in level.hogs:
            if hog.dead:
                if pygame.time.get_ticks()-hog.time_of<100:
                    hog.drawPuff(TRANS, 0)
                elif pygame.time.get_ticks()-hog.time_of<200:
                    hog.drawPuff(TRANS, 1)
                elif pygame.time.get_ticks()-hog.time_of<300:
                    hog.drawPuff(TRANS, 2)
            elif not hog.dead:
                hog.draw(TRANS)
        show_text(str(hogs_down)
            +"/"+str(level.num_hogs), 720, 100, (255, 255, 102), 40)

    elif not art:
        screen.fill((0, 0, 0))
        ground.draw_shape(TRANS)
        for log in level.logs:
            log.draw_shape(TRANS)
        for bird in level.birds:
            bird.draw_shape(TRANS)
        for hog in level.hogs:
            if not hog.dead:
                hog.draw_shape(TRANS)
        for hog in level.hogs:
            if hog.dead and pygame.time.get_ticks()-hog.time_of>=300:
                level.hogs.remove(hog)
        draw_sling(WHITE, slingshot, TRANS)

    pygame.display.flip()
    clock.tick(FPS)
print(pygame.display.get_wm_info())
pygame.quit()
