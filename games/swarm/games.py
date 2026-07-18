import pygame, json, os
from pygame import Vector2

from players import Player


plats_json = {
    "plat1": {
        "x": "50vw",
        "y": "-20vh",
        "w": "20vw",
        "h": "5vh",
        "texture": os.path.join("terrain", "floor", "grass_01.png"),
        "overflow": {
            "top": "100vh"
        }
    }, 
    "plat2": {
        "x": "30vw",
        "y": "-40vh",
        "w": "20vw",
        "h": "5vh"
    }, 
    "plat3": {
        "x": "40vw",
        "y": "-60vh",
        "w": "20vw",
        "h": "5vh"
    }, 

}


def relative_size(reference, value):

    try:
        reference = pygame.Vector2(reference.get_width(), reference.get_height())
    except:
        try:
            reference = pygame.Vector2(reference.height, reference.width)
        except:
            reference = pygame.Vector2(reference.x, reference.y)


    if type(value) is str:
        if value.endswith("vw"):
            value = float(value.replace("vw", ""))
            value = (reference.x * value /100)
        elif value.endswith("vh"):
            value = float(value.replace("vh", ""))
            value = (reference.y * value /100) 
        elif value.endswith("px"):
            value = float(value.replace("px", ""))
        else:
            value = float(value)
    return value


class Platform(object):
    def __init__(self, game, start_size, start_pos, fixed=False, passable=True, texture=None, overflow=None):

        w = relative_size(game.screen, start_size[0])
        h = relative_size(game.screen, start_size[1])
        x = relative_size(game.screen, start_pos[0]) 
        y = relative_size(game.screen, start_pos[1]) - h + game.screen.get_height() 
        print(x, y)

        start_size = pygame.Vector2(w, h)
        start_pos = pygame.Vector2(x, y)
        
        if type(fixed) is bool:
            fixed = [fixed, fixed]

        self.fixed = fixed
        self.passable = passable

        if overflow is None:
            overflow = {}
        self.overflow = overflow

        self.size = start_size
        self.pos = start_pos
        if texture is None:
            self.surface = pygame.Surface(start_size)
            self.surface.fill("cyan")
        else:
            from main import ART_FOLDER
            self.surface = pygame.image.load(os.path.join(ART_FOLDER, texture))
            self.surface = pygame.transform.scale_by(self.surface , self.size.y/(self.surface.get_rect().height + relative_size(self.surface, self.overflow.get("top",0))))
            #self.surface = pygame.transform.scale(self.surface, self.size)
        self.rect = pygame.Rect(self.pos, self.size)
        #self.rect.move_ip(self.pos)
        print(" * New platform with rect:", self.rect)

    def draw(self, screen, game):

        overflow_top = relative_size(self.size, self.overflow.get("top",0))

        rect = self.rect.copy()
        rect.y -= overflow_top
        rect.height +=  overflow_top

        texture = pygame.transform.scale_by(self.surface, rect.height/self.surface.get_rect().height)
        text_rect = texture.get_rect()

        for i in range(self.rect.width // text_rect.width):
            screen.blit(texture, rect)
            rect.x += text_rect.width

        text_rect.width = self.rect.width % text_rect.width

        screen.blit(texture, rect, area=text_rect)





class Game(object):
    def __init__(self, screen):
        screen.add(self)
        self.player = Player(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2), 
                             #sprite_folder="characters2D/Wraith_01/PNG")
                             sprite_folder=os.path.join("characters", "samurai_01", "stances")

        self.platforms = {}
        self.floor = Platform(self, [self.screen.get_width()*2, "5vh"], ["0vw", "0vh"], fixed=[False, False], passable=False, texture="terrain/floor/grass_01.png", overflow={"top": "20vh"})
        

        self.platforms["floor"] = self.floor
        print(json.dumps(plats_json, indent=4))

        for k, plat in plats_json.items():
            print(plat)
            self.platforms[k] = Platform(self, (plat["w"], plat["h"]), [plat["x"], plat["y"]], texture=plat.get("texture", None), overflow=plat.get("overflow", None))

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
        self.scroll.x += dist #+40
        if self.scroll.x <= 0:
            dist = dist-self.scroll.x
            self.scroll.x = 0
        for plat in self.platforms.values():
            if not plat.fixed[0]:
                plat.rect.move_ip(-dist, 0)
        self.player.pos.x -= dist

    def scroll_y(self, dist):

        self.scroll.y += dist #+40
        if self.scroll.y >= 0:
            dist = dist-self.scroll.y
            self.scroll.y = 0

        for plat in self.platforms.values():
            if not plat.fixed[1]:
                plat.rect.move_ip(0, -dist)
        self.player.pos.y -= dist

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

        if keys[pygame.K_LSHIFT]:
            dist *= 2
            player.sprinting = True
        else:
            player.sprinting = False

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

        # if keys[pygame.K_q]:
        #     new_stance = "cast"

        player.set_stance(new_stance, duration=1, direction=direction, force = False)


        #pygame.draw.line(self.screen, "green", Vector2((self.screen.get_width() * 0.8), 0), Vector2((self.screen.get_width() * 0.8), self.screen.get_height()))
        #pygame.draw.line(self.screen, "green", Vector2((self.screen.get_width() * 0.2), 0), Vector2((self.screen.get_width() * 0.2), self.screen.get_height()))

        print(self.scroll)

        if player.centre().x > (self.screen.get_width() * 0.8):
            self.scroll_x(dist)
        elif player.centre().x  < (self.screen.get_width() * 0.2):
            self.scroll_x(-dist)

        if player.centre().y > (self.screen.get_height() * 0.5):
            self.scroll_y(dist)
        elif player.centre().y  < (self.screen.get_height() * 0.2):
            self.scroll_y(-dist)

        player.pos.y = min(self.screen.get_height()-player.size.y, player.pos.y)
        player.pos.x = max(0, player.pos.x)



        



