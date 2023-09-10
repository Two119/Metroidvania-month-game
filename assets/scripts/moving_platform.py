from assets.scripts.core_funcs import *
class MovingPlatform:
    def __init__(self, length, init_pos, speed, distance):
        self.distance = distance
        self.speed = speed
        self.l = length
        self.pos = init_pos
        self.init_tile_pos = [int(init_pos[0]/64), int(init_pos[1]/64)]
        self.image = pygame.Surface([(64*length)+16, 96])
        self.cycles = 0
        self.offset = 0
        self.dir = 1
        self.image.set_colorkey((0, 0, 0))
        self.spikes = []
        self.objects = []
        self.rect = pygame.Rect(self.pos[0]-72, self.pos[1]-64, ((self.l+1)*64)+72, 192)
    def update(self, renderer):
        if hasattr(renderer, "dt"):
            self.cycles += 1
            if self.cycles == 1:
                self.image.blit(renderer.images[63], (0, 0))
                x = 64
                for i in range(1, self.l-1):
                    x = 64*i
                    self.image.blit(renderer.images[6], (x, 0))
                self.image.blit(renderer.images[7], (x+64, 0))
                self.mask = pygame.mask.from_surface(self.image)
                self.y = int((self.pos[1])/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))
            if self.dir == 1:
                if self.offset <= self.distance:
                    pass
                else:
                    self.dir = -1
                    self.offset = 0
                    
            else:
                if (0-self.offset) <= self.distance:
                    pass
                else:
                    self.dir = 1
                    self.offset = 0
                    
            self.pos[0]+=round(self.speed*self.dir*renderer.dt)
            self.offset+=round(self.speed*self.dir*renderer.dt)
            for spike in self.spikes:
                #renderer.levels[renderer.level][int((spike[renderer.attr_dict["pos"]][1])/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))][int((spike[renderer.attr_dict["pos"]][0]-renderer.camera.cam_change[0])/renderer.tile_size[0])] = 117
                if not spike in renderer.spikes:
                    renderer.spikes.append(spike)
            if hasattr(renderer.queue[0], "mask"):
                    if self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-(self.pos[0]), renderer.queue[0].pos[1]-(self.pos[1]))) == None:
                        pass
                    else:
                        renderer.queue[0].pos[0]+=round(self.speed*self.dir*renderer.dt)
                    
                    for spike in self.spikes:
                        spike[renderer.attr_dict["pos"]][0]+=round(self.speed*self.dir*renderer.dt)
                    for obj in self.objects:
                        obj.pos[0]+=round(self.speed*self.dir*renderer.dt)
            renderer.standing_masks.append([self.mask, self.pos, 122, self.init_tile_pos])
            self.rect = pygame.Rect(self.pos[0]-72, self.pos[1]-64, ((self.l+1)*64)+72, 192)
            #pygame.draw.rect(win, [255, 0, 0], self.rect)
            win.blit(self.image, self.pos)
            
            
