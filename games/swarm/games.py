import pygame, json
from pygame import Vector2

from players import Player


plats_json = {
    "plat1": {
        "x": "50vw",
        "y": "-20vh",
        "w": "20vw",
        "h": "1vh"
    }, 
    "plat2": {
        "x": "30vw",
        "y": "-40vh",
        "w": "20vw",
        "h": "1vh"
    }, 
    "plat3": {
        "x": "40vw",
        "y": "-60vh",
        "w": "20vw",
        "h": "1vh"
    }, 

}


def relative_size(screen, value):
    if type(value) is str:
        if value.endswith("vw"):
            value = float(value.replace("vw", ""))
            value = (screen.get_width() * value /100)
        elif value.endswith("vh"):
            value = float(value.replace("vh", ""))
            value = (screen.get_height() * value /100) 
        elif value.endswith("px"):
            value = float(value.replace("px", ""))
        else:
            value = float(value)
    return value


class Platform(object):
    def __init__(self, game, start_size, start_pos, fixed=False, passable=True):

        w = relative_size(game.screen, start_size[0])
        h = relative_size(game.screen, start_size[1])
        x = relative_size(game.screen, start_pos[0]) 
        y = relative_size(game.screen, start_pos[1]) - h + game.screen.get_height() 
        print(x, y)

        start_size = pygame.Vector2(w, h)
        start_pos = pygame.Vector2(x, y)
        
        self.fixed = fixed
        self.passable = passable

        self.size = start_size
        self.pos = start_pos
        self.surface = pygame.Surface(start_size)
        self.surface.fill("cyan")
        self.rect = self.surface.get_rect()
        self.rect.move_ip(self.pos)
        print(" * New platform with rect:", self.rect)

    def draw(self, screen, game):

        # if not self.fixed:
        #     self.rect.move_ip(-game.scroll)

        #print(self.rect, game.scroll)
        screen.blit(self.surface, self.rect)





class Game(object):
    def __init__(self, screen):
        screen.add(self)
        self.player = Player(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2), 
                             #sprite_folder="characters2D/Wraith_01/PNG")
                             sprite_folder="characters2D/Samurai_01/PNG")

        self.platforms = {}
        self.floor = Platform(self, [self.screen.get_width(), 10], ["0vw", "0vh"], fixed=True, passable=False)
        

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
            self.screen.blit(self.floor.surface, self.floor.rect)
            for plat in self.platforms.values():
                plat.draw(self.screen, self)

            self.player.draw(self.screen)
            




            #print(self.floor_rect)


    def scroll_x(self, dist):
        self.scroll.x += dist +40
        for plat in self.platforms.values():
            if not plat.fixed:
                plat.rect.move_ip(-dist, 0)
        self.player.pos.x -= dist

    def update(self):
        player = self.player.update()
        keys = self.engine.keys
        dt = self.engine.dt
        up = keys[pygame.K_w] or keys[pygame.K_UP]
        down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        new_stance = player.stance
        direction = player.direction

        dist = dt * 300
        
        player.gravity(dist, self.platforms)

        if up or keys[pygame.K_SPACE]:
            player.jump(dist*3)
        elif down:
            player.go_down()

        if left:
            player.pos.x -= dist
            direction = "left"

        if right:
            player.pos.x += dist
            direction = "right"

        if left or right:
            new_stance = "walk"


        # if keys[pygame.K_SPACE]:
        #     new_stance = "attack"

        if keys[pygame.K_q]:
            new_stance = "cast"

        player.set_stance(new_stance, duration=1, direction=direction, force = False)


        pygame.draw.line(self.screen, "green", Vector2((self.screen.get_width() * 0.8), 0), Vector2((self.screen.get_width() * 0.8), self.screen.get_height()))
        pygame.draw.line(self.screen, "green", Vector2((self.screen.get_width() * 0.2), 0), Vector2((self.screen.get_width() * 0.2), self.screen.get_height()))

        if player.centre().x > (self.screen.get_width() * 0.8):
            #print("Scrolling right", f"{player.pos.x:.2f} {self.scroll.x:.2f} {(self.screen.get_width() * 0.8):.2f}  {(self.screen.get_width() * 0.8):.2f}")
            self.scroll_x(dist)
        
        elif player.centre().x  < (self.screen.get_width() * 0.2):
            #print("Scrolling left", f"{player.pos.x:.2f} {self.scroll.x:.2f} {(self.screen.get_width() * 0.2):.2f}  {(self.screen.get_width() * 0.):.2f}")
            self.scroll_x(-dist)


        



