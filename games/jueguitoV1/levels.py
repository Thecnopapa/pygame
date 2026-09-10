import pygame
from utils import *



class PlatformLevel(object):
    def __init__(self, config):
        print(" * Inititlising level...")
        if type(config) is dict:
            self.config = config
        else:
            assert os.path.exists(config)
            with open(config) as f:
                self.config = json.load(f)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.config.get('name')}>"

    def load(self):
        print(" * Loading level:", self)
        pass