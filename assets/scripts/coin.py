from assets.scripts.core_funcs import *
from assets.scripts.swinging_axe import *
from assets.scripts.firebox import *
from assets.scripts.hidden_spike import *
class Coin:
    def __init__(self, pos : tuple, spritesheet : pygame.Surface, sheet_size : tuple):
        swap_color(spritesheet, [0, 0, 0], [1, 1, 1])
        img = scale_image(spritesheet)
        img.set_colorkey([255, 255, 255])
        self.spritesheet = SpriteSheet(img, [12, 1])
        self.frame = [0, 0]
        self.pos = pos
        self.init_pos = [int(pos[0]/64), int(pos[1]/64)]
        self.delay = 0
        self.collected = False
        self.rect_surf = pygame.Surface((64, 64))
        self.rect_surf.set_alpha(50)
        self.is_hovered = False
        self.shiftable = True
        self.cycles = 0
        if not web:
            pygame.mixer.music.load("assets\Audio\coin.ogg")
            self.sound = (pygame.mixer.Sound("assets\Audio\coin.ogg"))
        else:
            pygame.mixer.music.load("assets/Audio/coin.ogg")
            self.sound = (pygame.mixer.Sound("assets/Audio/coin.ogg"))
        self.level_spike_dicts = {0: 780, 1:-64}
    def update_animation(self, row, delay_wait, renderer):
        if hasattr(renderer, "dt"):
            if (renderer.dt) != 0:
                if round(delay_wait/(renderer.dt)) != 0:
                    self.frame[1] = row
                    self.delay += (1*renderer.dt)
                    if int(self.delay) % round(delay_wait/(renderer.dt)) == 0:
                        self.frame[0] += 1
                    if self.frame[0] > 11:
                        self.frame[0] = 0
    def update_physics(self, renderer):
        self.cycles += 1
        if self.cycles == 1:
            for obj in renderer.queue:
                if obj.__class__.__name__ == 'MovingPlatform':
                    if (obj.pos[1] - self.pos[1]) <= 200 and obj.rect.collidepoint([self.pos[0], obj.pos[1]]):
                        obj.objects.append(self)
                        if renderer.cur_cycle == 0:
                            self.pos[0]+=32
                        self.shiftable = False
                        break
        if hasattr(renderer.queue[0], "mask") and hasattr(renderer.queue[0], "pos"):
            if self.mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-self.pos[0], renderer.queue[0].pos[1]-self.pos[1])):
                if not self.collected:
                    renderer.coin_channel.play(self.sound)
                    renderer.queue[0].coins += 1
                self.collected = True
        if not self.shiftable:
            self.is_hovered = False
        if self.is_hovered:
            if pygame.mouse.get_pressed()[2]:
                    if renderer.level == 0:
                        renderer.levels[renderer.level][self.init_pos[1]-3][self.init_pos[0]] = renderer.queue[0].tile
                    else:
                        renderer.levels[renderer.level][self.init_pos[1]-1][self.init_pos[0]+4] = renderer.queue[0].tile
                    if renderer.queue[0].tile == 117:
                        renderer.add_spike_u(self.pos, True)
                        renderer.added_spikes += 1
                        renderer.spike_count += 1
                        if renderer.spike_count > renderer.added_spikes:
                            renderer.add_spike_u(self.pos, True)
                            renderer.added_spikes += 1
                        renderer.queue[0].shapeshifting=False
                        renderer.queue_updating = True
                    if renderer.queue[0].tile == 129:
                        renderer.add_spike_d(self.pos, True)
                        renderer.added_spikes += 1
                        renderer.spike_count += 1
                        if renderer.spike_count > renderer.added_spikes:
                            renderer.add_spike_d(self.pos, True)
                            renderer.added_spikes += 1
                        renderer.queue[0].shapeshifting=False
                        renderer.queue_updating = True
                    if renderer.queue[0].tile == 138:
                        renderer.add_spike_r(self.pos, True)
                        renderer.added_spikes += 1
                        renderer.spike_count += 1
                        if renderer.spike_count > renderer.added_spikes:
                            renderer.add_spike_r(self.pos, True)
                            renderer.added_spikes += 1
                        renderer.queue[0].shapeshifting=False
                        renderer.queue_updating = True
                    if renderer.queue[0].tile == 139:
                        renderer.add_spike_l(self.pos, True)
                        renderer.added_spikes += 1
                        renderer.spike_count += 1
                        if renderer.spike_count > renderer.added_spikes:
                            renderer.add_spike_l(self.pos, True)
                            renderer.added_spikes += 1
                        renderer.queue[0].shapeshifting=False
                        renderer.queue_updating = True
                    if renderer.queue[0].tile == 118:
                        if True:
                            renderer.queue.append(HiddenSpike(renderer.spike_image, [4, 1], [self.init_pos[0]*64+renderer.camera.cam_change[0], self.init_pos[1]*64+renderer.camera.cam_change[1]-64-self.level_spike_dicts[renderer.level]-4]))
                            renderer.added_spikes_h += 1
                        renderer.spike_h_count += 1
                        if renderer.spike_h_count > renderer.added_spikes_h:
                            renderer.queue.append(HiddenSpike(renderer.spike_image, [4, 1], [self.init_pos[0]*64+renderer.camera.cam_change[0], self.init_pos[1]*64+renderer.camera.cam_change[1]-64-self.level_spike_dicts[renderer.level]-4]))
                            renderer.added_spikes_h += 1
                    if renderer.queue[0].tile == 135:
                        if True:
                            renderer.queue.append(HiddenSpike(renderer.spike_image, [4, 1], [self.init_pos[0]*64+renderer.camera.cam_change[0], self.init_pos[1]*64+renderer.camera.cam_change[1]-64-self.level_spike_dicts[renderer.level]+4], True))
                            renderer.added_spikes_h += 1
                        renderer.spike_h_count += 1
                        if renderer.spike_h_count > renderer.added_spikes_h:
                            renderer.queue.append(HiddenSpike(renderer.spike_image, [4, 1], [self.init_pos[0]*64+renderer.camera.cam_change[0], self.init_pos[1]*64+renderer.camera.cam_change[1]-64-self.level_spike_dicts[renderer.level]+4], True))
                            renderer.added_spikes_h += 1
                    if renderer.queue[0].tile == 136:
                        if True:
                            renderer.queue.append(HiddenSpike(renderer.spike_image, [4, 1], [self.init_pos[0]*64+renderer.camera.cam_change[0]-12, self.init_pos[1]*64+renderer.camera.cam_change[1]-64-self.level_spike_dicts[renderer.level]-8], False, 90))
                            renderer.added_spikes_h += 1
                        renderer.spike_h_count += 1
                        if renderer.spike_h_count > renderer.added_spikes_h:
                            renderer.queue.append(HiddenSpike(renderer.spike_image, [4, 1], [self.init_pos[0]*64+renderer.camera.cam_change[0]-12, self.init_pos[1]*64+renderer.camera.cam_change[1]-64-self.level_spike_dicts[renderer.level]-8], False, 90))
                            renderer.added_spikes_h += 1
                    if renderer.queue[0].tile == 137:
                        renderer.queue.append(HiddenSpike(renderer.spike_image, [4, 1], [self.init_pos[0]*64+renderer.camera.cam_change[0]-4, self.init_pos[1]*64+renderer.camera.cam_change[1]-64-self.level_spike_dicts[renderer.level]-8], False, -90))
                        renderer.added_spikes_h += 1
                        renderer.spike_h_count += 1
                        if renderer.spike_h_count > renderer.added_spikes_h:
                            renderer.queue.append(HiddenSpike(renderer.spike_image, [4, 1], [self.init_pos[0]*64+renderer.camera.cam_change[0]-4, self.init_pos[1]*64+renderer.camera.cam_change[1]-64-self.level_spike_dicts[renderer.level]-8], False, -90))
                            renderer.added_spikes_h += 1
                    #[self.init_pos[0]*64+renderer.camera.cam_change[0], self.init_pos[1]*64+renderer.camera.cam_change[1]-64]
                    if renderer.queue[0].tile == 121:
                        renderer.queue.append(SwingingAxe(self.pos))
                    if renderer.queue[0].tile == 116:
                        renderer.queue.append(FireBox(self.pos, True))
                    renderer.queue = [ob for ob in renderer.queue if ob != self]
                    del self
                    return
            pygame.draw.rect(self.rect_surf, (255, 0, 0), pygame.Rect(0, 0, 64, 64))
            win.blit(self.rect_surf, [self.pos[0]+4, self.pos[1]+4])
    def update(self, renderer):
        if not self.collected:
            self.update_animation(0, 10, renderer)
            self.mask = pygame.mask.from_surface(self.spritesheet.get(self.frame))
            win.blit(self.spritesheet.get(self.frame), self.pos)
            self.update_physics(renderer)
        else:
            return
        