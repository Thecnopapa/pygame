import pygame

from players import Player

class Game(object):
    def __init__(self, screen):
        screen.add(self)
        self.player = Player(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2), 
                             sprite_folder="characters2D/Wraith_01/PNG")

        self.platforms = {}
        self.floor = pygame.Surface([self.screen.get_width(), 10])
        self.floor_rect = self.floor.get_rect()
        self.floor_rect.move_ip(0, self.screen.get_height()-10)
        self.floor.fill("cyan")

        self.platforms["floor"] = self.floor_rect

    def draw(self):
        if self.screen is not None:
            self.player.draw(self.screen)
            self.screen.blit(self.floor, self.floor_rect)
            #print(self.floor_rect)


    def update(self):
        player = self.player.update()
        keys = self.engine.keys
        dt = self.engine.dt
        up = keys[pygame.K_w] or keys[pygame.K_UP]
        down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        new_stance = player.stance


        dist = dt * 300
        
        player.gravity(dist, self.platforms)

        if up:
            player.jump(dist)

        if left:
            player.pos.x -= 300 * dt
            player.direction = "left"
        if right:
            player.pos.x += 300 * dt
            player.direction = "right"

        if left or right:
            new_stance = "walk"


        if keys[pygame.K_SPACE]:
            new_stance = "attack"

        if keys[pygame.K_q]:
            new_stance = "cast"

        if new_stance != player.stance:
            player.set_stance(new_stance, duration=1, force = False)



