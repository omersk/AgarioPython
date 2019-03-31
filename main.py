"""
name: Agario
creator: Omer Sasoni
verison: 10.0
project type: final project
to: ori and dana
"""
from sprites import *
import datetime
import math
import sys
import socket
players_socket = socket.socket()
players_socket.connect(('127.0.0.1', 25))


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.arr = []
        self.counter_x = 0
        self.counter_y = 0

    def new(self):
        # start a new game
        players_socket.send("hello")
        players_socket.recv(1024)
        self.all_sprites = pg.sprite.Group()
        self.all_viruses = pg.sprite.Group()
        self.all_ext_players = pg.sprite.Group()  #
        self.player = Player(RED)
        self.ext_player1 = Online(self.player, BLUE)  #
        self.all_ext_players.add(self.ext_player1)  #
        self.all_sprites.add(self.player)
        self.viruses = list()
        self.virusecounter = 0
        for i in range(NUMBER_VIRUSES):
            self.viruses.append(Viruses(self.player, self.virusecounter,
                                        self.counter_x, self.counter_y))
            self.virusecounter += 1
            self.all_viruses.add(self.viruses[i])
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        players_socket.send("hi")
        data = players_socket.recv(1024)
        if self.player.colour == EMPTY_COLOUR:
            sys.exit("U lost")
        elif data == "no":
            self.playing = False
        else:
            self.all_sprites.update()
            self.all_ext_players.update(self.player)
            for virus in self.viruses:
                if virus.colour == EMPTY_COLOUR:
                    self.all_viruses.remove(virus)
                    self.viruses.remove(virus)
            for online_player in self.all_ext_players:
                if online_player.colour == EMPTY_COLOUR:
                    self.all_ext_players.remove(online_player)
                    self.all_ext_players.remove(online_player)
            for player in self.all_sprites:
                if player.colour == EMPTY_COLOUR:
                    self.playing = False
                    self.running = False
            for player in self.all_ext_players:
                if player.colour == EMPTY_COLOUR:
                    self.all_ext_players.remove(player)
            now = datetime.datetime.now()
            if TIME_WAITING >= 1:
                if now.second % TIME_WAITING == 0 and \
                        now.second not in self.arr and \
                        len(self.all_viruses) < MAX_VIRUSES:
                    self.viruses.append(Viruses(self.player,
                                                self.virusecounter,
                                                self.counter_x,
                                                self.counter_y))
                    self.virusecounter += 1
                    self.all_viruses.add(self.viruses[len(self.viruses)-1])
                    self.arr.append(now.second)
            else:
                if now.second not in self.arr and \
                                len(self.all_viruses) < MAX_VIRUSES:
                    for i in range(0, int(1/TIME_WAITING)):
                        self.viruses.append(Viruses(self.player,
                                                    self.virusecounter,
                                                    self.counter_x,
                                                    self.counter_y))
                        self.virusecounter += 1
                        self.all_viruses.add(self.viruses[len(self.viruses)-1])
                        self.arr.append(now.second)

            if len(self.arr) == math.floor(60/TIME_WAITING):
                self.arr = []
            if self.player.top <= HEIGHT/10:
                self.counter_y += abs(self.player.vel.y)
                self.player.rect.y += abs(self.player.vel.y)
                for virus in self.all_viruses:
                    virus.rect.y += abs(self.player.vel.y)
                for online_player in self.all_ext_players:
                    online_player.rect.y += abs(self.player.vel.y)
            mergedlist = [self.player]
            for player in self.all_ext_players:
                mergedlist.extend([player])
            self.all_viruses.update(mergedlist)
            if self.player.bot >= 0.9 * HEIGHT:
                self.counter_y -= abs(self.player.vel.y)
                self.player.rect.y -= abs(self.player.vel.y)
                for online_player in self.all_ext_players:
                    online_player.rect.y -= abs(self.player.vel.y)
                for virus in self.all_viruses:
                    virus.rect.y -= abs(self.player.vel.y)
            if self.player.left >= 0.8 * WIDTH:
                self.counter_x -= abs(self.player.vel.x)
                for online_player in self.all_ext_players:
                    online_player.rect.x -= abs(self.player.vel.x)
                self.player.rect.x -= abs(self.player.vel.x)
                for virus in self.all_viruses:
                    virus.rect.x -= abs(self.player.vel.x)
            if self.player.right <= 0.2 * WIDTH:
                self.counter_x += abs(self.player.vel.x)
                for online_player in self.all_ext_players:
                    online_player.rect.x += abs(self.player.vel.x)
                self.player.rect.x += abs(self.player.vel.x)
                for virus in self.all_viruses:
                    virus.rect.x += abs(self.player.vel.x)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.all_ext_players.draw(self.screen)
        self.all_viruses.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
