import pygame, json

from players import Player


plats_json = {
    "plat1": {
        "x": "50vw",
        "y": "10vh",
        "w": "20vw",
        "h": "10px"
    }
}


def relative_size(screen, value):
    if type(value) is str:
        if value.endswith("vw"):
            value = float(value.replace("vw", ""))
            value = screen.get_width() - (screen.get_width() * value /100)
        elif value.endswith("vh"):
            value = float(value.replace("vh", ""))
            value = screen.get_height() - (screen.get_height() * value /100)
        elif value.endswith("px"):
            value = float(value.replace("px", ""))
        else:
            value = float(value)
    return value


class Platform(object):
    def __init__(self, game, start_size, start_pos, fixed=False):

        w = relative_size(game.screen, start_size[0])
        h = relative_size(game.screen, start_size[1])
        x = relative_size(game.screen, start_pos[0])
        y = relative_size(game.screen, start_pos[1])

        start_size = pygame.Vector2(w, h)
        start_pos = pygame.Vector2(x, y)
        
        self.size = start_size
        self.pos = start_pos
        self.surface = pygame.Surface(start_size)
        self.surface.fill("cyan")
        self.rect = self.surface.get_rect()
        self.rect.move_ip(self.pos)
        print(" * New platform with rect:", self.rect)





class Game(object):
    def __init__(self, screen):
        screen.add(self)
        self.player = Player(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2), 
                             sprite_folder="characters2D/Wraith_01/PNG")

        self.platforms = {}
        self.floor = Platform(self, [self.screen.get_width(), 10], [0, self.screen.get_height()-20], fixed=True)
        

        self.platforms["floor"] = self.floor
        print(json.dumps(plats_json, indent=4))

        for k, plat in plats_json.items():
            print(plat)
            self.platforms[k] = Platform(self, (plat["w"], plat["h"]), [plat["x"], plat["y"]])

        self.scroll = pygame.Vector2(0,0)

    def platform_rects(self):
        return {k: v.rect for k, v in self.platforms.items()}

    def draw(self):
        if self.screen is not None:
            self.player.draw(self.screen)
            self.screen.blit(self.floor.surface, self.floor.rect)
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
        
        player.gravity(dist, self.platform_rects())

        if up:
            player.jump(dist)

        if left:
            player.pos.x -= dist
            player.direction = "left"
        if right:
            player.pos.x += dist
            player.direction = "right"

        if left or right:
            new_stance = "walk"


        if keys[pygame.K_SPACE]:
            new_stance = "attack"

        if keys[pygame.K_q]:
            new_stance = "cast"

        if new_stance != player.stance:
            player.set_stance(new_stance, duration=1, force = False)



