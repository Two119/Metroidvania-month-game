from assets.scripts.core_funcs import *
from assets.scripts.swinging_axe import *
from assets.scripts.firebox import *
class HiddenSpike:
    def __init__(self, spritesheet, sheet_size, pos, down=False, ang=0):
        self.spritesheet = SpriteSheet(pygame.transform.flip(scale_image(spritesheet, 4).convert(), False, down), sheet_size, [236, 28, 36])
        self.frame = [0, 0]
        self.orig_pos = [pos[0]*1, pos[1]*1]
        if ang==0:
            self.pos = pos
        else:
            if ang==-90:
                self.pos = [pos[0]+((16*ang)/-90)+((62*ang)/-90)-int(self.spritesheet.get(self.frame).get_width()/2), pos[1]+72-int(self.spritesheet.get(self.frame).get_height()/2)]
            else:
                self.pos = [pos[0]+((16*ang)/90)+((62*ang)/90)-int(self.spritesheet.get(self.frame).get_width()/2), pos[1]+72-int(self.spritesheet.get(self.frame).get_height()/2)]
        self.down = down
        self.ang = ang
        self.delay = 0
        self.just_spawned = True
        self.rect_surf = pygame.Surface((64, 64))
        self.rect_surf.set_alpha(50)
        self.is_hovered = False
        self.played = False
        self.shiftable = True
        self.i = 0
        for img in self.spritesheet.sheet[0]:
            self.spritesheet.sheet[0][self.i] = pygame.transform.rotate(img, self.ang)
            self.i+=1
    def spawn_animation(self, row, delay_wait, renderer):
        if (renderer.clock.get_fps()) != 0 and self.just_spawned:
            self.frame[1] = row
            self.delay += 1
            if round(delay_wait/renderer.dt) != 0:
                if self.delay % round(delay_wait/renderer.dt) == 0:
                    self.frame[0] += 1
            if self.frame[0] > 3:
                self.frame[0] = 3
                self.just_spawned = False
        if not self.played:
                if not web:
                    renderer.coin_channel.play(pygame.mixer.Sound("assets\Audio\spike_spawn.ogg"))
                else:
                    renderer.coin_channel.play(pygame.mixer.Sound("assets/Audio/spike_spawn.ogg"))
        self.played = True
        self.mask = pygame.mask.from_surface(self.spritesheet.get(self.frame))
    def update(self, renderer):
        if hasattr(renderer, "dt") and hasattr(renderer.queue[0], "rect"):
            self.rect = self.spritesheet.get(self.frame).get_rect(topleft=self.pos)
            self.rect.x += 10
            self.rect.width -= 10
            if self.rect.colliderect(renderer.queue[0].rect) and self.just_spawned == None:
                self.just_spawned = True
            if self.just_spawned == None:
                for enemy in renderer.enemies:
                    e = renderer.queue[enemy]
                    if (e.__class__.__name__ == "EnemySwordsman" or e.__class__.__name__ == "EnemyWizard") and hasattr(e, "rect"):
                        if self.rect.colliderect(e.rect):
                            self.just_spawned = True
            if not self.just_spawned == None:
                if self.just_spawned:
                    self.spawn_animation(0, 4, renderer)
            else:
                pygame.draw.rect(win, [255, 0, 0], pygame.Rect(self.pos[0]+4, self.pos[1]+70, 64, 2))
            if hasattr(self, "mask") and hasattr(renderer.queue[0], "mask"):
                if self.ang == 0:
                    if self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-self.pos[0], renderer.queue[0].pos[1]-self.pos[1])) == None:
                        pass
                    else:
                        renderer.queue[0].is_alive = False
                        #renderer.queue = [ob for ob in renderer.queue if ob != self]
                        #reset(renderer.queue[0], renderer)
                        renderer.queue[0].deaths += 1
                        #del self
                        #return
                    for enemy in renderer.enemies:
                        e = renderer.queue[enemy]
                        if (e.__class__.__name__ == "EnemySwordsman" or e.__class__.__name__ == "EnemyWizard"):
                            if self.mask.overlap(e.mask, (e.pos[0]-self.pos[0], e.pos[1]-self.pos[1])) == None:
                                pass
                            else:
                                e.is_alive = False
                                #renderer.queue = [ob for ob in renderer.queue if ob != self]
                                #del self
                                #return
                else:
                    if self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-(self.pos[0]-int(self.spritesheet.get(self.frame).get_width()/2)), renderer.queue[0].pos[1]-(self.pos[1]-int(self.spritesheet.get(self.frame).get_height()/2)))) == None:
                        pass
                    else:
                        renderer.queue[0].is_alive = False
                        #renderer.queue = [ob for ob in renderer.queue if ob != self]
                        #reset(renderer.queue[0], renderer)
                        renderer.queue[0].deaths += 1
                        #del self
                        #return
                    for enemy in renderer.enemies:
                        e = renderer.queue[enemy]
                        if (e.__class__.__name__ == "EnemySwordsman" or e.__class__.__name__ == "EnemyWizard"):
                            if self.mask.overlap(e.mask, (e.pos[0]-(self.pos[0]-int(self.spritesheet.get(self.frame).get_width()/2)), e.pos[1]-(self.pos[1]-int(self.spritesheet.get(self.frame).get_height()/2)))) == None:
                                pass
                            else:
                                e.is_alive = False
                                
            if not self.just_spawned == None:
                if self.ang == 0:
                    win.blit(self.spritesheet.get(self.frame), self.pos)
                else:
                    win.blit(self.spritesheet.get(self.frame), [self.pos[0]-int(self.spritesheet.get(self.frame).get_width()/2), self.pos[1]-int(self.spritesheet.get(self.frame).get_height()/2)])
            if not self.shiftable:
                self.is_hovered = False
            if self.is_hovered and not(self.just_spawned):
                if not self.ang == 0:
                    if self.ang == 90:
                        if pygame.mouse.get_pressed()[2]:
                            if renderer.queue[0].tile == 117:
                                renderer.add_spike_u([self.pos[0]-4, self.pos[1]+52])
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_u([self.pos[0]-4, self.pos[1]+52])
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 129:
                                renderer.add_spike_d(self.orig_pos)
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_d(self.orig_pos)
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 138:
                                renderer.add_spike_r([self.pos[0]-4, self.pos[1]+52])
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_r([self.pos[0]-4, self.pos[1]+52])
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 139:
                                renderer.add_spike_l(self.orig_pos)
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_l(self.orig_pos)
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 121:
                                renderer.queue.append(SwingingAxe(self.orig_pos))
                            if renderer.queue[0].tile == 116:
                                renderer.queue.append(FireBox(self.orig_pos))
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            renderer.levels[renderer.level][int((self.pos[1]-28)/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))][int(((self.pos[0]-32)-renderer.camera.cam_change[0])/renderer.tile_size[0])] = renderer.queue[0].tile
                            renderer.queue = [ob for ob in renderer.queue if ob != self]
                            return
                        pygame.draw.rect(self.rect_surf, (255, 0, 0), pygame.Rect(0, 0, 64, 64))
                        win.blit(self.rect_surf, [self.pos[0]-32, self.pos[1]-28])
                    else:
                        if pygame.mouse.get_pressed()[2]:
                            if renderer.queue[0].tile == 117:
                                renderer.add_spike_u([self.pos[0]-4, self.pos[1]+52])
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_u([self.pos[0]-4, self.pos[1]+52])
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 129:
                                renderer.add_spike_d(self.orig_pos)
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_d(self.orig_pos)
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 138:
                                renderer.add_spike_r([self.pos[0]-4, self.pos[1]+52])
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_r([self.pos[0]-4, self.pos[1]+52])
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 139:
                                renderer.add_spike_l(self.orig_pos)
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_l(self.orig_pos)
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 121:
                                renderer.queue.append(SwingingAxe(self.orig_pos))
                            if renderer.queue[0].tile == 116:
                                renderer.queue.append(FireBox(self.orig_pos))
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            renderer.levels[renderer.level][int((self.pos[1]-28)/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))][int(((self.pos[0]-36)-renderer.camera.cam_change[0])/renderer.tile_size[0])] = renderer.queue[0].tile
                            renderer.queue = [ob for ob in renderer.queue if ob != self]
                            return
                        pygame.draw.rect(self.rect_surf, (255, 0, 0), pygame.Rect(0, 0, 64, 64))
                        win.blit(self.rect_surf, [self.pos[0]-36, self.pos[1]-28])
                else:
                    if pygame.mouse.get_pressed()[2]:
                        if renderer.queue[0].tile == 117:
                            renderer.add_spike_u([self.pos[0]-4, self.pos[1]+52])
                            renderer.added_spikes += 1
                            renderer.spike_count += 1
                            if renderer.spike_count > renderer.added_spikes:
                                renderer.add_spike_u([self.pos[0]-4, self.pos[1]+52])
                                renderer.added_spikes += 1
                            renderer.queue[0].shapeshifting=False
                            renderer.queue_updating = True
                        if renderer.queue[0].tile == 129:
                            renderer.add_spike_d(self.orig_pos)
                            renderer.added_spikes += 1
                            renderer.spike_count += 1
                            if renderer.spike_count > renderer.added_spikes:
                                renderer.add_spike_d(self.orig_pos)
                                renderer.added_spikes += 1
                            renderer.queue[0].shapeshifting=False
                            renderer.queue_updating = True
                        if renderer.queue[0].tile == 138:
                            renderer.add_spike_r([self.pos[0]-4, self.pos[1]+52])
                            renderer.added_spikes += 1
                            renderer.spike_count += 1
                            if renderer.spike_count > renderer.added_spikes:
                                renderer.add_spike_r([self.pos[0]-4, self.pos[1]+52])
                                renderer.added_spikes += 1
                            renderer.queue[0].shapeshifting=False
                            renderer.queue_updating = True
                        if renderer.queue[0].tile == 139:
                            renderer.add_spike_l(self.orig_pos)
                            renderer.added_spikes += 1
                            renderer.spike_count += 1
                            if renderer.spike_count > renderer.added_spikes:
                                renderer.add_spike_l(self.orig_pos)
                                renderer.added_spikes += 1
                            renderer.queue[0].shapeshifting=False
                            renderer.queue_updating = True
                        if renderer.queue[0].tile == 121:
                            renderer.queue.append(SwingingAxe(self.orig_pos))
                        if renderer.queue[0].tile == 116:
                            renderer.queue.append(FireBox(self.orig_pos))
                            renderer.queue[0].shapeshifting=False
                            renderer.queue_updating = True
                        renderer.levels[renderer.level][int((self.pos[1]+4)/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))][int(((self.pos[0]+8)-renderer.camera.cam_change[0])/renderer.tile_size[0])] = renderer.queue[0].tile
                        renderer.queue = [ob for ob in renderer.queue if ob != self]
                        return
                    pygame.draw.rect(self.rect_surf, (255, 0, 0), pygame.Rect(0, 0, 64, 64))
                    win.blit(self.rect_surf, [self.pos[0]+8, self.pos[1]+8])
            
            