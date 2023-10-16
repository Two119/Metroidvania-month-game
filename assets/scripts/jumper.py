from assets.scripts.core_funcs import *
class Jumper:
    def __init__(self, position):
        self.pos = [position[0]+2, position[1]-20]
        sheet = scale_image(pygame.image.load("assets/Spritesheets/Jumper.png").convert())
        self.spritesheet = SpriteSheet(sheet, [8, 1], [237, 28, 36])
        self.frame = 0
        self.jumping = False
        self.accel = 100
        self.time = time.time()
        self.mask = pygame.mask.from_surface(self.spritesheet.get([self.frame, 0]))
    def update_animation(self, renderer):
        self.mask = pygame.mask.from_surface(self.spritesheet.get([self.frame, 0]))
        if time.time() - self.time >= 0.1:
            self.frame += 1 
            if renderer.queue[0].mask.overlap(self.mask, (self.pos[0]-renderer.queue[0].pos[0], self.pos[1]-renderer.queue[0].pos[1])) != None:
                #renderer.queue[0].on_booster = True
                if self.frame < 3:
                    renderer.queue[0].pos[1] += 4
                if self.frame == 3:
                    renderer.queue[0].jumping = True
                    renderer.queue[0].standing = False
                    renderer.queue[0].just_jumped = True
                    renderer.queue[0].vel[1] = 0-(find_u(384, (0.24)*(renderer.dt)))
                    renderer.queue[0].pos[1] -= 32
                    #renderer.queue[0].on_booster = False
            self.time = time.time()
        if self.frame > 7:
            self.frame = 0
            self.mask = pygame.mask.from_surface(self.spritesheet.get([self.frame, 0]))
            self.jumping = False
    def append_rects(self, renderer):
        pass
        #self.rects = [pygame.Rect(self.pos[0], self.pos[1]+40, 1, 28), pygame.Rect(self.pos[0]+64, self.pos[1]+40, 1, 28)]
        #renderer.side_rects.append([self.rects[0], -1])
        #renderer.side_rects.append([self.rects[1], 1])
        #[pygame.draw.rect(win, [255, 0, 0], r) for r in self.rects]
    def update(self, renderer):
        self.jump_rect = self.spritesheet.get([self.frame, 0]).get_rect(topleft=self.pos)
        self.jump_rect.x += 4
        self.jump_rect.w -= 8
        self.jump_rect.y += 20
        self.jump_rect.h -= 24
        
        pygame.draw.rect(win, [255, 0, 0], self.jump_rect)
        if hasattr(renderer.queue[0], "rect"):
            if self.jump_rect.colliderect(renderer.queue[0].rect) and not self.jumping:
                if renderer.queue[0].mask.overlap(self.mask, (self.pos[0]-renderer.queue[0].pos[0], self.pos[1]-renderer.queue[0].pos[1])) != None:
                    self.jumping = True
                    self.time = time.time()
        if self.jumping:
            self.update_animation(renderer)
        
        renderer.standing_masks.append([self.mask, self.pos, self])
        win.blit(self.spritesheet.get([self.frame, 0]), self.pos)