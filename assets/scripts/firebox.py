from assets.scripts.core_funcs import *
class FireBox:
    def __init__(self, init_pos):
        self.pos = [init_pos[0]+4, init_pos[1]-60]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 64, 128)
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
    def update(self, renderer):
        if (hasattr(renderer, "dt")):
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
                win.blit(self.fire.get([renderer.firebox_frame, 0]), self.pos)
                win.blit(self.firebox.get([renderer.firebox_frame, 0]), self.pos)
                renderer.standing_masks.append([pygame.mask.from_surface(self.firebox.get([renderer.firebox_frame, 0])), self.pos, self])
                self.mask = pygame.mask.from_surface(self.firebox.get([renderer.firebox_frame, 0]))
            if self.is_hovered:
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
                        renderer.add_spike_d([self.pos[0]-4, self.pos[1]+56])
                        renderer.added_spikes += 1
                        renderer.spike_count += 1
                        if renderer.spike_count > renderer.added_spikes:
                            renderer.add_spike_d([self.pos[0]-4, self.pos[1]+56])
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
                        renderer.add_spike_l([self.pos[0]-4, self.pos[1]+56])
                        renderer.added_spikes += 1
                        renderer.spike_count += 1
                        if renderer.spike_count > renderer.added_spikes:
                            renderer.add_spike_l([self.pos[0]-4, self.pos[1]+56])
                            renderer.added_spikes += 1
                        renderer.queue[0].shapeshifting=False
                        renderer.queue_updating = True
                    if renderer.queue[0].tile != 116:
                        renderer.queue.remove(self)
                        del self
                        return 

