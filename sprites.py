# Sprite classes for platform game
import pygame as pg
from settings import *
import time

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)

        self.game = game
        touche_platform = 1
        self.image = pg.image.load("perso.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (300, HEIGHT / 2)
        self.pos = vec(300, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.stopped_by_wall = False
        self.jumping = False
        self.ground = True

    def jump(self):
        # jump only if standing on a platform
        #       self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        #        self.rect.x -= 1

        # print(self.vel.y, self.vel.x)
        if hits:
            self.vel.y = -20

    def update(self):

        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        keys = pg.key.get_pressed()
        if self.pos.y == GROUND_y:
            self.ground = True
        keys = pg.key.get_pressed()

        ##        if self.ground and keys[pg.K_RIGHT] and not keys[pg.K_UP]:
        ##                        self.pos.x = hits[0].rect.left
        #        if hits and pg.sprite.collide_rect(self.pos.x,hits[0].rect.left) :
        #           if self.rect.right >= hits[0].rect.left:
        #                print('yayy')
        if self.vel.y == 0 and self.ground and keys[pg.K_LEFT]:
            self.pos.y = GROUND_y
            print('yo')
            if keys[pg.K_LEFT]:
                self.vel(0, 0)
        #                       print('miauuu')
        elif self.vel.y > 0 and hits:
            self.pos.y = hits[0].rect.top
            self.vel.y = 0
            self.ground = True

        self.acc = vec(0, PLAYER_GRAV)
        ##        keys = pg.key.get_pressed()
        ##        if keys[pg.K_LEFT]:
        ##            self.acc.x = -PLAYER_ACC
        ##        if keys[pg.K_RIGHT]:
        ##            self.acc.x = PLAYER_ACC
        ##
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        ##        if self.pos.y > 540:
        ##            self.pos.y = 540

        self.rect.midbottom = self.pos


class MovesWithKeys(pg.sprite.Sprite):
    can_move_left = True
    can_move_right = True

    def process_player_movement(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and MovesWithKeys.can_move_left:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_RIGHT] and MovesWithKeys.can_move_right:
            self.acc.x = -PLAYER_ACC


class Enemy(MovesWithKeys):

    def __init__(self, game, x, y):

        self.groups = game.all_sprites, game.enemy1_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pg.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y)
        self.rect.x = x
        self.rect.y = y
        self.time1 = time.time()
        # print(self.time1)

        self.counter = 1

    def update(self):

        self.acc = vec(0, 0)

        self.process_player_movement()

        if self.counter:
            self.acc.x -= ENEMY_ACC

        if time.time() > self.time1 + 3 and self.counter:
            self.time1 = time.time()
            self.counter = 0

        if self.counter == 0:
            self.acc.x += ENEMY_ACC

        if time.time() > self.time1 + 3 and self.counter == 0:
            self.time1 = time.time()
            self.counter = 1

            # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos


class Enemy2(MovesWithKeys):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemy1_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pg.image.load("enemy2.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y)
        self.counter = 1
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.acc = vec(0, 0)
        self.process_player_movement()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos


class Background(MovesWithKeys):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load("background.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH, HEIGHT)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        self.process_player_movement()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


class Cloud(MovesWithKeys):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load("cloud.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    ##    def jump(self):
    ##        # jump only if standing on a platform
    ##        self.rect.x += 1
    ##        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
    ##        self.rect.x -= 1
    ##        if hits:
    ##            self.vel.y = -20

    def update(self):
        self.acc = vec(0, 0)
        self.process_player_movement()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


class Platform(MovesWithKeys):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        #       self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(x, y)

    def update(self):
        self.acc = vec(0, 0)
        self.process_player_movement()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos


class Coin(MovesWithKeys):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("coin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = ((WIDTH / 2) - 100, 0)
        self.pos = vec((WIDTH / 2) - 100, 0)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y)

    #       self.rect.center = (WIDTH / 2, HEIGHT / 2)

    ##    def stop(self):
    ##            self.vel = vec(0, 0)
    ##            self.acc = vec(0, 0)
    ##            print('miau')

    def update(self):

        ##        keys = pg.key.get_pressed()
        keys = pg.key.get_pressed()
        self.acc = vec(0, 0)
        self.process_player_movement()
        if keys[pg.K_DOWN]:
            self.acc.y = PLAYER_GRAV
        #           print('miau')

        ## hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        #        self.rect.x -= 1

        # print(self.vel.y, self.vel.x)
        ##        hits_cp = pg.sprite.groupcollide(self.game.platforms, self, False, False)
        ##        if hits_cp:
        ##            print('miau')
        if self.pos.y > GROUND_y - 30:  # or hits_cp: #hits or
            self.vel.y = 0
            self.acc.y = 0
        #           print('hi')

        ##        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        ##        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos


#       print(self.pos)


class Fireball(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("fireball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = ((WIDTH / 2) - 100, 0)
        self.pos = vec((WIDTH / 2) - 100, 0)
        self.vel = vec(80, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y)
        self.acc = vec(0, PLAYER_GRAV)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)

        ##        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        ##        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos


#       print(self.pos)


class Enemy_fire(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load("fireball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(100, 100)
        self.vel = vec(80, 0)
        self.acc = vec(0, 0)
        self.pos = vec(100, 100)
        self.acc = vec(0, PLAYER_GRAV)
        self.velocity0 = 0

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)

        ##        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        ##        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.velocity0 = self.vel
##        keys = pg.key.get_pressed()
##        if keys:
##          if keys[pg.K_RIGHT]:
##            self.vel = vec(0,0)
##            self.acc.x = -PLAYER_ACC
##            
##          if keys[pg.K_LEFT]:
##            self.acc.x = PLAYER_ACC
##        else:
##            self.vel = self.velocity0
##            self.rect.midbottom = self.pos
#       print(self.pos)
