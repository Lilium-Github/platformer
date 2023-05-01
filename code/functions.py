import random
from platformTypes import *

def platsmaker():
    allPlats = list()

    plats = list()
    for i in range(0,40,2):
        val = random.randrange(1, 40) + (20*i)
        plats.append(BasePlatform(random.randrange(-1600, 2400), val))
    allPlats.append(plats)

    clouds = list()
    for i in range(0,40,2):
        val = random.randrange(1, 40) + (20*i)
        clouds.append(Cloud(random.randrange(-1600, 2400), val))
    allPlats.append(clouds)

    ices = list()
    for i in range(0,40,2):
        val = random.randrange(1, 40) + (20*i)
        ices.append(Ice(random.randrange(-1600, 2400), val))
    allPlats.append(ices)

    return allPlats