import pygame
from utils import *
import levels

class OneLevelGame(object):
    def __init__(self, level):
        print(" * Inititlising game...")
        self.level = level
        self.load()


    @classmethod
    def from_level(cls, level):
        path = os.path.join("levels", f"{level}.json")
        assert os.path.exists(path), f"Level file not found: {path}"
        with open(path) as f:
            data = json.load(f)
        level = getattr(levels, f"{data['class']}")(data)
        return cls(level)



    def load(self):
        self.level.load()


    def tick(self):
        pass



