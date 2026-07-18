import pygame, os, math
from pygame import Vector2



class Player(object):
    def __init__(self, pos, sprite_folder=None):
        from main import ART_FOLDER
        # Static
        self.sprite_folder = os.path.join(ART_FOLDER, sprite_folder)

        # Movement
        self.pos = pos
        self.stance = None
        self.direction = "right"
        self.floating = True
        self.jump_speed = 1
        self.jump_recovery = 0
        self.going_down = False
        self.floor = None
        self.weight = 1
        self.sprinting = False

        # Sprite
        self.size = pygame.Vector2(100, 150)
        self.rect = pygame.Rect(*self.pos, *self.size)
        
        # Animation
        self.animation_speed = 0.5
        self.idle_counter=0
        self.f = 0
        self.n_frames=None
        self.stance_duration = 1
        self.stance_folder = None
        self.current_sprites = None
        self.wait_end=False

        # Init
        self.set_stance("idle", force=True)


    def centre(self):
        return Vector2(self.pos.x + self.size.x/2, self.pos.y + self.size.y/2)

    def go_down(self):
        if self.going_down is False:
            self.going_down=True


    def jump(self, dist, start=8):

        print(f"JUMP (floating={self.floating})", self.jump_recovery)
        if not self.floating and self.jump_recovery <= 0:
            self.jump_speed = start
            self.floating = True
            self.jump_recovery = 30




    def gravity(self, dist, platforms=None, gravity = 2):
        #print("Gravity", self.jump_speed )
        self.floating = True
        rect_dict = {k: v.rect for k, v in platforms.items()}



        if platforms is not None:
            if not self.floating:
                platforms = {self.floor: platforms[self.floor]}
            for key, plat in platforms.items():
                if self.rect.colliderect(plat.rect):
                    if key == self.going_down or self.jump_speed > 0:
                        self.floating = True
                        print("jumping...")
                        continue

                    if plat.rect.y+plat.rect.height >= (self.pos.y + (self.size.y *0.8)):
                        #print("above floor")
                        if (plat.rect.x < self.centre().x) or (plat.rect.x + plat.rect.width) > self.centre().x:
                            print("in platform")
                            #print(platforms[key].rect.x, center.x)
                            if self.going_down is True and plat.passable:
                                #self.pos.y += dist
                                self.floating = True
                                self.going_down = key
                            else:
                                self.pos.y += plat.rect.y-(self.pos.y + self.size.y)+  (self.size.y*0.1)
                                self.floating = False
                                self.going_down = False
                                self.jump_speed = 0
                                self.floor = key
                                #print([platforms[key].rect.y > (self.pos.y + (self.size.y *0.9)) , (platforms[key].rect.x < self.centre().x or (platforms[key].rect.x + platforms[key].rect.width) > self.centre().x)])
                            continue
                            



        if self.floating and self.jump_speed > 0:
            self.pos.y -= dist * self.jump_speed
            self.jump_speed -= 0.5


        if self.floating:
            self.pos.y += dist * gravity * self.weight

        if self.jump_recovery > 0:
            self.jump_recovery -= 1


    def set_stance(self, stance=None, duration=1, direction="right", force=False, wait_end=False):
        from main import ART_FOLDER
        

        #print(force, self.wait_end, (stance != self.stance) , (direction != self.direction))
        if force or not self.wait_end:
            if (stance != self.stance) or (direction != self.direction) or self.duration < 0:
                print(self.stance, "-->", stance)
                self.stance = stance
                self.f = 0
                self.duration = duration
                self.direction = direction
                self.wait_end = wait_end
                if not wait_end: self.stance_duration =0
                try:
                    self.stance_folder = os.path.join(self.sprite_folder, self.stance+f"_{self.direction}")
                    print(self.stance_folder)
                    assert os.path.exists(self.stance_folder)
                except AssertionError:
                    self.stance_folder = os.path.join(self.sprite_folder, self.stance)
                self.current_sprites = os.listdir(self.stance_folder)
                self.n_frames = len(self.current_sprites)

        return self

    def sprite(self):
        
        sprite = None
        stance = self.stance
        if self.stance is None:
            stance = "idle"

        #print(self.stance_duration)

        if self.sprite_folder is not None:
            try:
                
                if self.f + (0.5 * self.animation_speed) >= self.n_frames:
                    self.f -= self.n_frames
                    self.stance_duration -= 1
                    if self.stance_duration <= 0:
                        if self.idle_counter >= 5:
                            self.set_stance("idle") # blink
                            self.idle_counter = 0
                        else:
                            self.set_stance("idle")
                            self.idle_counter += 1
                        self.stance_duration  = 1
                        #return self.sprite()

                target_frame = math.floor(self.f % self.n_frames)

                for frame_img  in self.current_sprites:
                    if frame_img.split(".")[0].endswith(f"f{target_frame}"):
                        sprite_path = os.path.join(self.stance_folder, frame_img)
                        img = pygame.image.load(sprite_path).convert_alpha()

                        return img
            except:
                raise
        return sprite




    def update(self):
        

        return self




    def draw(self, screen):
        from main import DEBUG
        #print(self.f, end="\r")
        self.rect.update(*self.pos, *self.size)
        sprite = self.sprite()
        if sprite is not None:
            rect = sprite.get_rect()
            rect.fit(self.rect)
            self.surface = pygame.transform.scale_by(sprite, self.size.y/rect.height)
            # if (self.direction == "left") and not self.sprite_folder.endswith("left"):
            #     print(self.direction == "left" , not self.sprite_folder.endswith("left"))
            #     self.surface = pygame.transform.flip(self.surface, True, False)

        #print(self.rect)
        
        if DEBUG:
            pygame.draw.rect(screen, pygame.Color(255,255,255, a=128),self.rect)
        screen.blit(self.surface, self.rect.move(int(-self.size.x/4), 0))
        
        multiplier = 1
        if self.sprinting:
            multiplier +=1
        self.f += 0.5 * self.animation_speed * multiplier

        if self.f > self.n_frames:
            self.f = 1

        

            



