import pygame
from utils import *



class PlatformLevel(object):
    def __init__(self, config):
        log(1, "Inititlising level...")
        if type(config) is dict:
            self.config = config
        else:
            assert os.path.exists(config)
            with open(config) as f:
                self.config = json.load(f)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.config.get('name')}>"

    def load(self):
        log(1, "Loading level:", self)

        self.load_background()
        self.load_map()
        self.load_player()

    def load_background(self):
        log(2, "Loading background...")

    def load_map(self):
        log(2, "Loading background...")

    def load_player(self):
        log(2, "Loading player...")
