
from anger_common import *
from anger_sprites import *
from lvl_makers import *

TRANS = 0, 0

running = True
art = True

pygame.init()

def get_v(body):
    v = body.linearVelocity
    v = (v[0] ** 2 + v[1] ** 2) ** (1 / 2)
    return v


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

game = True

m_main = False
main_buttons = [Button(SKY,WHITE,"start",40,(620,650,200,75))]

slingshot = Slingshot(slingshot_art, (1.5, 1.4))
ground = Thing(ground_art, (10, 0), 0, BOX, static=True)

levels = [make_lvl1, make_lvl2, make_lvl3, make_lvl4]
level = levels[0]()
level_num = 0

while running:
    if game:
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
            if item.contact_impulse>item.min_impulse:
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
                if not log.dead and abs(log.body.position[0]-level.base)<3:
                    all.append(log)
            for hog in level.hogs:
                if not hog.dead and abs(hog.body.position[0]-level.base)<3:
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
        if hogs_down == level.num_hogs and level_num<len(levels)-1:
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
            level = levels[level_num + 1]()
            level_num += 1


        if art:
            screen.fill(SKY)
            screen.blit(level.background, (-1 * TRANS[0] * PPM, TRANS[1] * PPM))
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
                      "/" + str(level.num_hogs), 720, 100, YELLOW, 40)

        elif not art:
            screen.fill(BLACK)
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

    elif m_main:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(back_sunset_art, (0,0))
        show_text("anger birbs!", 720, 225, YELLOW, 100)
        for each in main_buttons:
            each.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
