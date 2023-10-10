from assets.scripts.core_funcs import *
class FallingBlock:
    def __init__(self, position, main_img:pygame.Surface, final_tile, tile_num, length=5):
        self.gravity = 0.24
        self.final_tile = final_tile
        self.vel = 0
        self.pos = position
        self.falling = False
        self.about_to_fall = False
        self.standing = False
        self.l=length
        self.tile_num = tile_num
        self.falling_rect = pygame.Rect(self.pos[0], self.pos[1], 64, 64*5)
        self.main_img = main_img.copy()
        self.spikes = scale_image(pygame.image.load("assets/Spritesheets/falling_block_spikes.png").convert())
        swap_color(self.spikes, [87, 114, 119], [254, 254, 254])
        swap_color(self.spikes, [129, 151, 150], [195, 195, 195])
        swap_color(self.spikes, [168, 181, 178], [195, 195, 195])
        self.spikes.set_colorkey([255, 255, 255])
        self.dust_sheet = SpriteSheet(scale_image(pygame.image.load("assets/Spritesheets/smoke.png").convert()), [7, 1], [255, 255, 255])
        self.dust_frame = 0
        self.dust = False

        self.rumble_range = [-4, 0, 4]
        self.fall_time = time.time()
        self.offset = [randint(0, 2), randint(0, 2)]
        self.mask = pygame.mask.from_surface(self.main_img)
        self.spike_mask = pygame.mask.from_surface(self.spikes)
        self.displacement = 0
        self.is_hovered = False
        self.time = time.time()
        self.dust_time = time.time()
    def update(self, renderer):

        #self.standing = False
        self.falling_rect = pygame.Rect(self.pos[0]+4, self.pos[1]+4, 64, 64*self.l)
        #pygame.draw.rect(win, [255, 0, 0], self.falling_rect)
        if hasattr(renderer.queue[0], "rect"):
            if self.falling_rect.colliderect(renderer.queue[0].rect) and not self.about_to_fall:
                self.about_to_fall = True
                self.fall_time = time.time()
            pos = [self.pos[0]+4, self.pos[1]+64]
            for obj in renderer.queue:
                if obj.__class__.__name__ == "EnemySwordsman" or obj.__class__.__name__ == "EnemyWizard":
                    if hasattr(obj, "rect"):
                        if self.spike_mask.overlap(obj.mask, (obj.pos[0]-pos[0], obj.pos[1]-pos[1])) != None:
                            obj.is_alive = False
                        if obj.rect.colliderect(self.falling_rect):
                            self.about_to_fall = True
                            self.fall_time = time.time()
                            self.time = time.time()
                            self.offset = [randint(0, 2), randint(0, 2)]
            if not self.about_to_fall:
                win.blit(self.main_img, self.pos)
                win.blit(self.spikes, [self.pos[0]+4, self.pos[1]+64])
            else:
                if not self.falling:
                    if round(time.time())-round(self.fall_time) == 1:
                        self.falling = True
                    if time.time() - self.time >= 0.05:
                        self.offset = [randint(0, 2), randint(0, 2)]
                        self.time = time.time()
                    win.blit(self.main_img, [self.pos[0]+self.rumble_range[self.offset[0]], self.pos[1]+self.rumble_range[self.offset[1]]])
                    win.blit(self.spikes, [self.pos[0]+4+self.rumble_range[self.offset[0]], self.pos[1]+64+self.rumble_range[self.offset[1]]])
                    pos = [self.pos[0]+4+self.rumble_range[self.offset[0]], self.pos[1]+64+self.rumble_range[self.offset[1]]]
                    if self.spike_mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-pos[0], renderer.queue[0].pos[1]-pos[1])) != None:
                        renderer.queue[0].is_alive = False
                        renderer.queue[0].deaths += 1
                    renderer.standing_masks.append([self.mask, [self.pos[0]+self.rumble_range[self.offset[0]], self.pos[1]+self.rumble_range[self.offset[1]]], self])
                else:
                    for double_list in renderer.standing_masks:
                        if (self.mask.overlap(double_list[0], (double_list[1][0]-self.pos[0], double_list[1][1]-self.pos[1])) != None) and double_list[2] != self:
                            if not self.standing:
                                self.dust = True
                                self.dust_time = time.time()
                            self.standing = True 
                            self.pos[1]=double_list[1][1]-64                           
                    if not self.standing:
                        self.vel += (self.gravity*renderer.dt)
                        self.displacement += self.vel
                        self.pos[1] += self.vel
                        win.blit(self.main_img, self.pos)
                        win.blit(self.spikes, [self.pos[0]+4, self.pos[1]+64])
                        pos = [self.pos[0]+4, self.pos[1]+64]
                        if self.spike_mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-pos[0], renderer.queue[0].pos[1]-pos[1])) != None:
                            renderer.queue[0].is_alive = False
                            renderer.queue[0].deaths += 1
                    else:   
                        renderer.standing_masks.append([self.mask, self.pos, self, [self.tile_num[0], self.tile_num[1]+round(self.displacement/64)]])
                        win.blit(self.main_img, self.pos)
                        self.vel = 0
                        
            if self.dust:
                
                if time.time() - self.dust_time >= 0.2:
                    self.dust_frame += 1
                    self.dust_time = time.time()
                if self.dust_frame > 6:
                    self.dust_frame = 0
                    self.dust = False
                    left_rect = pygame.Rect(self.pos[0]+4, self.pos[1]+12, 1, 56)
                    right_rect = pygame.Rect(self.pos[0]+68, self.pos[1]+12, 1, 56)
                    down_rect = pygame.Rect(self.pos[0]+4, self.pos[1]+68, 64, 1)
                    renderer.side_rects.append([left_rect, -1])
                    renderer.side_rects.append([right_rect, 1])
                    renderer.side_rects.append([down_rect, 2])
                    return
                win.blit(self.dust_sheet.get([self.dust_frame, 0]), [self.pos[0]-32, self.pos[1]+64-self.dust_sheet.size[1]+4])
            left_rect = pygame.Rect(self.pos[0]+4, self.pos[1]+12, 1, 56)
            right_rect = pygame.Rect(self.pos[0]+68, self.pos[1]+12, 1, 56)
            down_rect = pygame.Rect(self.pos[0]+4, self.pos[1]+68, 64, 1)
            renderer.side_rects.append([left_rect, -1])
            renderer.side_rects.append([right_rect, 1])
            renderer.side_rects.append([down_rect, 2])
            #pygame.draw.rect(win, [255, 0, 0], left_rect)
            #pygame.draw.rect(win, [255, 0, 0], right_rect)
            #pygame.draw.rect(win, [255, 0, 0], down_rect)
            
                    
                    