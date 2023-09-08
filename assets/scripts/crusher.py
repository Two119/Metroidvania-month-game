from assets.scripts.core_funcs import *
class Crusher:
    def __init__(self, pos):
        self.tile_pos = [int(pos[0]/64), int(pos[1]/64)]
        if not web:
            img = scale_image(pygame.image.load("assets\Spritesheets\crusher.png").convert(), 4)
            swap_color(img, [87, 114, 119], [255, 255, 255])
            swap_color(img, [129, 151, 150], [195, 195, 195])
            swap_color(img, [168, 181, 178], [195, 195, 195])
            self.spritesheet = SpriteSheet(img, [12, 1])
            self.sound = pygame.mixer.Sound("assets\Audio\crusher.ogg")
        else:
            img = scale_image(pygame.image.load("assets/Spritesheets/crusher.png").convert(), 4)
            swap_color(img, [87, 114, 119], [255, 255, 255])
            swap_color(img, [129, 151, 150], [195, 195, 195])
            swap_color(img, [168, 181, 178], [195, 195, 195])
            self.spritesheet = SpriteSheet(img, [12, 1])
            self.sound = pygame.mixer.Sound("assets/Audio/crusher.ogg")
        self.spritesheet.size = [64*4, 64*4]
        self.frame = [0, 0]
        self.pos = [pos[0], pos[1]+4]
        self.rect = pygame.Rect(self.pos[0]+(16*4), self.pos[1], 32*4, 64*4)
        self.falling = False
        self.adder = 1
        self.delay = 0
        self.cycles = 0
    def update_animation(self, delay_wait, renderer):
        if hasattr(renderer, "dt"):
            if round(delay_wait/renderer.dt) != 0:
                self.delay += (1*renderer.dt)
                if int(self.delay) % round(delay_wait/renderer.dt) == 0:
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
        self.cycles += 1
        if self.cycles == 1:
            for obj in renderer.queue:
                if obj.__class__.__name__ == "MovingPlatform":
                    if obj.rect.collidepoint(self.pos):
                        obj.objects.append(self)
        if hasattr(renderer, "dt") and hasattr(renderer.queue[0], "rect"):
           
            self.rect = pygame.Rect(self.pos[0]+(16*4), self.pos[1], 32*4, 64*4)
            if self.rect.colliderect(renderer.queue[0].rect):
                self.falling = True
            for enemy in renderer.enemies:
                e = renderer.queue[enemy]
                if (e.__class__.__name__ == "EnemySwordsman" or e.__class__.__name__ == "EnemyWizard") and hasattr(e, "rect"):
                    if self.rect.colliderect(e.rect):
                        self.falling = True
            if self.falling:
                self.update_animation(6, renderer)
            win.blit(self.spritesheet.get(self.frame), self.pos)