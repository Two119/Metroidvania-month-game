from assets.scripts.core_funcs import *
class FireBox:
    def __init__(self, init_pos):
        self.pos = [init_pos[0]+4, init_pos[1]+4]
        self.rect = pygame.Rect(self.pos[0], self.pos[1]-64, 64, 128)
        if web:
            fb = pygame.image.load("assets/Spritesheets/firebox.png")
            swap_color(fb, [255, 255, 255], [47, 54, 92])
            f = pygame.image.load("assets/Spritesheets/fire.png")
            swap_color(f, [255, 255, 255], [44, 50, 85])
            self.firebox = SpriteSheet(fb, [33, 1], [47, 54, 92])
            self.fire = SpriteSheet(f, [33, 1], [44, 50, 85])
        else:
            fb = pygame.image.load("assets\\Spritesheets\\firebox.png")
            swap_color(fb, [255, 255, 255], [47, 54, 92])
            f = pygame.image.load("assets\\Spritesheets\\fire.png")
            swap_color(f, [255, 255, 255], [44, 50, 85])
            self.firebox = SpriteSheet(fb, [33, 1], [47, 54, 92])
            self.fire = SpriteSheet(f, [33, 1], [44, 50, 85])
        self.frame = [0, 0]
        self.mask = pygame.mask.from_surface(self.fire.get(self.frame))
        self.delay = 0
        self.is_hovered = False
    def update(self, renderer):
        self.delay+=1
        if (hasattr(renderer, "dt")):
            if round(8/renderer.dt) != 0:
                if (self.delay%round(8/renderer.dt)==0):
                    self.frame[0]+=1
                    if (self.frame[0]>32):
                        self.frame[0] = 0
            self.mask = pygame.mask.from_surface(self.fire.get(self.frame))
            if (hasattr(renderer.queue[0], "rect")):
                if (self.rect.colliderect(renderer.queue[0].rect)):
                    if (self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-self.pos[0], renderer.queue[0].pos[1]-(self.pos[1]-64)))!=None) and self.frame[0] in range(4, 21):
                        renderer.queue[0].is_alive = False
                        renderer.queue[0].deaths += 1
            for enemy in renderer.enemies:
                if (hasattr(renderer.queue[enemy], "rect")):
                    if (self.rect.colliderect(renderer.queue[enemy].rect)):
                        if (self.mask.overlap(renderer.queue[enemy].mask, (renderer.queue[enemy].pos[0]-self.pos[0], renderer.queue[enemy].pos[1]-(self.pos[1]-64)))!=None) and self.frame[0] in range(4, 21):
                            renderer.queue[enemy].is_alive = False
                       
            win.blit(self.fire.get(self.frame), [self.pos[0], self.pos[1]-64])
            win.blit(self.firebox.get(self.frame), self.pos)
            renderer.standing_masks.append([pygame.mask.from_surface(self.firebox.get(self.frame)), self.pos, self])
            self.mask = pygame.mask.from_surface(self.firebox.get(self.frame))
        if self.is_hovered:
            if pygame.mouse.get_pressed()[2]:
                renderer.queue.remove(self)
                del self
                return 

