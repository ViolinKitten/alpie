import pygame as pg
import random
from settings import *
from sprites import *
import time


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.jumping = False

        self.hit = 1

        self.score = 0
        # I put a random comment in which is super-precious to me and I want to save it for 100 years!!!
        self.time1 = time.time()
        # start a new game
        self.all_sprites = pg.sprite.Group()

        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.fireball_group = pg.sprite.Group()
        self.enemy_fire = pg.sprite.Group()
        self.enemy1_group = pg.sprite.Group()
        self.enemy2_group = pg.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        for plat in PLATFORM_LIST:
            #           print(plat)
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        for coin in COIN_LIST:
            c = Coin(*coin)
            self.all_sprites.add(c)
            self.coins.add(c)

        for enemy in ENEMY_LIST:
            #           print('hi')
            e = Enemy(self, *enemy)
            self.all_sprites.add(e)
            self.enemy1_group.add(e)

        for enemy2 in ENEMY2_LIST:
            #           print('hi')
            e2 = Enemy2(self, *enemy2)
            self.all_sprites.add(e2)
            self.enemy2_group.add(e2)

    def run(self):
        # Game Loop
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def show_start_screen(self):
        start_screen = pg.image.load("startscreen.jpg")  # loads start screen
        self.screen.blit(start_screen, (0, 0))  # blits/prints start screen image
        pg.display.update()
        self.wait_for_key()

    #        self.music()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False  # if player quits game ends
                if event.type == pg.KEYUP:  # if player hits key game starts
                    waiting = False

    def music(self):
        ##        pg.mixer.music.play(5)                  #plays track (Kirby's Dream Course - Credits) six times
        ##        pg.mixer.music.queue('track.ogg')
        sound1 = pg.mixer.Sound('track.ogg')
        sound1.play()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # check if player hits a platform - only if falling
        keys = pg.key.get_pressed()

        colliding_platforms = pg.sprite.spritecollide(self.player, self.platforms, False)
        if len(colliding_platforms) > 1:
            platform = colliding_platforms[1]
            delta_y = platform.pos.y - self.player.pos.y
            delta_x = platform.pos.x - self.player.pos.x
            if abs(delta_x) > abs(delta_y):
                if delta_x > 0:
                    # CASE 1 -- bump from left (platform on right)
                    MovesWithKeys.can_move_right = False
                else:
                    # CASE 2 -- bump from right (platform on left)
                    MovesWithKeys.can_move_left = False
        else:
            MovesWithKeys.can_move_right = True
            MovesWithKeys.can_move_left = True

        # player eats coins:
        if pg.sprite.spritecollide(self.player, self.coins, True, False):
            self.score += 100
            print(self.score)
            pg.mixer.music.load('coin.ogg')
            sound2 = pg.mixer.Sound('coin.ogg')
            sound2.play()

        # player eats coins:
        if pg.sprite.spritecollide(self.player, self.coins, True, False):
            self.score += 1
            print(self.score)
        # enemy eats player
        # if pg.sprite.collide_rect(self.player, self.enemy):
        #            self.all_sprites.remove(self.player)
        # page de fin

        # fireball eats enemy
        pg.sprite.groupcollide(self.enemy1_group, self.fireball_group, True, True)

        # objects eat fireball
        pg.sprite.groupcollide(self.fireball_group, self.platforms, True, False)
        pg.sprite.groupcollide(self.enemy_fire, self.platforms, True, False)
        #       if self.fireball.pos.y>GROUND_y:
        #            self.all_sprites.remove(self.fireball)

        # platform and fireball collide
        ##        if pg.sprite.groupcollide(self.coins, self.platforms, False, False):
        ##            Coin.stop(self)

        # enemy hits platform
        ##        if pg.sprite.spritecollide(self.enemy, self.platforms,False):
        ##
        ##            Enemy.move(self)

        ##        if self.fireball.pos.y>GROUND_y:
        ##            self.fireball.remove(self.fireball)
        ##            self.all_sprites.remove(self.fireball)

        #       print(self.player.pos.y)
        #       if self.player.pos.y > 530:
        #               self.touche_platform=False
        #               self.player.pos.y=GROUND_y

        #       if (keys[pg.K_LEFT] or keys[pg.K_RIGHT]) and self.player.pos.y==540:
        #
        #           self.player.pos.y=GROUND_y

        # hits = pg.sprite.spritecollide(self.player, self.platforms, False)

        if self.player.vel.y > 0:

            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            ##            if hits and self.player.rect.right == hits[0].rect.left+1:
            ##                self.player.pos.y=540
            ##                print('miau')
            if hits:
                pass
                # and self.touche_platform:
            #               print(self.player.rect.right, 'miau', hits[0].rect.left)
            # print(self.player.vel.y)
            ##                if self.player.pos.y > hits[0].rect.top:
            ##                    self.player.pos.y = hits[0].rect.top
            ##                    self.player.vel.y = 0
            ##                    print(self.player.pos.y, hits[0].rect.top)
            ##                else:
            ## #                   self.player.stopped_by_wall = True
            ##                    self.player.pos.x -= 20
            ##                    self.player.vel.x = 0
            ##                    self.player.acc.x = 0
            ##                    print('miau1')

            elif self.player.pos.y > GROUND_y:
                # and self.touche_platform:

                self.player.pos.y = GROUND_y
                self.player.vel.y = 0
        #               self.touche_platform=False

        for plat in PLATFORM_LIST:
            #               plat.rect.y += abs(self.player.vel.y)
            #               print(plat[3])
            if plat[3] >= WIDTH:
                print('miau')
                plat.kill()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                    self.jumping = False
                    self.ground = False
                if event.key == pg.K_SPACE:
                    f = Fireball(self.player.pos.x, self.player.pos.y - 50)
                    self.all_sprites.add(f)
                    self.fireball_group.add(f)
                    self.fireball_group.draw(self.screen)

    ##                    ef2 = Enemy_fire(100,100)
    ##                    self.all_sprites.add(ef2)
    ##                    self.enemy_fire.add(ef2)
    ##                    self.enemy_fire.draw(self.screen)

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.coins.draw(self.screen)
        imagebase = pg.draw.rect(self.screen, (GREEN), (0, 540, 1200, 60))

        ##        for x in range (len(ENEMY_LIST)):
        ##
        ##            e = Enemy(x, GROUND_y)
        ##            self.all_sprites.add(e)
        ##            self.enemy.add(e)
        ##            self.enemy.draw(self.screen)

        #       self.platforms.add(imagebase)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_go_screen(self):
        # game over/continue
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.run()
    g.show_go_screen()

pg.quit()
