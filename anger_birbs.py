
from anger_common import *
from anger_sprites import *
from lvl_makers import *

TRANS = 0, 0

running = True
art = True
draw_anyways = False
test_mode = False

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
                           - translation[1]) * PPM), 5)
        pygame.draw.line(screen, color,
                         ((slingshot.anchorb.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (slingshot.anchorb.position[1]
                           - translation[1]) * PPM),
                         ((in_sling.body.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (in_sling.body.position[1]
                           - translation[1]) * PPM), 5)
    else:
        pygame.draw.line(screen, color,
                         ((slingshot.anchora.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (slingshot.anchora.position[1]
                           - translation[1]) * PPM),
                         ((slingshot.anchorb.position[0]
                          - translation[0]) * PPM,
                          VIEW[1] - (slingshot.anchorb.position[1]
                           - translation[1]) * PPM), 5)


in_sling = None
last_shot = None
time_shot = -1000
clicked = False

pan_to = False
pan_back = False
pan_stop = 0

game = False

m_main = True
main_buttons = []
start_button = Button(SKY,WHITE,"start",40,(620,550,200,75))
main_buttons.append(start_button)
main_level_select = Button(SKY,WHITE,"levels",40,(620,650,200,75))
main_buttons.append(main_level_select)

m_pause = False
pause_buttons = []
unpause = Button(THEME,WHITE,"unpause",30,(645,420,150,50))
quit_from_pause = Button(THEME,WHITE,"quit",30,(670,560,100,50))
pause_level_select = Button(THEME,WHITE,"level select",30,(605,490,230,50))
pause_buttons.append(unpause)
pause_buttons.append(quit_from_pause)
pause_buttons.append(pause_level_select)

m_level_select = False
select_buttons = []
quit_from_select = Button(WHITE,SKY,"quit",30,(870,590,100,60))
select_buttons.append(quit_from_select)
select_level_nums = []
num = 1
for i in range(6):
    button = SelectButton(num)
    select_level_nums.append(button)
    select_buttons.append(button)
    num+=1
    if test_mode:
        button.unlocked = True


level_buttons = []
pause_button = IconButton(pause_art, 100, 60)
rewind_button = IconButton(rewind_art, 200, 60)
level_buttons.append(pause_button)
level_buttons.append(rewind_button)

slingshot = Slingshot(slingshot_art, (1.5, 1.4))

levels = [make_lvl1, make_lvl2, make_lvl3, make_lvl4, make_lvl5, make_lvl6]
level_num = 1

pygame.mixer.music.load(track)
pygame.mixer.music.play(-1)

while running:
    if game:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if not m_pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    pos = ((pos[0] / PPM) + TRANS[0],
                            (VIEW[1] - pos[1]) / PPM + TRANS[1])
                    if in_sling is not None:
                        if in_sling.fix.TestPoint(pos):
                            clicked = True
                    if pause_button.isClicked():
                        m_pause = True
                    elif rewind_button.isClicked():
                        for item in level.hogs + level.logs + level.birds:
                            if item in level.birds:
                                world.DestroyBody(item.body)
                                item.body = None
                            else:
                                if not item.dead:
                                    world.DestroyBody(item.body)
                                    item.body = None
                        world.DestroyBody(level.ground.body)
                        in_sling = None
                        TRANS = 0, 0
                        time_shot = -1000
                        pan_back = False
                        pan_to = False
                        level = level = levels[level_num-1]()

                elif event.type == pygame.MOUSEBUTTONUP and clicked:
                    clicked = False
                    in_sling.launch(screen, slingshot, TRANS)
                    in_sling.shot = True
                    last_shot = in_sling
                    in_sling = None
                    time_shot = pygame.time.get_ticks()
                    pan_to = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        if last_shot.use_ability:
                            if last_shot.tag == "redwing" and last_shot.use_ability:
                                last_shot.body.ApplyLinearImpulse(
                                            (last_shot.body.linearVelocity[0]*1.25,
                                            last_shot.body.linearVelocity[1]*1.25),
                                            last_shot.body.position, True)
                            elif last_shot.tag == "gold" and last_shot.use_ability:
                                birda = Bird((last_shot.body.position[0],
                                            last_shot.body.position[1]+.1), 0, "gold")
                                birda.body.linearVelocity = last_shot.body.linearVelocity[0],last_shot.body.linearVelocity[1]+3
                                level.birds.append(birda)
                                birda.shot = True
                                birdb = Bird((last_shot.body.position[0],
                                            last_shot.body.position[1]-.1), 0, "gold")
                                birdb.body.linearVelocity = last_shot.body.linearVelocity[0],last_shot.body.linearVelocity[1]-3
                                level.birds.append(birdb)
                                birdb.shot = True
                            pygame.mixer.Sound.play(chirp)
                            last_shot.use_ability = False


            elif m_pause:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if unpause.isClicked():
                        m_pause = False
                    elif (quit_from_pause.isClicked()
                        or pause_level_select.isClicked()):
                        game = False
                        m_pause = False
                        for item in level.hogs + level.logs + level.birds:
                            if item in level.birds:
                                world.DestroyBody(item.body)
                                item.body = None
                            else:
                                if not item.dead:
                                    world.DestroyBody(item.body)
                                    item.body = None
                        pan_to = False
                        pan_back = False
                        world.DestroyBody(level.ground.body)
                        in_sling = None
                        TRANS = 0, 0
                        if quit_from_pause.isClicked():
                            m_main = True
                        else:
                            m_level_select = True


        if not m_pause and not m_main and not m_level_select:
            for bird in level.birds:
                if not bird.shot:
                    bird.body.awake = False
            if in_sling == None:
                birds_not_shot = 0
                for bird in level.birds:
                    if not bird.shot:
                        birds_not_shot += 1
                if (birds_not_shot > 0 and
                    pygame.time.get_ticks() - time_shot >= 1000):
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
                in_sling.body.awake = False
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
            if hogs_down == level.num_hogs and level_num<len(levels):
                for item in level.hogs + level.logs + level.birds:
                    if item in level.birds:
                        world.DestroyBody(item.body)
                        item.body = None
                    else:
                        if not item.dead:
                            world.DestroyBody(item.body)
                            item.body = None
                world.DestroyBody(level.ground.body)
                in_sling = None
                TRANS = 0, 0
                pan_to = False
                pan_back = False
                m_pause = False
                level = levels[level_num]()
                select_level_nums[level_num].unlocked = True
                level_num += 1



        if art and not m_main and not m_level_select:
            screen.fill(SKY)
            screen.blit(level.background, (-1 * TRANS[0] * PPM, TRANS[1] * PPM))
            level.ground.draw(TRANS)
            slingshot.draw(TRANS)
            draw_sling(SLING_COLOR, slingshot, TRANS)
            if draw_anyways:
                level.ground.draw_shape(TRANS)
                for log in level.logs:
                    if not log.dead:
                        log.draw_shape(TRANS)
                for bird in level.birds:
                    bird.draw_shape(TRANS)
                for hog in level.hogs:
                    if not hog.dead:
                        hog.draw_shape(TRANS)
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
            if not m_pause:
                show_text(str(hogs_down) +
                        "/" + str(level.num_hogs), 720, 100, THEME, 40)
                for each in level_buttons:
                    each.draw()
                if clicked:
                    posa = in_sling.body.position
                    posb = slingshot.rect.centerx,slingshot.rect.y
                    posb = (posb[0]/PPM), (VIEW[1]-posb[1])/PPM
                    length = (((posb[0]-posa[0])**2+
                        (posb[1]-posa[1])**2)**(1/2))
                    reduct = 8
                    vector = ((posb[0]-posa[0])*reduct,
                        (posb[1]-posa[1])*reduct)
                    radius = 8
                    for i in range(6):
                        y_vec = vector[1]-(10/60)*i
                        posa = posa[0]+vector[0]/8, posa[1]+y_vec/8
                        draw_pos = int(posa[0]*PPM), int(VIEW[1]-(posa[1]*PPM))
                        pygame.draw.circle(screen,WHITE,draw_pos,radius)
                        radius-=1


            else:
                pygame.draw.rect(screen,WHITE,(420,200,600,500))
                pygame.draw.rect(screen,THEME,(430,210,580,480),5)
                show_text("paused",720,346,THEME,80)
                for each in pause_buttons:
                    each.draw()
                show_text(str(hogs_down) +
                        "/" + str(level.num_hogs), 940, 260, THEME, 40)


        elif not art and not m_main and not m_level_select:
            screen.fill(BLACK)
            level.ground.draw_shape(TRANS)
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isClicked():
                    m_main = False
                    level = levels[level_num-1]()
                    time_shot = -1000
                    game = True
                elif main_level_select.isClicked():
                    m_main = False
                    m_level_select = True

        screen.blit(background_art, (0,0))
        show_text("anger birbs!", 725, 255, WHITE, 140)
        show_text("anger birbs!", 720, 255, THEME, 140)
        show_text("an angry birds clone by caroline hohner", 840, 320, THEME, 30)
        for each in main_buttons:
            each.draw()
    elif m_level_select:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_from_select.isClicked():
                    m_level_select = False
                    m_main = True
                for i in range(len(select_level_nums)):
                    if (select_level_nums[i].isClicked()
                        and select_level_nums[i].unlocked):
                        m_level_select = False
                        level = levels[i]()
                        level_num = i+1
                        time_shot = -1000
                        game = True

        screen.blit(background_art, (0,0))
        pygame.draw.rect(screen,WHITE,(420,200,600,500))
        pygame.draw.rect(screen,THEME,(430,210,580,480),5)
        pygame.draw.rect(screen,SKY,(450,330,540,340))

        show_text("level select",720,280,THEME,70)
        for each in select_buttons:
            each.draw()


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
