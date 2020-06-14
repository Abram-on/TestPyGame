from threading import Thread

import pygame
from pygame.sprite import Sprite
import random
from colors import Colors
import datetime
import time


class Turtle(Sprite):
    def __init__(self, x, y, surf: pygame.Surface, cl_surf, distance, finish_game, number: int):
        super(Turtle, self).__init__()
        self.image = surf
        self.image.fill(cl_surf)
        self.rect = self.image.get_rect()
        self.start_x = x
        self.start_y = y
        self.rect.x = x
        self.rect.y = y
        self.distance = distance
        self.finish_game = finish_game
        self.number = number
        self.font = pygame.font.SysFont('Arial black', 16, True)
        self.text = self.font.render(str(self.number), False, (10, 10, 10))
        self.image.blit(self.text, (13, 8))
        self.player_steps = []
        self.distance_player: int = 0
        self.cnt: int = 0

    def update(self):
        step: int = random.randint(1, 10)
        self.cnt += 1
        if (self.distance_player + step) > self.distance:
            step = (self.distance - self.distance_player)
        self.distance_player += step
        self.rect.x += step
        self.player_steps.append(step)
        if self.distance_player >= self.distance:
            self.finish_game()

    def set_start(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
# END class Turtle_______________________


class Game(Colors, Thread):
    stop_event_listener: bool = False
    stop_thread: bool = False
    SPRITE_WIDTH: int = 40
    SPRITE_HEIGHT: int = 40
    TOP_RANGE = 80
    BOTTOM_RANGE = 50
    LEFT_RANGE: int = 50
    RIGHT_RANGE: int = 60
    FPS: int
    GAME_START: bool = False
    BG_COLOR = (200, 255, 200)

    def __init__(self, full_screen: bool, players: int, fps: int):
        Thread.__init__(self)
        self.name = "Game"
        self.PLAYERS = players
        self.FPS = fps
        pygame.init()
        pygame.font.init()
        self.info = pygame.display.get_desktop_sizes()
        if full_screen:
            self.DISPLAY_WIDTH = self.info[0][0]
            self.DISPLAY_HEIGHT = self.info[0][1]
        else:
            self.DISPLAY_WIDTH = 1000
            self.DISPLAY_HEIGHT = 1000
        self.wn = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.wn_rect = self.wn.get_rect()
        pygame.display.set_caption("Turtle racing")
        self.caption_x: int = (self.DISPLAY_WIDTH // 2) - ((len("Turtle Racing") * 19) // 2)
        self.caption_y: int = 10
        self.FINISH_GAME = False
        self.LINE_START: int = self.LEFT_RANGE
        self.LINE_FINISH: int = self.DISPLAY_WIDTH - self.RIGHT_RANGE
        self.DISTANCE: int = self.LINE_FINISH - self.LINE_START
        self.pre_y = (self.DISPLAY_HEIGHT - self.TOP_RANGE - self.BOTTOM_RANGE) // self.PLAYERS
        self.pre_x = self.LINE_START - self.SPRITE_WIDTH
        self.group = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.wn.fill(self.BG_COLOR)
        self.font = pygame.font.SysFont('Arial black', 32, False)
        self.event_font = pygame.font.SysFont('Arial black', 18, False)
        self.surf_width: int = self.LINE_FINISH
        self.surf_height: int = self.DISPLAY_HEIGHT - self.BOTTOM_RANGE - self.TOP_RANGE - 2
        self.game_surf = pygame.Surface([self.surf_width, self.surf_height])
        self.game_rect = self.game_surf.get_rect()
        self.game_rect.x = 0
        self.game_rect.y = self.TOP_RANGE + 2
        self.game_surf.fill(self.BG_COLOR)

    def bg_screen_draw(self):
        self.wn.blit(self.game_surf, self.game_rect)
        # Старт
        pygame.draw.line(self.wn, self.RED, (self.LINE_START, self.TOP_RANGE), (self.LINE_START, self.DISPLAY_HEIGHT - self.BOTTOM_RANGE), 4)
        # Финиш
        pygame.draw.line(self.wn, self.RED, (self.LINE_FINISH, self.TOP_RANGE), (self.LINE_FINISH, self.DISPLAY_HEIGHT - self.BOTTOM_RANGE), 4)
        text = self.font.render('Turtle Racing', False, (255, 0, 0))
        self.wn.blit(text, (self.caption_x, self.caption_y))
        # Первая линия
        pygame.draw.line(self.wn, self.BLACK, (self.LINE_START + 4, self.TOP_RANGE), (self.LINE_FINISH - 4, self.TOP_RANGE), 2)
        # Дорожки
        for i in range(self.PLAYERS):
            pygame.draw.line(self.wn, self.BLACK,
                             (self.LINE_START + 4, (self.TOP_RANGE + (((self.DISPLAY_HEIGHT -
                                                              (self.TOP_RANGE + self.BOTTOM_RANGE))
                                                             // self.PLAYERS) * (i + 1)))),
                             (self.LINE_FINISH - 4, (self.TOP_RANGE + (((self.DISPLAY_HEIGHT -
                                                               (self.TOP_RANGE + self.BOTTOM_RANGE))
                                                              // self.PLAYERS) * (i + 1)))),
                             2)

    def on_start(self):
        self.FINISH_GAME = False
        if len(self.group.sprites()) > 0:
            for i in range(self.PLAYERS):
                self.group.sprites()[i].distance_player = 0
                self.group.sprites()[i].player_steps.clear()
                self.group.sprites()[i].set_start()

        else:
            for i in range(self.PLAYERS):
                surf = pygame.Surface([40, 40])
                t = Turtle(self.pre_x, (self.TOP_RANGE + (((self.pre_y // 2) - self.SPRITE_WIDTH // 2) + (self.pre_y * i))),
                           surf, self.get_random_color(), self.DISTANCE, self.finish_game, i + 1)
                self.group.add(t)
        self.group.draw(self.wn)
        pygame.display.update()

    def run_play(self):
        while not self.FINISH_GAME:
            self.clock.tick(self.FPS)
            self.group.update()
            #self.group.clear(wn, self.bg_screen_draw)
            self.bg_screen_draw()
            self.group.draw(self.wn)
            pygame.display.update()

    def finish_game(self):
        self.FINISH_GAME = True
        print("call finish_game")

    def finish_stat(self):
        print("Game stop")
        print("DISTANCE= " + str(self.DISTANCE))
        for i in range(self.PLAYERS):
            print("distance_player" + str(i) + " = " + str(self.group.sprites()[i].distance_player)
                  + "  steps = " + str(len(self.group.sprites()[i].player_steps))
                  + "  cnt = " + str(self.group.sprites()[i].cnt))
            for stp in range(len(self.group.sprites()[i].player_steps)):
                print("player" + str(i) + "  step" + str(stp) + " = " + str(self.group.sprites()[i].player_steps[stp]))

    def clock_thread(self):
        event_surf = pygame.Surface([100, 22])
        event_rect = event_surf.get_rect()
        event_rect.x = self.DISPLAY_WIDTH - 200
        event_rect.y = 13
        event_surf.fill((100, 100, 255))
        self.wn.blit(event_surf, event_rect)
        while not self.stop_event_listener:
            t1 = datetime.datetime.now()
            s = datetime.datetime.strftime(t1, '%H:%M:%S')
            event_text = self.event_font.render(s, False, (0, 0, 0))
            self.wn.blit(event_surf, event_rect)
            self.wn.blit(event_text, (self.DISPLAY_WIDTH - 200, 10))
            pygame.display.update(event_rect)
            time.sleep(0.5)

    def timer_thread(self):
        font = pygame.font.SysFont('Arial black', 18, False)
        t1 = time.time()
        surf = pygame.Surface([100, 22])
        rect = surf.get_rect()
        rect.x = 26
        rect.y = 13
        surf.fill((100, 100, 255))
        self.wn.blit(surf, rect)

        while not self.stop_thread:
            time.sleep(0.01)
            t2 = time.time()
            s = str(round(t2 - t1, 3))
            text = font.render(s, False, (0, 0, 0))
            self.wn.blit(surf, rect)
            self.wn.blit(text, (50, 10))
            pygame.display.update(rect)
# END class Game_______________________


