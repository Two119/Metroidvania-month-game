from assets.scripts.core_funcs import *
class Shop:
    def  __init__(self, renderer):
        self.tiles = [117, 118, 121, 116]
        self.tile_names_dict = {117: "Spike", 118: "Hidden Spike", 121: "Swinging Axe", 116: "Fire platform"}
        self.tile_images = [renderer.spikesheet.sheet[0][3].copy(), renderer.spikesheet.sheet[0][3].copy()]
        fb = pygame.image.load("assets/Spritesheets/FireBox.png").convert()
        fb = scale_image(fb)
        self.firebox_sheet = SpriteSheet(fb, [13, 1], [255, 255, 255])
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
        self.font : pygame.font.Font = renderer.font
        self.item_names = [self.font.render(self.tile_names_dict[self.tiles[i]], False, [255, 255, 255], [0, 0, 0]) for i in range(len(self.tiles))]
        [item.set_colorkey([0, 0, 0]) for item in self.item_names]
        self.firebox_masks = [pygame.mask.from_surface(image) for image in self.firebox_sheet.sheet[0]]
        self.firebox_frame = 0
        self.delay = 0
    def update(self, renderer):
        x = ((1280-self.bg_tex.get_width())/2)+128
        y = -128
        self.delay += (1*renderer.dt)
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
        for i in range(len(self.tile_masks)):
            if cursor_mask.overlap(self.tile_masks[i], (self.tile_positions[i][0]-pygame.mouse.get_pos()[0], self.tile_positions[i][1]-pygame.mouse.get_pos()[1])) != None:
                win.blit(self.tile_images[i], self.tile_positions[i])
                
        

        