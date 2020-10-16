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

    hog_infos = [((0.08013515472412092, 1.900923490524292), 0),
        ((-0.08775157928466815, 4.214478492736816), 0)]

    hogs = make_hogs(hog_infos, base)

    log_infos = [((-0.31868095397949237, 0.9659917950630188),
                89.97735359718448, 0, False),
                ((-1.296089839935303, 1.3149046897888184),
                -90.01380631678484, 1, False),
                ((0.4888985633850096, 0.9658260345458984),
                -89.98704563561672, 0, True),
                ((1.4662330627441404, 1.3149597644805908),
                -90.00098605171272, 1, True),
                ((0.050200271606445135, 3.8945581912994385),
                0.006770065662781008, 2, True),
                ((0.17996625900268537, 1.5809270143508911),
                -0.009420229086545365, 1, True),
                ((-1.2784058570861818, 2.9296600818634033),
                -90.02471412888934, 1, True),
                ((1.4740808486938475, 2.9298598766326904),
                -89.99938095725777, 1, False),
                ((0.5890486717224119, 4.509588718414307),
                -89.99241416430435, 0, False),
                ((-0.5587379455566408, 4.509151935577393),
                -89.90651770530228, 0, False),
                ((0.03372793197631818, 5.125909805297852),
                0.20055960705519169, 2, False),
                ((1.3810461044311522, 5.760431289672852),
                0.06462598260640023, 0, True),
                ((1.0306280136108397, 5.4445648193359375),
                 0.14901609141179634, 0, True),
                ((-0.8561241149902346, 5.437365531921387),
                0.23745059268055208, 0, True),
                ((-1.2927453041076662, 5.750103950500488),
                0.8919172645582945, 0, True)]

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

    hog_infos = [((0.010000038146972479, 0.67166668176651), 0),
                ((-0.4618160247802736, 2.814626693725586), 0),
                ((0.4011190414428709, 2.8146297931671143), 0),
                ((-0.02984352111816424, 5.05683708190918), 0)]
    hogs = make_hogs(hog_infos, base)

    log_infos = [((1.4099872589111326, 0.9646461606025696),
                -90.00384107078578, 0, False),
                ((0.7187912940979002, 0.9645808935165405),
                -90.01213975062736, 0, False),
                ((-1.4791728973388674, 0.9646880030632019),
                 -90.00856756169144, 0, False),
                ((-0.7401139259338381, 0.9645892381668091),
                -90.02002861911872, 0, False),
                ((-0.043508720397949396, 1.5789401531219482),
                -0.001005131809696484, 2, True),
                ((0.3716805458068846, 2.1946327686309814),
                -90.00451042932445, 0, True),
                ((-0.4698984146118166, 2.1946277618408203),
                -90.00133439136039, 0, True),
                ((1.0805147171020506, 2.5430972576141357),
                -90.057000433096, 1, False),
                ((-1.0895645141601564, 2.543255090713501),
                -90.04256824337976, 1, False),
                ((-0.07943220138549822, 3.5075857639312744),
                -0.004584619405551961, 2, False),
                ((-0.38391084671020526, 4.122201919555664),
                -90.0223577136257, 0, True),
                ((0.4703457832336424, 4.122075080871582),
                -90.01473522251196, 0, True),
                ((0.029939460754394354, 4.736793041229248),
                -0.008166938565884367, 1, False)]

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
