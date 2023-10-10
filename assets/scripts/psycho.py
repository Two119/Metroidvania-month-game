from assets.scripts.hidden_spike import *
class Psycho:
    def __init__(self, position):
        self.pos = position
        self.time = time.time()
        self.moving = False
        sheet = scale_image(pygame.image.load("assets/Spritesheets/ghost.png").convert())
        swap_color(sheet, [53, 53, 64], [1, 1, 1])
        self.sheet = SpriteSheet(sheet, [4, 12], [254, 254, 254])
        self.frame = [0, 0]
        self.vel = [0, 0]
        self.speed = 3.42
        self.angle = 0
        self.just_spawned = True
        self.dir = 1
        self.turning = False
        self.sfx = [pygame.mixer.Sound("assets/Audio/ghost1.ogg"), pygame.mixer.Sound("assets/Audio/ghost2.ogg"), pygame.mixer.Sound("assets/Audio/ghost3.ogg"), pygame.mixer.Sound("assets/Audio/ghost4.ogg")]
    def update_animation(self, row):
        self.frame[1] = row
        if time.time()-self.time > 0.2:
            self.frame[0] += 1
            self.time = time.time()
        if self.frame[0] > 3:
            if not self.just_spawned:
                self.frame[0] = 0
            else:
                self.frame[0] = 3
            if row == 3 or row == 9:
                self.turning = False
            self.just_spawned = False
    def update(self, renderer):
        if hasattr(renderer.queue[0], "mask"):
            self.rect = pygame.Rect(self.pos[0], self.pos[1], 64, 64)
            if self.rect.colliderect(renderer.camera.window_rect) and not self.just_spawned:
                self.moving = True
            self.angle = angle_between([self.pos, renderer.queue[0].pos])
            if self.moving:
                self.vel = [math.cos(radians(self.angle))*self.speed, math.sin(radians(self.angle))*self.speed]
                chance = randint(0, round(150*renderer.dt))
                if chance == 35:
                    if not renderer.swoosh_channel.get_busy():
                        renderer.swoosh_channel.play(self.sfx[randint(0, len(self.sfx)-1)])
            else:
                self.vel = [0, 0]
            if renderer.queue[0].pos[0] < self.pos[0]:
                if self.dir != 1:
                    self.turning = True
                    self.frame[0] = 0
                self.dir = 1
            else:
                if self.dir != -1:
                    self.turning = True
                    self.frame[0] = 0
                self.dir = -1
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            if self.just_spawned and self.rect.colliderect(renderer.camera.window_rect):
                self.update_animation(0)
            if self.moving:
                if not self.turning:
                    if self.dir == -1:
                        self.update_animation(2)
                    elif self.dir == 1:
                        self.update_animation(8)
                else:
                    if self.dir == 1:
                        self.update_animation(3)
                    elif self.dir == -1:
                        self.update_animation(9)
            self.mask = pygame.mask.from_surface(self.sheet.get(self.frame))
            if self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-self.pos[0], renderer.queue[0].pos[1]-self.pos[1])):
                renderer.queue[0].is_alive = False
                renderer.queue[0].deaths += 1
            win.blit(self.sheet.get(self.frame), self.pos)
