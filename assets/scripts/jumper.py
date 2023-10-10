from assets.scripts.core_funcs import *
class Jumper:
    def __init__(self, position):
        self.pos = [position[0]-10, position[1]+8]
        sheet = scale_image(pygame.image.load("assets/Spritesheets/Jumper.png").convert())
        self.spritesheet = SpriteSheet(sheet, [8, 1], [237, 28, 36])
        self.frame = 0
        self.jumping = False
        self.accel = 100
        self.time = time.time()
    def update_animation(self):
        if time.time() - self.time >= 0.1:
            self.frame += 1
            self.time = time.time()
        if self.frame > 7:
            self.frame = 0
            self.jumping = False
    def update(self, renderer):
        self.jump_rect = self.spritesheet.get([self.frame, 0]).get_rect(topleft=self.pos)
        self.jump_rect.x += 4
        self.jump_rect.w -= 12
        #pygame.draw.rect(win, [255, 0, 0], self.jump_rect)
        if hasattr(renderer.queue[0], "rect"):
            if self.jump_rect.colliderect(renderer.queue[0].rect) and not self.jumping:
                self.jumping = True
                self.time = time.time()
        if self.jumping:
            self.update_animation()
        
        win.blit(self.spritesheet.get([self.frame, 0]), self.pos)