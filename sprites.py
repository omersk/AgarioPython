import pygame as pg
from settings import *
import random
import socket
my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 23))
my_virus_socket = socket.socket()
my_virus_socket.connect(('127.0.0.1', 24))
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, colour):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((RADIUS_X, RADIUS_Y))
        self.current_radius_x = RADIUS_X
        self.current_radius_y = RADIUS_Y
        self.colour = colour
        self.score = 0
        self.image.fill(colour)
        self.start_x = WIDTH/2
        self.start_y = HEIGHT/2
        self.rect = vec(WIDTH/2, HEIGHT/2)
        self.top = self.rect.y - self.current_radius_y/2
        self.bot = self.rect.y + self.current_radius_y/2
        self.left = self.rect.x - self.current_radius_x/2
        self.right = self.rect.x + self.current_radius_x/2
        self.vel = vec(0.0, 0.0)
        self.acc = vec(0.0, 0.0)
        self.real_rect = vec(random.randint(-2*WIDTH, 2*WIDTH),
                             random.randint(-2*HEIGHT, 2*HEIGHT))

    def update(self):
        print self.real_rect
        self.acc.x = 0
        self.acc.y = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_DOWN]:
            self.acc.y = PLAYER_ACC
        if keys[pg.K_UP]:
            self.acc.y = -PLAYER_ACC
        # apply friction

        self.acc.x += self.vel.x*PLAYER_FRICTION
        self.acc.y += self.vel.y*PLAYER_FRICTION
        self.vel.x += self.acc.x
        self.vel.y += self.acc.y
        if self.vel.y + 0.5 * self.acc.y <= 0 or self.real_rect.y < 2*HEIGHT:
            if self.vel.y + 0.5 * self.acc.y >= 0 or\
                            self.real_rect.y > -2*HEIGHT:
                self.rect.y += self.vel.y + 0.5 * self.acc.y
                self.real_rect.y += self.vel.y + 0.5*self.acc.y
        if self.vel.x + 0.5 * self.acc.x <= 0 or self.real_rect.x < 2*WIDTH:
            if self.vel.x + 0.5 * self.acc.x >= 0 or\
                            self.real_rect.x > -2*WIDTH:
                self.rect.x += self.vel.x + 0.5 * self.acc.x
                self.real_rect.x += self.vel.x + 0.5*self.acc.x
            self.top = self.rect.y - self.current_radius_y/2
            self.bot = self.rect.y + self.current_radius_y/2
            self.left = self.rect.x - self.current_radius_x/2
            self.right = self.rect.x + self.current_radius_x/2
            self.real_top = self.real_rect.y - self.current_radius_y/2
            self.real_bot = self.real_rect.y + self.current_radius_y/2
            self.real_left = self.real_rect.x - self.current_radius_x/2
            self.real_right = self.real_rect.x + self.current_radius_x/2


class Online(pg.sprite.Sprite):

    def __init__(self, player, colour):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((RADIUS_X, RADIUS_Y))
        self.colour = colour
        self.image.fill(self.colour)
        self.current_radius_x = RADIUS_X
        self.current_radius_y = RADIUS_Y
        self.start_x = random.randint(-2*WIDTH, 2*WIDTH)
        self.start_y = random.randint(-2*HEIGHT, 2*HEIGHT)
        self.rect = vec(self.start_x, self.start_y)
        self.real_rect = vec(self.start_x + player.real_rect.x - player.rect.x,
                             self.start_y + player.real_rect.y - player.rect.y)
        self.pos = vec(self.rect.x - VIRUSES_RADIUS_X/2,
                       self.rect.y - VIRUSES_RADIUS_Y/2)
        self.score = 0

    def update(self, player):
        my_socket.send(str(player.real_rect.x) + "," + str(player.real_rect.y))
        data = my_socket.recv(1024)
        self.rect.x += float(data.split(',')[0])-self.real_rect.x
        self.rect.y += float(data.split(',')[1])-self.real_rect.y
        self.real_rect.x = float(data.split(',')[0])
        self.real_rect.y = float(data.split(',')[1])
        self.real_top = self.real_rect.y - self.current_radius_y/2
        self.real_bot = self.real_rect.y + self.current_radius_y/2
        self.real_left = self.real_rect.x - self.current_radius_x/2
        self.real_right = self.real_rect.x + self.current_radius_x/2
        self.top = self.rect.y - self.current_radius_y/2
        self.bot = self.rect.y + self.current_radius_y/2
        self.left = self.rect.x - self.current_radius_x/2
        self.right = self.rect.x + self.current_radius_x/2
        if player.real_left <= self.real_rect.x <= player.real_right:
            if player.real_bot >= self.real_rect.y >= player.real_top:
                if player.current_radius_x > self.current_radius_x:
                    self.image = pg.Surface(EMPTY_SURFACE)
                    self.colour = EMPTY_COLOUR
                    colour = player.colour
                    player.current_radius_x += self.current_radius_x
                    player.current_radius_y += self.current_radius_y
                    player.image = pg.Surface((player.current_radius_x,
                                               player.current_radius_y))
                    player.image.fill(colour)
                    player.score += self.score
        if self.real_left <= player.real_rect.x <= self.real_right:
            if self.real_bot >= player.real_rect.y >= self.real_top:
                if self.current_radius_x > player.current_radius_x:
                    player.image = pg.Surface(EMPTY_SURFACE)
                    player.colour = EMPTY_COLOUR
                    colour = self.colour
                    self.current_radius_x += player.current_radius_x
                    self.current_radius_y += player.current_radius_y
                    self.image = pg.Surface((self.current_radius_x,
                                             self.current_radius_y))
                    self.image.fill(colour)
                    self.score += player.score


class Viruses(pg.sprite.Sprite):
    def __init__(self, player, counter, passed_x, passed_y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((VIRUSES_RADIUS_X, VIRUSES_RADIUS_Y))
        self.colour = VIRUSES_COLOR_ARRAY[random.randint(0, 3)]
        self.image.fill(self.colour)
        my_virus_socket.send(str(counter))
        data = my_virus_socket.recv(1024)
        self.counter = counter
        self.start_x = float(data.split(",")[0])
        self.start_y = float(data.split(",")[1])
        self.real_rect = vec(self.start_x, self.start_y)
        self.rect = vec(self.start_x + player.rect.x - player.real_rect.x,
                        self.start_y + player.rect.y - player.real_rect.y)
        self.pos = vec(self.real_rect.x - VIRUSES_RADIUS_X/2,
                       self.real_rect.y - VIRUSES_RADIUS_Y/2)

    def update(self, players):
        for player in players:
            if player.real_left <= self.real_rect.x <= player.real_right:
                if player.real_bot >= self.real_rect.y >= player.real_top:
                    self.image = pg.Surface(EMPTY_SURFACE)
                    self.colour = EMPTY_COLOUR
                    colour = player.colour
                    player.current_radius_x += RADIUS_X_ADDING
                    player.current_radius_y += RADIUS_Y_ADDING
                    player.image = pg.Surface((player.current_radius_x,
                                               player.current_radius_y))
                    player.image.fill(colour)
                    player.score += 1
