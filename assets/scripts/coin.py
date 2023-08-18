from assets.scripts.core_funcs import *
class Coin:
    def __init__(self, pos : tuple, spritesheet : pygame.Surface, sheet_size : tuple):
        swap_color(spritesheet, [0, 0, 0], [1, 1, 1])
        img = scale_image(spritesheet)
        img.set_colorkey([255, 255, 255])
        self.spritesheet = SpriteSheet(img, [12, 1])
        self.frame = [0, 0]
        self.pos = pos
        self.delay = 0
        self.collected = False
        self.rect_surf = pygame.Surface((64, 64))
        self.rect_surf.set_alpha(50)
        self.is_hovered = False
        self.shiftable = True
        if not web:
            pygame.mixer.music.load("assets\Audio\coin.ogg")
            self.sound = (pygame.mixer.Sound("assets\Audio\coin.ogg"))
        else:
            pygame.mixer.music.load("assets/Audio/coin.ogg")
            self.sound = (pygame.mixer.Sound("assets/Audio/coin.ogg"))
    def update_animation(self, row, delay_wait, renderer):
        if hasattr(renderer, "dt"):
            if (renderer.dt) != 0:
                if round(delay_wait/(renderer.dt)) != 0:
                    self.frame[1] = row
                    self.delay += 1
                    if self.delay % round(delay_wait/(renderer.dt)) == 0:
                        self.frame[0] += 1
                    if self.frame[0] > 11:
                        self.frame[0] = 0
    def update_physics(self, renderer):
        if hasattr(renderer.queue[0], "mask") and hasattr(renderer.queue[0], "pos"):
            if self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-self.pos[0], renderer.queue[0].pos[1]-self.pos[1])):
                if not self.collected:
                    renderer.coin_channel.play(self.sound)
                    renderer.queue[0].coins += 1
                self.collected = True
        if not self.shiftable:
            self.is_hovered = False
        if self.is_hovered:
            if pygame.mouse.get_pressed()[2]:
                    renderer.levels[renderer.level][int(self.pos[1]/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))][int((self.pos[0]-renderer.camera.cam_change[0])/renderer.tile_size[0])] = renderer.queue[0].tile
                    renderer.queue = [ob for ob in renderer.queue if ob != self]
                    del self
                    return
            pygame.draw.rect(self.rect_surf, (255, 0, 0), pygame.Rect(0, 0, 64, 64))
            win.blit(self.rect_surf, [self.pos[0]+4, self.pos[1]+4])
    def update(self, renderer):
        if not self.collected:
            self.update_animation(0, 10, renderer)
            self.mask = pygame.mask.from_surface(self.spritesheet.get(self.frame))
            win.blit(self.spritesheet.get(self.frame), self.pos)
            self.update_physics(renderer)
        else:
            return
        