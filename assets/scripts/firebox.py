from assets.scripts.core_funcs import *
class FireBox:
    def __init__(self, init_pos, shifted=False, spike_shifted=False):
        self.shifted = shifted
        self.spike_shifted = spike_shifted
        self.pos = [init_pos[0]+4, init_pos[1]-60]
        self.init_tile_pos = [int(init_pos[0]/64), int(init_pos[1]/64)]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 64, 128)
        self.level_spike_dicts = {0: 524, 1:-64}
        if web:
            fb = pygame.image.load("assets/Spritesheets/FireBox.png")
            swap_color(fb, [255, 255, 255], [47, 54, 92])
            f = pygame.image.load("assets/Spritesheets/fire.png")
            swap_color(f, [255, 255, 255], [44, 50, 85])
            fb.set_colorkey([44, 50, 85])
            f = scale_image(f)
            fb = scale_image(fb)
            self.firebox = SpriteSheet(fb, [13, 1], [47, 54, 92])
            self.fire = SpriteSheet(f, [13, 1], [44, 50, 85])
            self.sfx = pygame.mixer.Sound("assets/Audio/fire.ogg")
        else:
            fb = pygame.image.load("assets\\Spritesheets\\FireBox.png")
            swap_color(fb, [255, 255, 255], [47, 54, 92])
            f = pygame.image.load("assets\\Spritesheets\\fire.png")
            swap_color(f, [255, 255, 255], [44, 50, 85])
            fb.set_colorkey([44, 50, 85])
            f = scale_image(f)
            fb = scale_image(fb)
            self.firebox = SpriteSheet(fb, [13, 1], [47, 54, 92])
            self.fire = SpriteSheet(f, [13, 1], [44, 50, 85])
            self.sfx = pygame.mixer.Sound("assets\\Audio\\fire.ogg")
        self.mask = pygame.mask.from_surface(self.fire.get([0, 0]))
        self.delay = 0
        self.is_hovered = False
        self.cycles = 0
        self.on_platform = False
    def append_rects(self, renderer):
        self.rects = [pygame.Rect(self.pos[0], self.pos[1]+72, 1, 56), pygame.Rect(self.pos[0]+64, self.pos[1]+72, 1, 56)]
        renderer.side_rects.append([self.rects[0], 1, 116])
        renderer.side_rects.append([self.rects[1], 1, 116])
        pygame.draw.rect(win, [255, 0, 0], self.rects[0])
        pygame.draw.rect(win, [255, 0, 0], self.rects[1])
    def update(self, renderer):
        self.cycles += 1
        if self.cycles == 1:
            for obj in renderer.queue:
                if obj.__class__.__name__ == "MovingPlatform":
                    if obj.rect.collidepoint([self.pos[0], self.pos[1]+64]):
                        obj.objects.append(self)
                        self.on_platform = True
                        break
        if (hasattr(renderer, "dt")):
            if renderer.camera.bigger_window_rect.collidepoint(self.pos):
                if renderer.dt != 0:
                    self.rect = pygame.Rect(self.pos[0], self.pos[1], 64, 128)
                    self.mask = pygame.mask.from_surface(self.fire.get([renderer.firebox_frame, 0]))
                    if (hasattr(renderer.queue[0], "rect")):
                        if (self.rect.colliderect(renderer.queue[0].rect)):
                            if (self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-self.pos[0], renderer.queue[0].pos[1]-(self.pos[1])))!=None):
                                renderer.queue[0].is_alive = False
                                renderer.queue[0].deaths += 1
                    for enemy in renderer.enemies:
                        if (hasattr(renderer.queue[enemy], "rect")):
                            if (self.rect.colliderect(renderer.queue[enemy].rect)):
                                if (self.mask.overlap(renderer.queue[enemy].mask, (renderer.queue[enemy].pos[0]-self.pos[0], renderer.queue[enemy].pos[1]-(self.pos[1])))!=None):
                                    renderer.queue[enemy].is_alive = False
                    if renderer.firebox_frame in range(4, 9):
                        if not renderer.firebox_channel.get_busy():
                            renderer.firebox_channel.play(self.sfx)
                    else:
                        renderer.firebox_channel.stop()
                    for rect in self.rects:
                        if hasattr(renderer.queue[0], "rect"):
                            if rect.colliderect(renderer.queue[0].rect):
                                renderer.queue[0].pos[0] -= renderer.queue[0].vel[0]
                                if renderer.queue[0].jumping:
                                    renderer.queue[0].vel[1] = 0
                                    renderer.queue[0].jumping = False
                    win.blit(self.fire.get([renderer.firebox_frame, 0]), self.pos)
                    win.blit(self.firebox.get([renderer.firebox_frame, 0]), self.pos)
                    renderer.standing_masks.append([pygame.mask.from_surface(self.firebox.get([renderer.firebox_frame, 0])), self.pos, self, self.init_tile_pos])
                    self.mask = pygame.mask.from_surface(self.firebox.get([renderer.firebox_frame, 0]))
                if self.is_hovered:
                    if pygame.mouse.get_pressed()[2]:
                        renderer.queue[0].shapeshifts -= 1
                        if renderer.level != 0:
                            if not self.shifted:
                                if renderer.queue[0].tile == 117:
                                    renderer.add_spike_u([self.init_tile_pos[0]*64+renderer.camera.cam_change[0], self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-4], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_u([self.init_tile_pos[0]*64+renderer.camera.cam_change[0], self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-4], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                                if renderer.queue[0].tile == 129:
                                    renderer.add_spike_d([self.init_tile_pos[0]*64+renderer.camera.cam_change[0], self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-1], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_d([self.init_tile_pos[0]*64+renderer.camera.cam_change[0], self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-1], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                                if renderer.queue[0].tile == 138:
                                    renderer.add_spike_r([self.init_tile_pos[0]*64+renderer.camera.cam_change[0]+1, self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-4], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_r([self.init_tile_pos[0]*64+renderer.camera.cam_change[0]+1, self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-4], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                                if renderer.queue[0].tile == 139:
                                    renderer.add_spike_l([self.init_tile_pos[0]*64+renderer.camera.cam_change[0]-1, self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-1], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_l([self.init_tile_pos[0]*64+renderer.camera.cam_change[0]-1, self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-1], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                            elif self.spike_shifted:
                                if renderer.queue[0].tile == 117:
                                    renderer.add_spike_u([(self.init_tile_pos[0])*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_u([(self.init_tile_pos[0])*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                                if renderer.queue[0].tile == 129:
                                    renderer.add_spike_d([(self.init_tile_pos[0])*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_d([(self.init_tile_pos[0])*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                                if renderer.queue[0].tile == 138:
                                    renderer.add_spike_r([(self.init_tile_pos[0])*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_r([(self.init_tile_pos[0])*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                                if renderer.queue[0].tile == 139:
                                    renderer.add_spike_l([(self.init_tile_pos[0])*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_l([(self.init_tile_pos[0])*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                            else:
                                if renderer.queue[0].tile == 117:
                                    renderer.add_spike_u([(self.init_tile_pos[0]+1)*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_u([(self.init_tile_pos[0]+1)*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                                if renderer.queue[0].tile == 129:
                                    renderer.add_spike_d([(self.init_tile_pos[0]+1)*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_d([(self.init_tile_pos[0]+1)*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                                if renderer.queue[0].tile == 138:
                                    renderer.add_spike_r([(self.init_tile_pos[0]+1)*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_r([(self.init_tile_pos[0]+1)*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                                if renderer.queue[0].tile == 139:
                                    renderer.add_spike_l([(self.init_tile_pos[0]+1)*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                    renderer.added_spikes += 1
                                    renderer.spike_count += 1
                                    if renderer.spike_count > renderer.added_spikes:
                                        renderer.add_spike_l([(self.init_tile_pos[0]+1)*64, self.init_tile_pos[1]*64-self.level_spike_dicts[renderer.level]-24], True)
                                        renderer.added_spikes += 1
                                    renderer.queue[0].shapeshifting=False
                                    renderer.queue_updating = True
                        else:
                            if renderer.queue[0].tile == 117:
                                renderer.add_spike_u([self.init_tile_pos[0]*64+renderer.camera.cam_change[0], self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-4], True)
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_u([self.init_tile_pos[0]*64+renderer.camera.cam_change[0], self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-4], True)
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 129:
                                renderer.add_spike_d([self.init_tile_pos[0]*64+renderer.camera.cam_change[0], self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-1], True)
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_d([self.init_tile_pos[0]*64+renderer.camera.cam_change[0], self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-1], True)
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 138:
                                renderer.add_spike_r([self.init_tile_pos[0]*64+renderer.camera.cam_change[0]+1, self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-4], True)
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_r([self.init_tile_pos[0]*64+renderer.camera.cam_change[0]+1, self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-4], True)
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                            if renderer.queue[0].tile == 139:
                                renderer.add_spike_l([self.init_tile_pos[0]*64+renderer.camera.cam_change[0]-1, self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-1], True)
                                renderer.added_spikes += 1
                                renderer.spike_count += 1
                                if renderer.spike_count > renderer.added_spikes:
                                    renderer.add_spike_l([self.init_tile_pos[0]*64+renderer.camera.cam_change[0]-1, self.init_tile_pos[1]*64+renderer.camera.cam_change[1]-self.level_spike_dicts[renderer.level]-1], True)
                                    renderer.added_spikes += 1
                                renderer.queue[0].shapeshifting=False
                                renderer.queue_updating = True
                        if renderer.queue[0].tile != 116:
                            renderer.queue.remove(self)
                            del self
                            return 

