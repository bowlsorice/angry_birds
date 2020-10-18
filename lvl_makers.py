from anger_common import *
from anger_sprites import *

def make_logs(info_list,base):
    logs = []
    for each in info_list:
        a_log = Log((each[0][0]+base,each[0][1]),
                each[1], each[2],each[3])
        logs.append(a_log)
    return logs

def make_hogs(info_list,base):
    hogs = []
    for info in info_list:
        a_hog = Hog((info[0][0] + base, info[0][1]), info[1])
        hogs.append(a_hog)
    return hogs

def make_lvl1():
    base = 12

    birds = []
    basic = Bird(basic_art, (1.5, .5), 0)
    birds.append(basic)
    redwing = Bird(redwing_art, (.5, .5), 0)
    birds.append(redwing)
    bluebird = Bird(bluebird_art, (1, .5), 0)
    birds.append(bluebird)

    hog_infos = [((0.08, 1.90), 0),
                ((-0.09, 4.21), 0)]

    hogs = make_hogs(hog_infos, base)

    log_infos = [((-0.32, 0.97),89.97735359718448, 0, False),
                ((-1.30, 1.31),-90.01380631678484, 1, False),
                ((0.49, 0.97),-89.98704563561672, 0, True),
                ((1.47, 1.31),-90.00098605171272, 1, True),
                ((0.05, 3.89),0.006770065662781008, 2, True),
                ((0.18, 1.58),-0.009420229086545365, 1, True),
                ((-1.28, 2.93),-90.02471412888934, 1, True),
                ((1.47, 2.93),-89.99938095725777, 1, False),
                ((0.59, 4.51),-89.99241416430435, 0, False),
                ((-0.56, 4.51),-89.90651770530228, 0, False),
                ((0.034, 5.13),0.20055960705519169, 2, False),
                ((1.34, 5.76),0.06462598260640023, 0, True),
                ((1.03, 5.44),0.14901609141179634, 0, True),
                ((-0.86, 5.44),0.23745059268055208, 0, True),
                ((-1.29, 5.75),0.8919172645582945, 0, True)]

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

    hog_infos = [((0.01, 0.67), 0),
                ((-0.46, 2.81), 0),
                ((0.40, 2.81), 0),
                ((-0.03, 5.06), 0)]
    hogs = make_hogs(hog_infos, base)

    log_infos = [((1.41, 0.96),-90.00384107078578, 0, False),
                ((0.72, 0.96),-90.01213975062736, 0, False),
                ((-1.45, 0.96), -90.00856756169144, 0, False),
                ((-0.74, 0.96),-90.02002861911872, 0, False),
                ((-0.04, 1.58),-0.001005131809696484, 2, True),
                ((0.37, 2.19),-90.00451042932445, 0, True),
                ((-0.47, 2.19),-90.00133439136039, 0, True),
                ((1.08, 2.54),-90.057000433096, 1, False),
                ((-1.09, 2.54),-90.04256824337976, 1, False),
                ((-0.08, 3.51),-0.004584619405551961, 2, False),
                ((-0.38, 4.12),-90.0223577136257, 0, True),
                ((0.47, 4.12),-90.01473522251196, 0, True),
                ((0.03, 4.74),-0.008166938565884367, 1, False)]

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

    log_infos = [((-1.5, 1.0), 90, 0, True), ((1.5, 1.0), 90, 0, True),
                ((0, 1.0), 90, 0, True), ((0, 1.5), 0, 2, False),
                ((-.25, 2.0), 90, 0, False), ((.25, 2.0), 90, 0, False),
                ((0, 2.5), 0, 1, False)]
    logs = make_logs(log_infos,base)

    lvl3 = Level(logs, base, hogs, birds)
    return lvl3

def make_lvl4():
    base = 12

    birds = []
    basic = Bird(basic_art, (1.5, .5), 0)
    birds.append(basic)
    redwing = Bird(redwing_art, (.5, .5), 0)
    birds.append(redwing)
    bluebird = Bird(bluebird_art, (1, .5), 0)
    birds.append(bluebird)

    hog_infos = [((-1.12, 2.8, 2), 0)]
    hogs = make_hogs(hog_infos, base)

    log_infos = [((1.08, 2.93), 90.06857077355, 1, True),
                ((-1.06, 1.32), -90.07252545307944, 1, True),
                ((-1.12, 2.28), -0.0626278921400138, 1, True),
                ((1.09, 1.31), -90.03883212990377, 1, True)]
    logs = make_logs(log_infos,base)

    lvl4 = Level(logs, base, hogs, birds)
    return lvl4
