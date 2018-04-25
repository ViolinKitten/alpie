import random

# game options/settings
TITLE = "Alpie!"
WIDTH = 1200
HEIGHT = 600
FPS = 60

# Player properties
PLAYER_ACC = 0.5
ENEMY_ACC = 0.3
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8

# coordinate ground
GROUND_y = 540

# Starting platforms
# width = random.randrange(50, 100)
PLATFORM_LIST = [(0, 540),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4)]

for i in range(1000, 10000, 400):
    PLATFORM_LIST.append((500 + random.randrange(i, i + 100), random.randrange(250, 400)))

ENEMY2_LIST = []

##print(ENEMY2_LIST) 
##ENEMY2_LIST.append((1531, 168))   #PLATFORM_LIST[random.randrange(0,len(PLATFORM_LIST)/2)]
##print(ENEMY2_LIST) 
##ENEMY2_LIST.append((2356, 394))   #PLATFORM_LIST[random.randrange(len(PLATFORM_LIST)/2, len(PLATFORM_LIST))]
##print(ENEMY2_LIST)                  

nb1 = []
nb1 = PLATFORM_LIST[4]
#print(nb1)
ENEMY2_LIST.append((nb1[0], nb1[1] - 20))
#print(ENEMY2_LIST)
nb1 = PLATFORM_LIST[6]
ENEMY2_LIST.append((nb1[0], nb1[1] - 20))

FIRE_E = []
nb2 = []
nb2 = ENEMY2_LIST[0]
FIRE_E.append(nb2[0])
FIRE_E.append(nb2[1])
nb2 = ENEMY2_LIST[1]
FIRE_E.append(nb2[0])
FIRE_E.append(nb2[1])
#print(FIRE_E)

PLATFORM2_LIST = []
for m in range(500, 10000, 1000):
    # platforms on bottom beyond the very first one
    PLATFORM2_LIST.append((500 + m, GROUND_y))
  

COIN_LIST = []
for n in range(1000, 10000, 200):
    COIN_LIST.append((500 + random.randrange(n, n + 900), 0))

ENEMY_LIST = []
for m in range(500, 10000, 1000):
    ENEMY_LIST.append((500 + random.randrange(m, m + 100) + 600, GROUND_y))

nb = []
LIST_LIST = []
for l in range(10):
    nb = PLATFORM2_LIST[l]
    LIST_LIST.append((nb[0] + 1))
    nb = []
#print(LIST_LIST)

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (143, 217, 254)
YELLOW = (255, 255, 0)
BGCOLOR = (0, 155, 155)
BACKG = (200, 155, 200)
