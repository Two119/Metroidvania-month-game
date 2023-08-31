from assets.scripts.core_funcs import *
class SwingingAxe:
    def __init__(self, pos):
        if not web:
            img = pygame.image.load("assets\Spritesheets\swinging_axe.png").convert()
            self.image = scale_image(img).convert()
            self.sound = pygame.mixer.Sound("assets\Audio\spike_spawn.ogg")
        else:
            img = pygame.image.load("assets/Spritesheets/swinging_axe.png").convert()
            self.image = scale_image(img).convert()
            self.sound = pygame.mixer.Sound("assets/Audio/spike_spawn.ogg")
        self.image.set_colorkey([236, 28, 36])
        self.pos = [pos[0]+32, pos[1]+4]
        self.angle = 0
        self.adder = 1.2
        self.shifted = False
        self.swing_angle = 45
        self.img = pygame.transform.rotate(self.image, self.angle)
    def update(self, renderer):
        if hasattr(renderer, "dt") and hasattr(renderer.queue[0], "mask"):
            self.img = pygame.transform.rotate(self.image, self.angle)
            if (not(self.angle < self.swing_angle) and self.angle > 0 and not self.shifted) or (not(self.angle > 0-self.swing_angle) and self.angle < 0 and self.shifted):
                self.shifted = not(self.shifted)
                self.adder*= -1
            self.angle += self.adder*renderer.dt
            self.mask = pygame.mask.from_surface(self.img)
            if self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-(self.pos[0]-(self.img.get_width()/2)), renderer.queue[0].pos[1]-(self.pos[1]-(self.img.get_height()/2)))) == None:
                pass
            else:
                renderer.queue[0].is_alive = False
                #renderer.queue = [ob for ob in renderer.queue if ob != self]
                #reset(renderer.queue[0], renderer)
                renderer.queue[0].deaths += 1
                #del self
                return
            
            win.blit(self.img, [self.pos[0]-int(self.img.get_width()/2), self.pos[1]-int(self.img.get_height()/2)])
            pygame.draw.circle(win, (0, 0, 0), self.pos, 10)
        