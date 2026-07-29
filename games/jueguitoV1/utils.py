import pygame
from pygame import Vector2 as V


class InvalidVector(Exception):
    pass

class Location(object):
    def __init__(self, x=0, y=0, w=0, h=0, p=None, s=None):

        if p is not None:
            if isinstance(p, V):
                self.x, self.y = p.x, p.y
            elif type(p) in (list, tuple):
                self.x, self.y = p[0], p[1]
            else:
                raise InvalidVector(p)
        else:
            self.x, self.y = x, y

        if s is not None:
            if isinstance(s, V):
                self.w, self.h = s.x, s.y
            elif type(s) in (list, tuple):
                self.w, self.h = s[0], s[1]
            else:
                raise InvalidVector(s)
        else:
            self.w, self.h = h, w


    def pos(self):
        return V(self.x, self.y)

    def size(self):
        return V(self.w, self.h)

    def surface(self):
        return pygame.Surface([self.w, self.h])

    def rect(self):
        return pygame.Rect([self.x, self.y, self.w, self.h])

    def centre(self):
        cx = self.x + (self.w/2)
        cy = self.y + (self.h/2)
        return V(cx, cy)