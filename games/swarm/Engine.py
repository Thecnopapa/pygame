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
