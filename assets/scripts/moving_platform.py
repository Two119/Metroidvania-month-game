from assets.scripts.core_funcs import *
class MovingPlatform:
    def __init__(self, length, init_pos, speed, distance):
        self.distance = distance
        self.speed = speed
        self.l = length
        self.pos = init_pos
        self.image = pygame.Surface([(64*length)+16, 96])
        self.cycles = 0
        self.offset = 0
        self.dir = 1
        self.image.set_colorkey((0, 0, 0))
        self.spikes = []
        self.objects = []
    def update(self, renderer):
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
                 
        self.pos[0]+=(self.speed*self.dir)
        self.offset+=(self.speed*self.dir)
        for spike in self.spikes:
            #renderer.levels[renderer.level][int((spike[renderer.attr_dict["pos"]][1])/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))][int((spike[renderer.attr_dict["pos"]][0]-renderer.camera.cam_change[0])/renderer.tile_size[0])] = 117
            if not spike in renderer.spikes:
                renderer.spikes.append(spike)
        if hasattr(renderer.queue[0], "mask"):
                if self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-(self.pos[0]), renderer.queue[0].pos[1]-(self.pos[1]))) == None:
                    pass
                else:
                    renderer.queue[0].pos[0]+=(self.speed*self.dir)
                if self.cycles == 1:
                    for spike in renderer.spikes:
                        spike_y = int((spike[renderer.attr_dict["pos"]][1])/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))
                        if not spike[6]:
                            if self.y - spike_y == 1 and (spike[renderer.attr_dict["pos"]][0] in range(self.pos[0]-32, self.pos[0]+self.image.get_width()-32)):
                                spike.append(1)
                                self.spikes.append(spike)
                        else:
                            if spike_y-self.y == 1 and (spike[renderer.attr_dict["pos"]][0] in range(self.pos[0]-32, self.pos[0]+self.image.get_width()-32)):
                                spike.append(1)
                                self.spikes.append(spike)
                    for obj_ in renderer.queue:
                        if obj_.__class__.__name__ in ["Crusher", "SwingingAxe"]:
                            obj_y = int((obj_.pos[1])/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))
                            if obj_y-self.y == 1 and (obj_.pos[0] in range(self.pos[0]-32, self.pos[0]+self.image.get_width()-32)):
                                self.objects.append(obj_)
                        if obj_.__class__.__name__ == "Coin":
                            obj_y = int((obj_.pos[1])/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))
                            if self.y-obj_y in range(1, 4) and (obj_.pos[0] in range(self.pos[0]-32, self.pos[0]+self.image.get_width()-32)):
                                obj_.shiftable = False
                                self.objects.append(obj_)
                        if obj_.__class__.__name__ == "HiddenSpike":
                            if obj_.ang == 0:
                                if not obj_.down:
                                    obj_y = int((obj_.pos[1])/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))
                                    if self.y-obj_y == 1 and (obj_.pos[0] in range(self.pos[0]-32, self.pos[0]+self.image.get_width()-32)):
                                        obj_.shiftable = False
                                        self.objects.append(obj_)
                                else:
                                    obj_y = int((obj_.pos[1])/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))
                                    if self.y-obj_y == -1 and (obj_.pos[0] in range(self.pos[0]-32, self.pos[0]+self.image.get_width()-32)):
                                        obj_.shiftable = False
                                        self.objects.append(obj_)
                            else:
                                if obj_.ang == 90:
                                    obj_y = int((obj_.pos[1]-28)/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))
                                    if self.y==obj_y and ((obj_.pos[0]-32) in range(self.pos[0]-72, self.pos[0]+self.image.get_width()+72)):
                                        obj_.shiftable = False
                                        self.objects.append(obj_)
                                else:
                                    obj_y = int((obj_.pos[1]-28)/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))
                                    if self.y==obj_y and ((obj_.pos[0]-36) in range(self.pos[0]-72, self.pos[0]+self.image.get_width()+72)):
                                        obj_.shiftable = False
                                        self.objects.append(obj_)
                for spike in self.spikes:
                    spike[renderer.attr_dict["pos"]][0]+=(self.speed*self.dir)
                for obj in self.objects:
                    obj.pos[0]+=(self.speed*self.dir)
        renderer.standing_masks.append([self.mask, self.pos, 122])
        win.blit(self.image, self.pos)
            
