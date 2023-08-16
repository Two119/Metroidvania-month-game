from assets.scripts.core_funcs import *
class Slider:
    def __init__(self, args):
        self.pos = args[0]
        self.font = args[1]
        self.div = args[2]
        if len(args) == 4:
            self.game = args[3]
            if self.div:
                self.x_offset = self.game.renderer.queue[0].channel.get_volume()*100
            else:
                self.x_offset = self.game.renderer.def_frame
        self.rect_surf = pygame.Surface((32, 32))
        self.mask = pygame.mask.from_surface(self.rect_surf)
        self.outlines = self.mask.outline()
        self.bg_surf = pygame.Surface((32, 32))
        self.bg_surf.set_colorkey((0, 0, 0))
    def update(self):
        self.bg_surf.fill((0, 0, 0))
        self.overall_rect = pygame.Rect(self.pos[0], self.pos[1]-10, 120, 40)
        self.bar_rect = pygame.Rect(self.pos[0], self.pos[1], 120, 20)
        self.slider_rect = pygame.Rect(self.pos[0]+self.x_offset, self.pos[1]-10, 20, 40)
        if self.overall_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.x_offset = pygame.mouse.get_pos()[0]-self.pos[0]
        if self.x_offset > 100:
            self.x_offset = 100
        if self.x_offset < 40 and not self.div:
            self.x_offset = 40
        #pygame.draw.rect(win, (0, 0, 255), self.overall_rect)
        pygame.draw.rect(win, (0, 0, 50), self.bar_rect)
        pygame.draw.rect(win, (255, 255, 255), self.slider_rect)
        self.value = round(self.x_offset/10)
        if self.div:
            self.game.volume = self.value/10
        else:
            self.value *= 10
            self.game.renderer.def_frame = self.value
        value = self.font.render(str(self.value), False, (255, 255, 255), (0, 0, 0))
        value.set_colorkey((0, 0, 0))
        pygame.draw.lines(self.bg_surf, (1, 1, 1), True, self.outlines, 3)
        self.bg_surf.blit(value, [self.bg_surf.get_width()/2-value.get_width()/2, self.bg_surf.get_height()/2-value.get_height()/2])
        win.blit(self.bg_surf, [self.pos[0]+self.overall_rect.w+25, self.pos[1]-(self.bar_rect.h/4)])
        
        
        