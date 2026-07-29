import pygame
from utils import *


class MenuButton(object):
    def __init__(self, text, pos, on_click=None, on_hover=None, centered=False):
        self.font = pygame.font.Font(None, 36)
        self.color = [255, 255, 255]
        self.new_color = None
        self.text = text
        size = V(self.font.size(self.text))
        if centered:
            pos.x -= size.x/2
            pos.y -= size.y/2
            pass
        self.location = Location(p=pos,s=size)

        self.rect = self.location.rect()
        print(self.rect)

        self.on_click = on_click
        self.on_hover = on_hover

    def check(self):
        coords = pygame.mouse.get_pos()
        if self.in_button(coords):
            self.hover()
            if pygame.mouse.get_pressed()[0]:
                #print(pygame.mouse.get_pressed()[0])
                self.click()

    def in_button(self, coords):
        return self.rect.collidepoint(coords)

    def draw(self, screen):
        color = self.color
        if self.new_color is not None:
            color = self.new_color
        text = self.font.render(self.text, 1, color)
        screen.blit(text, self.rect)
        self.new_color = None

    def hover(self, *args, **kwargs):
        if self.on_hover is None:
            return
        return self.on_hover(*args, button=self,  **kwargs)

    def click(self, *args, **kwargs):
        if self.on_click is None:
            return
        return self.on_click( *args ,button=self, **kwargs)

    def darken(button):
        button.new_color = [button.color[0]*0.6, button.color[1]*0.6, button.color[2]*0.6]




class Menu(object):
    def __init__(self, engine):
        self.engine = engine
        self.background = None
        self.buttons = []

    def draw(self):
        if self.background is not None:
            self.engine.screen.blit(self.background, self.engine.screen.get_rect())

        for button in self.buttons:
            button.check()
            button.draw(self.engine.screen)

class MainMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = Location(0,0, self.engine.screen.get_width(), self.engine.screen.get_height())
        self.background = pygame.image.load(os.path.join(ART_FOLDER, "backgrounds", "menu", "gdd_portrait.jpeg"))
        #self.background.fill([0, 255, 255, 128])
        self.background= self.background.convert_alpha()
        print(self.location)
        print(self.location.centre())
        
        self.buttons.append(MenuButton("New Game", self.location.centre(), on_click=self.engine.start_game, on_hover=MenuButton.darken, centered=True))



class InGameMenu(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background = pygame.Surface(V(engine.screen.get_width(), engine.screen.get_width()))
        self.background.fill([0, 0, 0, 128])
        self.background=background.convert_alpha()
        
        self.buttons = [
            MenuButton("Continue", Vector2(60, 60), on_click=self.unpause, on_hover=Button.darken),
            MenuButton("Quit Game", Vector2(60, 120), on_click=self.quit, on_hover=Button.darken)
        ]


    

