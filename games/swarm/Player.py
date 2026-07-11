import pygame, os

class Player(object):
    def __init__(self, pos, sprite_folder=None):
        self.pos = pos
        self.stance = "idle"
        self.direction = "right"
        self.f = 0
        self.n_frames=12
        self.animation_speed = 0.5
        self.size = [250, 210]
        self.sprite_folder = sprite_folder
        self.surface = pygame.Surface(self.size)
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.stance_duration = None




    def sprite(self):
        from main import ART_FOLDER
        sprite = None
        stance = self.stance
        if self.stance is None:
            stance = "idle"
        if self.sprite_folder is not None:
            try:
                stance_folder = os.path.join(ART_FOLDER, self.sprite_folder, stance)
                n_frames = len(os.listdir(stance_folder))
                for frame_img  in os.listdir(stance_folder):
                    if frame_img.split(".")[0].endswith(f"f{self.f//1 % n_frames}"):
                        sprite_path = os.path.join(stance_folder, frame_img)
                        img = pygame.image.load(sprite_path).convert_alpha()
                        return img

            except:
                raise
        return sprite


    def set_stance(self, stance=None, duration=None, reset=False):

        if (not reset) and (stance != self.stance):
            return





        print(stance, duration, reset)
        
        if self.stance_duration is not None: 
            if self.stance_duration <= 0:
                reset = True
                if stance is None:
                    stance = "idle"
                    duration = None

        if reset: 
            self.f = 0
            self.stance_duration = duration

        self.stance = stance
        return self

    def update(self):
        if self.stance_duration is not None:
            if self.stance_duration <= 0:
                self.set_stance("idle")
        return self




    def draw(self, screen):
        print(self.f, end = "\r")
        self.rect.update(*self.pos, 100, 100)
        sprite = self.sprite()
        if sprite is not None:
            rect = sprite.get_rect()
            rect.fit(self.rect)
            pygame.transform.scale(sprite, self.size, self.surface)
            if self.direction == "left":
                self.surface = pygame.transform.flip(self.surface, True, False)
        screen.blit(self.surface, self.rect)
        self.f += 1 / self.animation_speed
        if self.stance_duration is not None:
            self.stance_duration -= 1 * self.animation_speed

        if self.f > 99:
            self.f = 0

        

            



