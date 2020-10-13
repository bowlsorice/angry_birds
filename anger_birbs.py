
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


def make_logs(info_list,base):
    logs = []
    for each in info_list:
        if each [-1] == "ice":
            a_log = Log((each[0][0]+base,each[0][1]),
                    each[1], each[2],is_ice=True)
        else:
            a_log = Log((each[0][0]+base,each[0][1]),
                    each[1], each[2])
        logs.append(a_log)
    return logs

def make_hogs(info_list,base):
    hogs = []
    for info in info_list:
        a_hog = Hog((info[0][0] + base, info[0][1]), info[1])
        hogs.append(a_hog)
    return hogs

def get_v(body):
    v = body.linearVelocity
    v = (v[0] ** 2 + v[1] ** 2) ** (1 / 2)
    return v



def make_lvl1():
    base = 12

    birds = []
    basic = Bird(basic_art, (1.5, .5), 0)
    birds.append(basic)
    redwing = Bird(redwing_art, (.5, .5), 0)
    birds.append(redwing)
    bluebird = Bird(bluebird_art, (1, .5), 0)
    birds.append(bluebird)

    hog_infos = [((-5,1),0)]#((0, 2.0), 0)]
    hogs = make_hogs(hog_infos, base)

    log_infos = [((-1, 1.0), 90, 0), ((0, 1.2), 90, 1), ((1, 2), 90, 2),
                ((-5,8),0,0)]
    logs = make_logs(log_infos,base)

    lvl1 = Level(logs, base, hogs, birds)
    return lvl1


def make_lvl2():
    base = 12

    birds = []
    basic = Bird(basic_art, (1.5, .5), 0)
    birds.append(basic)
    redwing = Bird(redwing_art, (.5, .5), 0)
    birds.append(redwing)
    bluebird = Bird(bluebird_art, (1, .5), 0)
    birds.append(bluebird)

    hog_infos = [((0, 3.6), 0)]
    hogs = make_hogs(hog_infos, base)

    log_infos = [((-.5, 1), 90, 1, "ice"), ((.5, 1), 90, 1, "ice"),
                 ((0, 2), 0, 1), ((-.3, 3), 90, 0),
                 ((.2, 3), 90, 0), ((0, 3.5), 0, 0, "ice")]
    logs = make_logs(log_infos,base)

    lvl2 = Level(logs, base, hogs, birds)
    return lvl2


def make_lvl3():
    base = 12

    birds = []
    basic = Bird(basic_art, (1.5, .5), 0)
    birds.append(basic)
    redwing = Bird(redwing_art, (.5, .5), 0)
    birds.append(redwing)
    bluebird = Bird(bluebird_art, (1, .5), 0)
    birds.append(bluebird)

    hog_infos = [((0, 3), 0), ((-.75, 1), 0), ((.75, 1), 0)]
    hogs = make_hogs(hog_infos, base)

    log_infos = [((-1.5, 1.0), 90, 0, "ice"), ((1.5, 1.0), 90, 0, "ice"),
                ((0, 1.0), 90, 0, "ice"), ((0, 1.5), 0, 2),
                ((-.25, 2.0), 90, 0), ((.25, 2.0), 90, 0),
                ((0, 2.5), 0, 1)]
    logs = make_logs(log_infos,base)

    lvl3 = Level(logs, base, hogs, birds)
    return lvl3


