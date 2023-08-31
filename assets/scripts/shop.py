from assets.scripts.core_funcs import *
from assets.scripts.button import *
class Shop:
    def  __init__(self, renderer):
        self.tiles = [117, 118, 121, 116]
        self.tile_names_dict = {117: "Spike", 118: "Hidden Spike", 121: "Swinging Axe", 116: "Fire platform"}
        self.tile_images = [renderer.spikesheet.sheet[0][3].copy(), renderer.spikesheet.sheet[0][3].copy()]
        fb = pygame.image.load("assets/Spritesheets/FireBox.png").convert()
        f = pygame.image.load("assets/Spritesheets/fire.png").convert()
        fb = scale_image(fb)
        f = scale_image(f)
        self.spikesheet = renderer.spikesheet
        self.firebox_sheet = SpriteSheet(fb, [13, 1], [255, 255, 255])
        self.fire_sheet = SpriteSheet(f, [13, 1], [255, 255, 255])
        firebox = self.firebox_sheet.get([0, 0])
        swinging_axe = scale_image(pygame.image.load("assets/Spritesheets/swingin_axe_icon.png").convert())
        swinging_axe.set_colorkey([236, 28, 36])
        self.tile_images.append(swinging_axe)
        self.tile_images.append(firebox)
        self.pos = [0, 0]
        self.bg_tex = scale_image(pygame.image.load("assets/Spritesheets/shop_bg.png").convert())
        self.bg_tex.set_colorkey([255, 255, 255])
        self.tiles_unlocked = [115]
        self.tile_masks = [pygame.mask.from_surface(i) for i in self.tile_images]
        self.tile_positions = []
        self.buttons = []
        self.font : pygame.font.Font = renderer.font
        self.item_names = [self.font.render(self.tile_names_dict[self.tiles[i]], False, [255, 255, 255], [0, 0, 0]) for i in range(len(self.tiles))]
        [item.set_colorkey([0, 0, 0]) for item in self.item_names]
        self.firebox_frame = 0
        self.spike_frame = 0
        self.delay = 0
    def update(self, renderer):
        x = ((1280-self.bg_tex.get_width())/2)+128
        y = -128
        
        win.blit(self.bg_tex, [(1280-self.bg_tex.get_width())/2, (720-self.bg_tex.get_height())/2])
        for i in range(len(self.tile_images)):
            if i % 3 == 0:
                y += 192
                x = ((1280-self.bg_tex.get_width())/2)+128
            if i == 0:
                if self.tiles[i] in self.tiles_unlocked:
                    win.blit(self.tile_images[i], [x-4, y-8])
                else:
                    self.tile_images[i].set_alpha(96)
                    win.blit(self.tile_images[i], [x-4, y-8])
                    self.tile_images[i].set_alpha(255)
                if not ([x-4, y-8] in self.tile_positions):
                    self.tile_positions.append([x-4, y-8])
                win.blit(self.item_names[i], [x-4, y+72])
            elif i == 1:
                if self.tiles[i] in self.tiles_unlocked:
                    win.blit(self.tile_images[i], [x-4, y-8])
                else:
                    self.tile_images[i].set_alpha(96)
                    win.blit(self.tile_images[i], [x-4, y-8])
                    self.tile_images[i].set_alpha(255)
                if not ([x-4, y-8] in self.tile_positions):
                    self.tile_positions.append([x-4, y-8])
                win.blit(self.item_names[i], [x-4-self.tile_images[i].get_width()/2, y+72])
            else:
                if self.tiles[i] in self.tiles_unlocked:
                    win.blit(self.tile_images[i], [x, y])
                else:
                    self.tile_images[i].set_alpha(96)
                    if i != len(self.tile_images) - 1:
                        win.blit(self.tile_images[i], [x, y])
                    else:
                        win.blit(self.tile_images[i], [x, y-64])
                    self.tile_images[i].set_alpha(255)
                if not ([x, y] in self.tile_positions) and i != len(self.tile_images)-1:
                    self.tile_positions.append([x, y])
                if not ([x, y-64] in self.tile_positions) and i == len(self.tile_images)-1:
                    self.tile_positions.append([x, y-64])
                if i < len(self.tile_images)-2:
                    win.blit(self.item_names[i], [x-self.tile_images[i].get_width()/2, y+72])
                else:
                    win.blit(self.item_names[i], [x-8-self.tile_images[i].get_width()/2, y+72])
            x += 192
        if self.buttons == []:
                pass
        for i in range(len(self.tile_masks)):
            if cursor_mask.overlap(self.tile_masks[i], (self.tile_positions[i][0]-pygame.mouse.get_pos()[0], self.tile_positions[i][1]-pygame.mouse.get_pos()[1])) != None:
                if i == len(self.tile_images)-1:
                    pygame.draw.rect(win, [234, 212, 170], pygame.Rect(self.tile_positions[i][0], self.tile_positions[i][1], 64, 128))
                    win.blit(self.firebox_sheet.get([self.firebox_frame, 0]), self.tile_positions[i]) 
                    win.blit(self.fire_sheet.get([self.firebox_frame, 0]), self.tile_positions[i]) 
                    if renderer.clock.get_fps() != 0:
                        self.delay += (1*(60/renderer.clock.get_fps()))
                        if int(self.delay)%round(16/(60/renderer.clock.get_fps()))==0:
                            self.firebox_frame += 1
                            if self.firebox_frame > 12:
                                self.firebox_frame = 0
                elif i == 1:
                    pygame.draw.rect(win, [234, 212, 170], pygame.Rect(self.tile_positions[i][0], self.tile_positions[i][1], 64, 72))
                    win.blit(self.spikesheet.get([self.spike_frame, 0]), self.tile_positions[i]) 
                    win.blit(self.spikesheet.get([self.spike_frame, 0]), self.tile_positions[i]) 
                    if renderer.clock.get_fps() != 0:
                        self.delay += (1*(60/renderer.clock.get_fps()))
                        if int(self.delay)%round(10/(60/renderer.clock.get_fps()))==0:
                            self.spike_frame += 1
                            if self.spike_frame > 3:
                                self.spike_frame = 0
                else:
                    win.blit(self.tile_images[i], self.tile_positions[i])
                
                
        

        