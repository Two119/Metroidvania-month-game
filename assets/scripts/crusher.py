from assets.scripts.core_funcs import *
class Crusher:
    def __init__(self, pos):
        if not web:
            img = scale_image(pygame.image.load("assets\Spritesheets\crusher.png").convert(), 6)
            swap_color(img, [87, 114, 119], [255, 255, 255])
            swap_color(img, [129, 151, 150], [195, 195, 195])
            swap_color(img, [168, 181, 178], [195, 195, 195])
            self.spritesheet = SpriteSheet(img, [12, 1])
            self.sound = pygame.mixer.Sound("assets\Audio\crusher.ogg")
        else:
            img = scale_image(pygame.image.load("assets/Spritesheets/crusher.png").convert(), 6)
            swap_color(img, [87, 114, 119], [255, 255, 255])
            swap_color(img, [129, 151, 150], [195, 195, 195])
            swap_color(img, [168, 181, 178], [195, 195, 195])
            self.spritesheet = SpriteSheet(img, [12, 1])
            self.sound = pygame.mixer.Sound("assets/Audio/crusher.ogg")
        self.spritesheet.size = [64*6, 64*6]
        self.frame = [0, 0]
        self.pos = [pos[0], pos[1]+8]
        self.rect = pygame.Rect(self.pos[0]+(16*6), self.pos[1], 32*6, 64*6)
        self.falling = False
        self.adder = 1
        self.delay = 0
    def update_animation(self, delay_wait, renderer):
        if hasattr(renderer, "dt"):
            self.delay += 1
            if self.delay % round(delay_wait/renderer.dt) == 0:
                self.frame[0] += self.adder
            if self.frame[0] > 11:
                self.frame[0] = 11
                self.adder=-1
                renderer.coin_channel.play(self.sound)
            if self.frame[0] < 0:
                self.frame[0] = 0
                self.adder=1
                self.falling = False
        self.mask = pygame.mask.from_surface(self.spritesheet.get(self.frame))
    def update(self, renderer):
        if hasattr(renderer, "dt"):
            self.rect = pygame.Rect(self.pos[0]+(16*6), self.pos[1], 32*6, 64*6)
            if self.rect.colliderect(renderer.queue[0].rect):
                self.falling = True
            if self.falling:
                self.update_animation(6, renderer)
            win.blit(self.spritesheet.get(self.frame), self.pos)