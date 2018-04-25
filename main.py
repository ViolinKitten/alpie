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
        self.font_name = pg.font.match_font('Oswald')

        self.hit = 1

        self.score = 0
        self.time1 = time.time()

    def text(self, surface, text, size, x, y):
        # points - coins
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect = (980, 30)
        self.screen.blit(text_surface, text_rect)

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()

        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.fireball_group = pg.sprite.Group()
        self.enemy_fire = pg.sprite.Group()
        self.enemy1_group = pg.sprite.Group()
        self.enemy2_group = pg.sprite.Group()

        self.panneau = Panneau(self)
        self.all_sprites.add(self.panneau)

        self.player = Player(self)
        self.all_sprites.add(self.player)

        # platform on the ground
        p_g = Platform(WIDTH * 4, HEIGHT, 0)
        self.all_sprites.add(p_g)
        self.platforms.add(p_g)

        for plat in PLATFORM_LIST:
            #           print(plat)
            p1 = Platform(*plat, 1)
            self.all_sprites.add(p1)
            self.platforms.add(p1)

        for plat in PLATFORM2_LIST:
            #           print(plat)
            p2 = Platform(*plat, 2)
            self.all_sprites.add(p2)
            self.platforms.add(p2)

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
        self.run()

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
                if event.type == pg.KEYDOWN:  # if player hits key game starts
                    if event.key == pg.K_RETURN:
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
                # print(platform.pos.y, self.player.pos.y)
                if delta_x > 0:
                    # CASE 1 -- bump from left (platform on right)
                    MovesWithKeys.can_move_right = False

                elif delta_x < 0:
                    # CASE 2 -- bump from right (platform on left)
                    MovesWithKeys.can_move_left = False

        elif len(colliding_platforms) == 1:
            # CASE 3 -- bump from underneath (platform above)
            platform = colliding_platforms[0]
            if platform.pos.y < self.player.pos.y:
                # print('hi')
                self.player.can_move_up = False
            else:
                self.player.can_move_up = True
            MovesWithKeys.can_move_right = True
            MovesWithKeys.can_move_left = True



        # player eats coins:
        if pg.sprite.spritecollide(self.player, self.coins, True, False):
            self.score += 10
            pg.mixer.music.load('coin.ogg')
            sound2 = pg.mixer.Sound('coin.ogg')
            sound2.play()

        # fireball eats enemy
        if pg.sprite.groupcollide(self.enemy1_group, self.fireball_group, True, True):
            self.score += 50

        # objects eat fireball
        pg.sprite.groupcollide(self.fireball_group, self.platforms, True, False)
        pg.sprite.groupcollide(self.enemy_fire, self.platforms, True, False)
        #       if self.fireball.pos.y>GROUND_y:
        #            self.all_sprites.remove(self.fireball)

        # enemy eats player
        if pg.sprite.spritecollide(self.player, self.enemy1_group, False, False):
            self.playing = False

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
                    #                  self.jumping = False
                    self.ground = False
                if event.key == pg.K_SPACE:
                    if self.player.left:
                        f = Fireball(self.player.pos.x, self.player.pos.y - 50, -80)
                    else:
                        f = Fireball(self.player.pos.x, self.player.pos.y - 50, 80)
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
        gameground = pg.draw.rect(self.screen, (GREEN), (0, 540, 1200, 60))
        self.text(self.screen, "Score: " + str(self.score), 60, 60, 10)

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
        if self.running:
            self.score = 0
            start_screen = pg.image.load("startscreen.jpg")  # loads start screen
            self.screen.blit(start_screen, (0, 0))  # blits/prints start screen image
            pg.display.update()
            self.wait_for_key()


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
