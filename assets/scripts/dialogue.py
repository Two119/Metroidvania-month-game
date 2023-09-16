from assets.scripts.core_funcs import *
class Dialogue:
    def __init__(self, font:pygame.font.Font, text:str, speed:int=8, wraplimit:int=250, h:int=75):
        self.font = font
        self.text = [char for char in text]
        self.string = text
        self.speed = speed
        self.pos = [(1280-wraplimit)/2, 620-h]
        self.wraplimit = wraplimit
        self.char = 0
        self.delay = 0
        self.text_surf = None
        self.bg_color = [58, 68, 102]
        self.bg_color2 = [38, 43, 68]
        self.bg_color3 = [24, 20, 37]
        self.bg_rect = pygame.Rect(self.pos[0]-6, self.pos[1]-6, wraplimit+6, h+6)
        self.o_rect = pygame.Rect(self.pos[0]-10, self.pos[1]-10, wraplimit+14, h+14)
        self.p_rect = pygame.Rect(self.pos[0]-6, self.pos[1]-6, wraplimit+6, h+6)
        self.done = False
        self.finished = False
    def update(self, renderer):
        self.delay += 1
        if (self.delay % round(self.speed/renderer.dt) == 0) and self.char < len(self.text):
            self.char += 1
        if self.char >= len(self.text):
            self.finished = True
        string = ""
        if self.o_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.char = len(self.text)
                self.finished = True
        if self.finished and (pygame.key.get_pressed()[pygame.K_RCTRL] or pygame.key.get_pressed()[pygame.K_LCTRL]):
            self.done = True
        for i in range(0, self.char):
            string = string + self.text[i]    
        self.text_surf = self.font.render(string, False, [255, 255, 255], [0, 0, 0], self.wraplimit)
        self.text_surf.set_colorkey([0, 0, 0])
        
        pygame.draw.rect(win, self.bg_color3, self.o_rect, 4)
        pygame.draw.rect(win, self.bg_color, self.bg_rect)
        pygame.draw.rect(win, self.bg_color2, self.p_rect, 4)
        win.blit(self.text_surf, self.pos)
        