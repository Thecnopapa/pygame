import pygame, os, math



class Player(object):
    def __init__(self, pos, sprite_folder=None):
        # Static
        self.sprite_folder = sprite_folder

        # Movement
        self.pos = pos
        self.stance = None
        self.direction = "right"
        self.floating = True
        self.jumping = 0
        self.jump_speed = 0

        # Sprite
        self.size = pygame.Vector2(100, 150)
        self.rect = pygame.Rect(*self.pos, *self.size)
        
        # Animation
        self.animation_speed = 1
        self.idle_counter=0
        self.f = 0
        self.n_frames=None
        self.stance_duration = 1
        self.stance_folder = None
        self.current_sprites = None

        # Init
        self.set_stance("idle", force=True)


    def jump(self, dist, start=8):

        #print(f"JUMP (folating={self.floating})")
        if not self.floating:
            self.jump_speed = start
            self.floating = True
            self.pos.y -= dist * self.jump_speed 




    def gravity(self, dist, platforms=None, gravity = 2):
        #print("Gravity")
        if platforms is not None:
            #print(self.rect, self.rect.collidedict(platforms, values=1))
            if self.rect.collidedict(platforms, values=1) is not None:
                self.floating = False

        if self.floating and self.jump_speed > 0:
            self.pos.y -= dist * (self.jump_speed - gravity)
            self.jumping -= self.jump_speed
            self.jump_speed -= 1
        else:
            jumping = 0

            if self.floating:
                self.pos.y += dist * gravity


    def set_stance(self, stance=None, duration=1, force=False):
        from main import ART_FOLDER
        
        if force or stance != self.stance:
            #print(self.stance, "-->", stance)
            self.stance = stance
            self.f = 0
            self.duration = duration

            self.stance_folder = os.path.join(ART_FOLDER, self.sprite_folder, self.stance)
            self.current_sprites = os.listdir(self.stance_folder)
            self.n_frames = len(self.current_sprites)

        return self

    def sprite(self):
        
        sprite = None
        stance = self.stance
        if self.stance is None:
            stance = "idle"



        if self.sprite_folder is not None:
            try:
                
                if self.f  >= self.n_frames:
                    self.f -= self.n_frames
                    self.stance_duration -= 1
                    if self.stance_duration <= 0:
                        if self.idle_counter >= 5:
                            self.set_stance("blink")
                            self.idle_counter = 0
                        else:
                            self.set_stance("idle")
                            self.idle_counter += 1
                        self.stance_duration  = 1
                        return self.sprite()

                target_frame = math.floor(self.f % self.n_frames)

                for frame_img  in self.current_sprites:
                    if frame_img.split(".")[0].endswith(f"f{target_frame}"):
                        sprite_path = os.path.join(self.stance_folder, frame_img)
                        img = pygame.image.load(sprite_path).convert_alpha()
                        #print(img)
                        #rect = img.get_rect()
                        #print(rect)
                        #rect.update(rect.height/3, 0, rect.height/1.5, rect.height,)
                        #print(rect)
                        #img = img.subsurface(rect)
                        #print(img)
                        return img
            except:
                raise
        return sprite




    def update(self):
        

        return self




    def draw(self, screen):
        #print(self.f, end="\r")
        self.rect.update(*self.pos, *self.size)
        sprite = self.sprite()
        if sprite is not None:
            rect = sprite.get_rect()
            rect.fit(self.rect)
            self.surface = pygame.transform.scale_by(sprite, self.size.y/rect.height)
            if self.direction == "left":
                self.surface = pygame.transform.flip(self.surface, True, False)
        #print(self.rect)
        
        screen.blit(self.surface, self.rect)
        #pygame.draw.rect(screen, "cyan",self.rect)
        

        self.f += 0.5 * self.animation_speed

        if self.f > 99:
            self.f = 0

        

            



