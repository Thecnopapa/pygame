import pygame
from utils import *
from menu import MainMenu
from game import OneLevelGame
class Engine(object):
    def __init__(self, fps=60, width=1280, height=720):
        log(1, "Inititlising engine...")
        pygame.init()
        self.fps=fps
        self.dt=0
        self.clock = pygame.time.Clock()
        self.keys = None
        self.running = True
        self.background = "black"
        self.screen = pygame.display.set_mode((width, height))
        self.game = None
        self.menu = MainMenu(self)

    def start_frame(self):
        for event in pygame.event.get():
            #print(event.type, pygame.QUIT)
            if event.type == pygame.QUIT:
                self.running = False
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LCTRL] and self.keys[pygame.K_c]:
            self.running = False
        self.clear()

    def tick(self):
        print(f"#TICK {float(self.clock.get_fps()):3.0f} fps", end="\r")
        self.game.tick()

    def show_menu(self):
        self.menu.draw()

    def start_game(self, level=None, button=None):
        self.game = OneLevelGame.from_level(level)

    def clear(self):
        if self.background is not None:
            self.screen.fill(self.background)

    def end_frame(self):
        pygame.display.flip()
        self.dt = self.clock.tick(self.fps) / 1000

    def quit(self):
        pygame.quit()
        quit(0)
