import pygame


class Engine(object):
    def __init__(self, fps=60):
        pygame.init()
        self.fps=fps
        self.dt=0
        self.clock = pygame.time.Clock()
        self.keys = None
        self.running = True

    def start_frame(self):
        for event in pygame.event.get():
            #print(event.type, pygame.QUIT)
            if event.type == pygame.QUIT:
                self.running = False
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_LCTRL] and self.keys[pygame.K_c]:
            self.running = False

    def end_frame(self):
        pygame.display.flip()
        self.dt = self.clock.tick(self.fps) / 1000

    def quit(self):
        pygame.quit()


        

class Screen(object):
    def __init__(self, engine,  width=1280, height=720, background=None):
        self.engine = engine
        self.screen = pygame.display.set_mode((width, height))
        self.fps = engine.fps
        self.dt = engine.dt
        self.background = background

        self.components = []

    def clear(self):
        if self.background is not None:
            self.screen.fill(self.background)

    def tick(self):
        for comp in self.components:
            comp.draw()

    def add(self, comp):
        comp.screen = self.screen
        comp.engine = self.engine
        self.components.append(comp)

class Game(object):
    def __init__(self, screen):
        screen.add(self)
        self.player = Player(pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2))

    def draw(self):
        if self.screen is not None:
            self.player.draw(self.screen)


    def update(self):
        keys = self.engine.keys
        dt = self.engine.dt
        up = keys[pygame.K_w] or keys[pygame.K_UP]
        down = keys[pygame.K_s] or keys[pygame.K_DOWN]
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]


        if up:
            self.player.pos.y -= 300 * dt
        if down:
            self.player.pos.y += 300 * dt
        if left:
            self.player.pos.x -= 300 * dt
        if right:
            self.player.pos.x += 300 * dt


class Player(object):
    def __init__(self, pos):
        self.pos = pos

    def draw(self, screen):
        pygame.draw.circle(screen, "cyan", self.pos, 40)









def main():
    engine = Engine()
    screen = Screen(engine, background="black")

    game = Game(screen)





    while engine.running:

        engine.start_frame()

        screen.clear()

        game.update()

        screen.tick()

        engine.end_frame()

    engine.quit()



if __name__ == "__main__":
    main()
