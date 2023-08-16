from assets.scripts.core_funcs import *
class CheckBox:
    def __init__(self, args):
        self.pos = args[0]
        self.font = args[1]
        self.checked = args[2]
        self.game = args[3]
        self.rect_surf = pygame.Surface((32, 32))
        self.mask = pygame.mask.from_surface(self.rect_surf)
        self.outlines = self.mask.outline()
        self.bg_surf = pygame.Surface((32, 32))
        self.bg_surf.set_colorkey((0, 0, 0))
        self.just_checked = False
    def update(self):
        self.bg_surf.fill((0, 0, 0))
        pygame.draw.lines(self.bg_surf, (1, 1, 1), True, self.outlines, 3)
        self.rect = pygame.Rect(self.bg_surf.get_width()/2-10, self.bg_surf.get_height()/2-10, 20, 20)
        if self.checked:
            pygame.draw.rect(self.bg_surf, (0, 0, 50), self.rect)
        if self.bg_surf.get_rect(topleft=self.pos).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            if not self.just_checked:
                self.checked = not(self.checked)
                self.just_checked = True
        else:
            self.just_checked = False
        win.blit(self.bg_surf, self.pos)