def draw_sling(color, slingshot, translation):
    if in_sling is not None:
        pygame.draw.line(screen, color,
                         ((slingshot.anchora.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (slingshot.anchora.position[1]
                           - translation[1]) * PPM),
                         ((in_sling.body.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (in_sling.body.position[1]
                           - translation[1]) * PPM), 4)
        pygame.draw.line(screen, color,
                         ((slingshot.anchorb.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (slingshot.anchorb.position[1]
                           - translation[1]) * PPM),
                         ((in_sling.body.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (in_sling.body.position[1]
                           - translation[1]) * PPM), 4)
    else:
        pygame.draw.line(screen, color,
                         ((slingshot.anchora.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (slingshot.anchora.position[1]
                           - translation[1]) * PPM),
                         ((slingshot.anchorb.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (slingshot.anchorb.position[1]
                           - translation[1]) * PPM), 4)


in_sling = None
time_shot = -1000
clicked = False
pan_to = False
pan_back = False
pan_stop = 0

slingshot = Slingshot(slingshot_art, (1.5, 1.4))
ground = Thing(ground_art, (10, 0), 0, BOX, static=True)

levels = [make_lvl1, make_lvl2, make_lvl3]
level = levels[0]()
level_num = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos = (pos[0] / PPM) + TRANS[0], (VIEW[1] - pos[1]) / PPM + TRANS[1]
            if in_sling is not None:
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
                birds_not_shot += 1
        if birds_not_shot > 0 and pygame.time.get_ticks() - time_shot >= 1000:
            i = 0
            while in_sling == None:
                if not level.birds[i].shot:
                    level.birds[i].load(slingshot)
                    in_sling = level.birds[i]
                    level.birds[i].body.awake = False
                    level.birds[i].shot = True
                else:
                    i += 1
    else:
        if clicked:
            posa = pygame.mouse.get_pos()
            posa = ((posa[0] / PPM) + TRANS[0],
                    (VIEW[1] - posa[1]) / PPM + TRANS[1])
            posb = slingshot.rect.centerx, slingshot.rect.y + 10
            posb = posb[0] / PPM, (VIEW[1] - posb[1]) / PPM
            length = (((posb[0] - posa[0]) ** 2 +
                       (posb[1] - posa[1]) ** 2) ** (1 / 2))
            if length <= 1.0:
                in_sling.body.transform = (posa, 0)
            else:
                reduct = 1.0 / length
                move = (posb[0] - (posb[0] - posa[0]) * reduct,
                        posb[1] - (posb[1] - posa[1]) * reduct)
                in_sling.body.transform = (move, in_sling.body.angle)
        else:
            in_sling.body.awake = False

    for item in level.hogs + level.logs:
        if not item.dead:
            lastv = get_v(item.body)
            item.lastv = lastv

    world.Step(TIME_STEP / 2, 5, 5)
    world.Step(TIME_STEP / 2, 5, 5)

    alive = []
    for item in level.hogs + level.logs:
        if not item.dead:
            alive.append(item)

    for item in alive:
        v = get_v(item.body)
        if abs(v - item.lastv) > item.minv:
            item.kill()
        elif abs(item.body.linearVelocity[1])<.5:
            for contact in item.body.contacts:
                other_v = get_v(contact.other)
                if other_v>item.minv:
                    item.kill()


    for hog in level.hogs:
        if not hog.dead:
            if hog.body.position[1] < 0:
                world.DestroyBody(hog.body)
                level.hogs.remove(hog)
                hog.body = None
    for bird in level.birds:
        if bird.body.position[1] < 0:
            world.DestroyBody(bird.body)
            level.birds.remove(bird)
            bird.body = None
    for log in level.logs:
        if not log.dead:
            if log.body.position[1] < 0:
                world.DestroyBody(log.body)
                level.logs.remove(log)
                log.body = None

    for hog in level.hogs:
        if hog.dead and pygame.time.get_ticks() - hog.time_of >= 300:
            level.hogs.remove(hog)
    for log in level.logs:
        if log.dead and pygame.time.get_ticks() - log.time_of >= 300:
            level.logs.remove(log)

    if (pan_back is False and TRANS[0] == level.base - VIEW[0] / PPM // 2
            and pygame.time.get_ticks() - pan_stop > 5000):
        pan_back = True
        all = []
        for log in level.logs:
            if not log.dead:
                all.append(log)
        for hog in level.hogs:
            if not hog.dead:
                all.append(hog)
        for each in all:
            v = get_v(each.body)
            if abs(v) > .2:
                pan_back = False

    if pan_to:
        pan_back = False
        if TRANS[0] != level.base - VIEW[0] / PPM // 2:
            TRANS = TRANS[0] + .25, TRANS[1]
        else:
            pan_to = False
            pan_stop = pygame.time.get_ticks()
    elif pan_back:
        if TRANS[0] != 0:
            TRANS = TRANS[0] - .25, TRANS[1]
        else:
            pan_back = False

    hogs_down = level.num_hogs - len(level.hogs)
    if hogs_down == level.num_hogs:
        for item in level.hogs + level.logs + level.birds:
            if item in level.birds:
                world.DestroyBody(item.body)
                item.body = None
            else:
                if not item.dead:
                    world.DestroyBody(item.body)
                    item.body = None
        in_sling = None
        TRANS = 0, 0
        if level_num + 1 <= len(levels):
            level = levels[level_num + 1]()
            level_num += 1

    if art:
        screen.fill((128, 216, 255))
        screen.blit(background_art, (-1 * TRANS[0] * PPM, TRANS[1] * PPM))
        ground.draw(TRANS)
        slingshot.draw(TRANS)
        draw_sling(SLING_COLOR, slingshot, TRANS)
        for bird in level.birds:
            bird.draw(TRANS)
        for item in level.logs+level.hogs:
            if item.dead:
                if pygame.time.get_ticks() - item.time_of < 100:
                    item.drawDeath(TRANS, 0)
                elif pygame.time.get_ticks() - item.time_of < 200:
                    item.drawDeath(TRANS, 1)
                elif pygame.time.get_ticks() - item.time_of < 300:
                    item.drawDeath(TRANS, 2)
            elif not item.dead:
                item.draw(TRANS)
        show_text(str(hogs_down) +
                  "/" + str(level.num_hogs), 720, 100, (255, 255, 102), 40)

    elif not art:
        screen.fill((0, 0, 0))
        ground.draw_shape(TRANS)
        for log in level.logs:
            if not log.dead:
                log.draw_shape(TRANS)
        for bird in level.birds:
            bird.draw_shape(TRANS)
        for hog in level.hogs:
            if not hog.dead:
                hog.draw_shape(TRANS)
        draw_sling(WHITE, slingshot, TRANS)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
