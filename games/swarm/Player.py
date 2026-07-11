import pygame

class Player(object):
    def __init__(self, pos):
        self.pos = pos
        self.stance = "still"
        self.direction = "down"
        self.f = 0
        

    def draw(self, screen):
        pygame.draw.circle(screen, "cyan", self.pos, 40)



