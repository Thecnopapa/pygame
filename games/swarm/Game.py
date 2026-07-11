import pygame

from Player import Player

class Game(object):
    def __init__(self, screen):
        screen.add(self)
        self.player = Player(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2), 
                             sprite_folder="characters2D/Wraith_01/PNG")

    def draw(self):
        if self.screen is not None:
            self.player.draw(self.screen)


    def update(self):
        player = self.player.update()
        keys = self.engine.keys
        dt = self.engine.dt
        up = keys[pygame.K_w] or keys[pygame.K_UP]
        down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]


        if up:
            player.pos.y -= 300 * dt
        if down:
            player.pos.y += 300 * dt
        if left:
            player.pos.x -= 300 * dt
            player.direction = "left"
        if right:
            player.pos.x += 300 * dt
            player.direction = "right"

        if up or down or left or right:
            player.set_stance("walk", duration=None)


        if keys[pygame.K_SPACE]:
            player.set_stance("attack", duration=12)


