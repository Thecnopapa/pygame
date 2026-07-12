import pygame

from engines import Engine

class Screen(object):
    def __init__(self, engine,  width=1280, height=720, background=None):
        self.engine = engine
        self.screen = pygame.display.set_mode((width, height))
        self.fps = engine.fps
        self.dt = engine.dt
        self.background = background

        self.components = []

    def clear(self):
        if self.background is not None:
            self.screen.fill(self.background)

    def tick(self):
        for comp in self.components:
            comp.draw()

    def add(self, comp):
        comp.screen = self.screen
        comp.engine = self.engine
        self.components.append(comp)

