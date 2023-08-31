from assets.scripts.core_funcs import *
class Shop:
    def  __init__(self, renderer):
        self.tiles = [117, 129, 138, 139, 118, 136, 137, 135, 121, 116]
        self.tile_names_dict = {117: "Spike (Up)", 129: "Spike (Down)", 138: "Spike (Right)", 139: "Spike (Left)", 118: "Hidden Spike (Up)", 135: "Hidden Spike (Down)", 136: "Hidden Spike (Right)", 137: "Hidden Spike (Left)", 121: "Swinging Axe", 116: "Fire platform"}
        self.tile_images = [pygame.transform.rotate(renderer.spikesheet.sheet[0][3].copy(), i*90) for i in range(4)]
        for i in range(4):
            self.tile_images.append(self.tile_images[i].copy())
        fb = pygame.image.load("assets/Spritesheets/FireBox.png").convert()
        swap_color(fb, [255, 255, 255], [47, 54, 92])
        fb.set_colorkey([44, 50, 85])
        fb = scale_image(fb)
        firebox_ = SpriteSheet(fb, [13, 1], [47, 54, 92]).get([0, 0])
        firebox = pygame.Surface([64, 64])
        firebox.blit(firebox_, [0, -64])
        firebox.set_colorkey([0, 0, 0])
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
    def update(self):
        x = ((1280-self.bg_tex.get_width())/2)+32
        y = -128
        win.blit(self.bg_tex, [(1280-self.bg_tex.get_width())/2, (720-self.bg_tex.get_height())/2])
        for i in range(10):
            if i % 4 == 0:
                y += 192
                x = ((1280-self.bg_tex.get_width())/2)+32
            if i == 0:
                if self.tiles[i] in self.tiles_unlocked:
                    win.blit(self.tile_images[i], [x-4, y-8])
                else:
                    self.tile_images[i].set_alpha(96)
                    win.blit(self.tile_images[i], [x-4, y-8])
                    self.tile_images[i].set_alpha(255)
                if not ([x-4, y-8] in self.tile_positions):
                    self.tile_positions.append([x-4, y-8])
            elif i == 1:
                if self.tiles[i] in self.tiles_unlocked:
                    win.blit(self.tile_images[i], [x-8, y])
                else:
                    self.tile_images[i].set_alpha(96)
                    win.blit(self.tile_images[i], [x-8, y])
                    self.tile_images[i].set_alpha(255)
                if not ([x-8, y] in self.tile_positions):
                    self.tile_positions.append([x-8, y])
            elif i == 4:
                if self.tiles[i] in self.tiles_unlocked:
                    win.blit(self.tile_images[i], [x-4, y-8])
                else:
                    self.tile_images[i].set_alpha(96)
                    win.blit(self.tile_images[i], [x-4, y-8])
                    self.tile_images[i].set_alpha(255)
                if not ([x-4, y-8] in self.tile_positions):
                    self.tile_positions.append([x-4, y-8])
            elif i == 5:
                if self.tiles[i] in self.tiles_unlocked:
                    win.blit(self.tile_images[i], [x-8, y])
                else:
                    self.tile_images[i].set_alpha(96)
                    win.blit(self.tile_images[i], [x-8, y])
                    self.tile_images[i].set_alpha(255)
                if not ([x-8, y] in self.tile_positions):
                    self.tile_positions.append([x-8, y])
            else:
                if self.tiles[i] in self.tiles_unlocked:
                    win.blit(self.tile_images[i], [x, y])
                else:
                    self.tile_images[i].set_alpha(96)
                    win.blit(self.tile_images[i], [x, y])
                    self.tile_images[i].set_alpha(255)
                if not ([x, y] in self.tile_positions):
                    self.tile_positions.append([x, y])
            x += 192
        for i in range(len(self.tile_masks)):
            if cursor_mask.overlap(self.tile_masks[i], (self.tile_positions[i][0]-pygame.mouse.get_pos()[0], self.tile_positions[i][1]-pygame.mouse.get_pos()[1])) != None:
                win.blit(self.tile_images[i], self.tile_positions[i])
        

        