from assets.scripts.core_funcs import *
from assets.scripts.coin import *
from assets.scripts.crusher import *
from assets.scripts.hidden_spike import *
from assets.scripts.spikeball import *
from assets.scripts.button import *
from assets.scripts.moving_platform import *
from assets.scripts.swinging_axe import *
from assets.scripts.firebox import *
from assets.scripts.enemy import *
from assets.scripts.bullet_manager import *
class LevelRenderer:
    def __init__(self, levels : tuple, tilesheet : pygame.Surface, tilesheet_size : tuple, spike_images : tuple, colors : tuple, background : pygame.Surface, coin_image):
        final_color = [30, 30, 30]
        swap_color(background, [255, 255, 255], final_color)
        swap_color(background, [0, 0, 0], final_color)
        tilesheet.set_colorkey([255, 255, 255])
        self.spikes = []
        if not web:
            self.spike_image = pygame.image.load("assets\Spritesheets\spikes.png").convert()
            self.button_sprites = SpriteSheet(scale_image(pygame.image.load("assets\Spritesheets\\buttons.png").convert()), [2, 1], [255, 255, 255])
        else:
            self.spike_image = pygame.image.load("assets/Spritesheets/spikes.png").convert()
            self.button_sprites = SpriteSheet(scale_image(pygame.image.load("assets/Spritesheets/buttons.png").convert()), [2, 1], [255, 255, 255])
        self.spikesheet = SpriteSheet(scale_image(self.spike_image, 4).convert(), [4, 1], [236, 28, 36])
        self.attr_dict = {"pos":0, "delay":1, "just_spawned":2, "rect_surf":3, "is_hovered":4, "played":5}
        self.frame = [0, 0]
        self.button = None
        #self.pos = pos
        #self.delay = 0
        self.def_frame = 60
        self.enemies = []
        self.surf = pygame.Surface(win_size)
        pygame.draw.rect(self.surf, (0, 0, 0), pygame.Rect(0, 0, win_size[0], win_size[1]))
        self.surf.set_alpha(50)
        #self.just_spawned = True
        self.played = False
        self.rect_surf = pygame.Surface((64, 64))
        self.rect_surf.set_alpha(75)
        pygame.draw.rect(self.rect_surf, (255, 0, 0), pygame.Rect(0, 0, 64, 64))
        self.levels = levels
        self.level = 0
        self.coin_img = coin_image.convert()
        self.changed = []
        self.background = scale_image(background, win_size[0]/background.get_width())
        self.background.convert()
        self.colorkeys = colors
        self.tilesheet = SpriteSheet(tilesheet, tilesheet_size)
        self.images = []
        self.tilesheet_size = tilesheet_size
        for i in range(self.tilesheet_size[1]):
            for j in range(self.tilesheet_size[0]):
                img = scale_image(self.tilesheet.get([j, i]), 4)
                for color in self.colorkeys:
                    pygame.transform.threshold(img,img, color, (10, 10 ,10), (0, 0, 0), 1, None, True)
                img.set_colorkey((0, 0, 0))
                img.convert()
                self.images.append(img)
        self.spike_images = spike_images
        self.damage_masks = []
        self.standing_masks = []
        self.side_rects = []
        self.enemies = []
        self.special_blocks = []
        self.coin_channel = pygame.mixer.Channel(2)
        self.coin_channel.set_volume(0.5)
        self.tile_size = [64, 64]
        self.init_render_pos = [[-1, -9.2], [-1, -12.2]]
        self.x = self.init_render_pos[self.level][0]
        self.y = self.init_render_pos[self.level][1]
        self.queue = []
        self.decorative_tiles = [76, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 105, 106, 107, 110, 111, 112, 113, 114, 123, 124, 125, 126, 127]
        self.changed = []
        self.deleted = []
        self.player_death_limit = [1500, 1500]
        self.first_tile_pos = []
        self.queue_updating = True
        self.first_cycle = True
        self.clock = pygame.time.Clock()
        self.first_layer = []
        self.coin_appending = True
        self.added_coins = 0
        self.added_spikes = 0
        self.added_spikes_h = 0
        self.camera = None
        self.exceptions = [60, 116, 117, 118, 119, 120, 121, 122, 129, 135, 136, 137, 138, 139, 140]
        self.ground = ["SpikeBall", "MovingPlatform", "FireBox"]
        self.bullet_manager = BulletManager(self)
    def spawn_animation(self, delay_wait, spike):
        renderer = self
        if (renderer.clock.get_fps()) != 0 and spike[self.attr_dict["just_spawned"]]:
                spike[self.attr_dict["delay"]] += 1
                if round(delay_wait/renderer.dt) != 0:
                    if spike[self.attr_dict["delay"]] % round(delay_wait/renderer.dt) == 0:
                        self.frame[0] += 1
                if self.frame[0] > 3:
                    self.frame[0] = 3
                    spike[self.attr_dict["just_spawned"]] = False
                self.mask = pygame.mask.from_surface(self.spikesheet.get(self.frame))
                self.mask_2 = pygame.mask.from_surface(pygame.transform.flip(self.spikesheet.get(self.frame), False, spike[6]))
                self.mask_3 = pygame.mask.from_surface(pygame.transform.rotate(self.spikesheet.get(self.frame), 90))
                self.mask_4 = pygame.mask.from_surface(pygame.transform.rotate(self.spikesheet.get(self.frame), -90))
                
    def spike_update(self):
        renderer = self
        if hasattr(renderer, "dt"):
            for spike in self.spikes:
                if spike[self.attr_dict["just_spawned"]]:
                    self.spawn_animation(4, spike)
                if spike[7]==0:
                    win.blit(pygame.transform.flip(self.spikesheet.get(self.frame), False, spike[6]), spike[self.attr_dict["pos"]])
                else:
                    win.blit(pygame.transform.rotate(self.spikesheet.get(self.frame), spike[7]), spike[self.attr_dict["pos"]])
                mouse_pos = pygame.mouse.get_pos()
                if spike[7]==0:
                    if not spike[6]:
                        if (cursor_mask.overlap(self.mask, (spike[self.attr_dict["pos"]][0]-mouse_pos[0], spike[self.attr_dict["pos"]][1]-mouse_pos[1])) == None):
                            spike[self.attr_dict["is_hovered"]] = False
                        else:
                            if len(spike) != 9:
                                if not renderer.queue_updating:
                                    spike[self.attr_dict["is_hovered"]] = True
                                else:
                                    spike[self.attr_dict["is_hovered"]] = False
                    else:
                        if (cursor_mask.overlap(self.mask_2, (spike[self.attr_dict["pos"]][0]-mouse_pos[0], spike[self.attr_dict["pos"]][1]-mouse_pos[1])) == None):
                            spike[self.attr_dict["is_hovered"]] = False
                        else:
                            if len(spike) != 9:
                                if not renderer.queue_updating:
                                    spike[self.attr_dict["is_hovered"]] = True
                                else:
                                    spike[self.attr_dict["is_hovered"]] = False
                else:
                    if spike[7]==90:
                        if (cursor_mask.overlap(self.mask_3, (spike[self.attr_dict["pos"]][0]-mouse_pos[0], spike[self.attr_dict["pos"]][1]-mouse_pos[1])) == None):
                            spike[self.attr_dict["is_hovered"]] = False
                        else:
                            if len(spike) != 9:
                                if not renderer.queue_updating:
                                    spike[self.attr_dict["is_hovered"]] = True
                                else:
                                    spike[self.attr_dict["is_hovered"]] = False
                    else:
                        if (cursor_mask.overlap(self.mask_4, (spike[self.attr_dict["pos"]][0]-mouse_pos[0], spike[self.attr_dict["pos"]][1]-mouse_pos[1])) == None):
                            spike[self.attr_dict["is_hovered"]] = False
                        else:
                            if len(spike) != 9:
                                if not renderer.queue_updating:
                                    spike[self.attr_dict["is_hovered"]] = True
                                else:
                                    spike[self.attr_dict["is_hovered"]] = False
                if spike[self.attr_dict["is_hovered"]]:
                    if pygame.mouse.get_pressed()[2]:
                        renderer.levels[renderer.level][int(spike[self.attr_dict["pos"]][1]/renderer.tile_size[1])+(0-int(renderer.init_render_pos[renderer.level][1]))][int((spike[self.attr_dict["pos"]][0]+8-renderer.camera.cam_change[0])/renderer.tile_size[0])] = renderer.queue[0].tile
                        self.spikes = [sp for sp in self.spikes if sp != spike]
                    if self.rect_surf.get_alpha() != 50:
                        self.rect_surf.set_alpha(50)
                    if spike[7]==0:
                        win.blit(self.rect_surf, [spike[self.attr_dict["pos"]][0]+4, spike[self.attr_dict["pos"]][1]+8])
                    elif spike[7]==90:
                        win.blit(self.rect_surf, [spike[self.attr_dict["pos"]][0]+4, spike[self.attr_dict["pos"]][1]])
                    elif spike[7]==-90:
                        win.blit(self.rect_surf, [spike[self.attr_dict["pos"]][0], spike[self.attr_dict["pos"]][1]+6])
                if spike[7]==0:
                    if not spike[6]:
                        if (renderer.queue[0].mask.overlap(self.mask, (spike[self.attr_dict["pos"]][0]-renderer.queue[0].pos[0], spike[self.attr_dict["pos"]][1]-renderer.queue[0].pos[1])) == None):
                            pass
                        else:
                            renderer.queue[0].is_alive = False
                            #reset(renderer.queue[0], renderer)
                            renderer.queue[0].deaths += 1
                    else:
                        if (renderer.queue[0].mask.overlap(self.mask_2, (spike[self.attr_dict["pos"]][0]-renderer.queue[0].pos[0], spike[self.attr_dict["pos"]][1]-renderer.queue[0].pos[1])) == None):
                            pass
                        else:
                            renderer.queue[0].is_alive = False
                            #reset(renderer.queue[0], renderer)
                            renderer.queue[0].deaths += 1
                else:
                    if spike[7]==90:
                        if (renderer.queue[0].mask.overlap(self.mask_3, (spike[self.attr_dict["pos"]][0]-renderer.queue[0].pos[0], spike[self.attr_dict["pos"]][1]-renderer.queue[0].pos[1])) == None):
                            pass
                        else:
                            renderer.queue[0].is_alive = False
                            #reset(renderer.queue[0], renderer)
                            renderer.queue[0].deaths += 1
                    else:
                        if (renderer.queue[0].mask.overlap(self.mask_4, (spike[self.attr_dict["pos"]][0]-renderer.queue[0].pos[0], spike[self.attr_dict["pos"]][1]-renderer.queue[0].pos[1])) == None):
                            pass
                        else:
                            renderer.queue[0].is_alive = False
                            #reset(renderer.queue[0], renderer)
                            renderer.queue[0].deaths += 1
                if spike[7]==0:
                    if not spike[6]:
                        for enemy in self.enemies:
                            if (renderer.queue[enemy].mask.overlap(self.mask, (spike[self.attr_dict["pos"]][0]-renderer.queue[enemy].pos[0], spike[self.attr_dict["pos"]][1]-renderer.queue[enemy].pos[1])) == None):
                                pass
                            else:
                                renderer.queue[enemy].is_alive = False

                    else:
                        for enemy in self.enemies:
                            if (renderer.queue[enemy].mask.overlap(self.mask_2, (spike[self.attr_dict["pos"]][0]-renderer.queue[enemy].pos[0], spike[self.attr_dict["pos"]][1]-renderer.queue[enemy].pos[1])) == None):
                                pass
                            else:
                                renderer.queue[enemy].is_alive = False

                else:
                    if spike[7]==90:
                        for enemy in self.enemies:
                            if (renderer.queue[enemy].mask.overlap(self.mask_3, (spike[self.attr_dict["pos"]][0]-renderer.queue[enemy].pos[0], spike[self.attr_dict["pos"]][1]-renderer.queue[enemy].pos[1])) == None):
                                pass
                            else:
                                renderer.queue[enemy].is_alive = False

                    else:
                        for enemy in self.enemies:
                            if (renderer.queue[enemy].mask.overlap(self.mask_4, (spike[self.attr_dict["pos"]][0]-renderer.queue[enemy].pos[0], spike[self.attr_dict["pos"]][1]-renderer.queue[enemy].pos[1])) == None):
                                pass
                            else:
                                renderer.queue[enemy].is_alive = False
                if not self.played:
                    if not web:
                        renderer.coin_channel.play(pygame.mixer.Sound("assets\Audio\spike_spawn.ogg"))
                    else:
                        renderer.coin_channel.play(pygame.mixer.Sound("assets/Audio/spike_spawn.ogg"))
                self.played = True
    def add_spike_u(self, pos):
        self.spikes.append([[pos[0], pos[1]], 0, True, 0, False, False, False, 0])
    def add_spike_d(self, pos):
        self.spikes.append([[pos[0], pos[1]+4], 0, True, 0, False, False, True, 0])
    def add_spike_r(self, pos):
        selfpos = [pos[0]+((16*90)/90)+((20*90)/90)-int(self.spikesheet.get([3, 0]).get_width()/2)-8, pos[1]+44-int(self.spikesheet.get([3, 0]).get_height()/2)]
        self.spikes.append([selfpos, 0, True, 0, False, False, True, 90])
    def add_spike_l(self, pos):
        selfpos = [pos[0]+((16*-90)/-90)+((26*-90)/-90)-int(self.spikesheet.get([3, 0]).get_width()/2)-4, pos[1]+38-int(self.spikesheet.get([3, 0]).get_height()/2)]
        self.spikes.append([selfpos, 0, True, 0, False, False, True, -90])
    def render(self):
        self.coin_count = 0
        self.spike_count = 0
        self.spike_h_count = 0
        self.damage_masks = []
        self.side_rects = []
        self.standing_masks = []
        win.blit(self.background, [0, 0])
        tilemap = self.levels[self.level]
        self.num_row = -1
        self.num_col = -1
        self.y = self.init_render_pos[self.level][1]
        for row in tilemap:
            self.y += 1
            self.num_col = -1
            self.num_row += 1
            self.x = self.init_render_pos[self.level][0]
            for tile in row:
                self.num_col += 1
                self.x+=1
                #if not [self.x*self.tile_size[0], self.y*self.tile_size[1]] in self.deleted:
                if not tile == -1 and not(tile in self.exceptions):
                    win.blit(self.images[tile], [self.x*self.tile_size[0], self.y*self.tile_size[1]])
                    if not (tile in self.decorative_tiles):
                        #if self.standing_masks[]
                        if self.queue_updating:
                            if not tile == 19:
                                if (tilemap[self.num_row-1][self.num_col] == -1) or (tilemap[self.num_row-1][self.num_col] in self.decorative_tiles):
                                    self.standing_masks.append([pygame.mask.from_surface(self.images[tile]), [self.x*self.tile_size[0], self.y*self.tile_size[1]], tile])
                        else:
                            self.standing_masks.append([pygame.mask.from_surface(self.images[tile]), [self.x*self.tile_size[0], self.y*self.tile_size[1]], tile])
                        if not tile in [26, 27, 28]:
                            if tilemap[self.num_row][self.num_col-1] == -1 or tilemap[self.num_row][self.num_col-1] in self.decorative_tiles:
                                if not tilemap[self.num_row-1][self.num_col] == -1 and not(tilemap[self.num_row-1][self.num_col] in self.decorative_tiles):
                                    self.side_rects.append([pygame.Rect(self.x*self.tile_size[0]+10, (self.y*self.tile_size[1]), 1, (self.tile_size[1])), -1])
                                    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.x*self.tile_size[0], (self.y*self.tile_size[1]), 1, (self.tile_size[1])))
                                else:
                                    self.side_rects.append([pygame.Rect(self.x*self.tile_size[0], (self.y*self.tile_size[1]+15), 1, (self.tile_size[1]-15)), -1])
                                    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.x*self.tile_size[0], (self.y*self.tile_size[1]+15), 1, (self.tile_size[1]-15)))
                            if self.num_col+1 < len(tilemap[self.num_row]):
                                if tilemap[self.num_row][self.num_col+1] == -1 or tilemap[self.num_row][self.num_col+1] in self.decorative_tiles:
                                    if not tilemap[self.num_row-1][self.num_col] == -1 and not(tilemap[self.num_row-1][self.num_col] in self.decorative_tiles):
                                        self.side_rects.append([pygame.Rect((self.x+1)*self.tile_size[0]+6, (self.y*self.tile_size[1]), 1, (self.tile_size[1])), 1])
                                        pygame.draw.rect(win, (255, 0, 0), pygame.Rect((self.x+1)*self.tile_size[0]+6, (self.y*self.tile_size[1]), 1, (self.tile_size[1])))
                                    else:
                                        self.side_rects.append([pygame.Rect((self.x+1)*self.tile_size[0]+6, (self.y*self.tile_size[1]+15), 1, (self.tile_size[1]-15)), 1])
                                        pygame.draw.rect(win, (255, 0, 0), pygame.Rect((self.x+1)*self.tile_size[0]+6, (self.y*self.tile_size[1]+15), 1, (self.tile_size[1]-15)))
                            if self.num_row+1 < len(tilemap):
                                if tilemap[self.num_row+1][self.num_col] == -1 or tilemap[self.num_row+1][self.num_col] in self.decorative_tiles:
                                    self.side_rects.append([pygame.Rect((self.x*self.tile_size[0])+7.5, ((self.y+1)*self.tile_size[1])+7.5, (self.tile_size[0]), 1), 2])
                                    pygame.draw.rect(win, (255, 0, 0), pygame.Rect((self.x*self.tile_size[0])+7.5, ((self.y+1)*self.tile_size[1])+7.5, (self.tile_size[0]), 1))
                        else:
                            if tilemap[self.num_row][self.num_col-1] == -1:
                                if not tilemap[self.num_row-1][self.num_col] == -1:
                                    self.side_rects.append([pygame.Rect(self.x*self.tile_size[0]+10, (self.y*self.tile_size[1]+(0-int(self.init_render_pos[self.level][1]))), 1, 24), -1])
                                    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.x*self.tile_size[0]+10, (self.y*self.tile_size[1]+(0-int(self.init_render_pos[self.level][1]))), 1, 24))
                                else:
                                    self.side_rects.append([pygame.Rect(self.x*self.tile_size[0]+10, (self.y*self.tile_size[1]+15), 1, (24-7)), -1])
                                    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.x*self.tile_size[0]+10, (self.y*self.tile_size[1]+15), 1, (24-7)))
                            if self.num_col+1 < len(tilemap[self.num_row]):
                                if tilemap[self.num_row][self.num_col+1] == -1:
                                    if not tilemap[self.num_row-1][self.num_col] == -1:
                                        self.side_rects.append([pygame.Rect((self.x+1)*self.tile_size[0]+6, (self.y*self.tile_size[1]+(0-int(self.init_render_pos[self.level][1]))), 1, (24)), 1])
                                        pygame.draw.rect(win, (255, 0, 0), pygame.Rect((self.x+1)*self.tile_size[0]+6, (self.y*self.tile_size[1]+(0-int(self.init_render_pos[self.level][1]))), 1, (24)))
                                    else:
                                        self.side_rects.append([pygame.Rect((self.x+1)*self.tile_size[0]+10, (self.y*self.tile_size[1]+15), 1, (24-15)), 1])
                                        pygame.draw.rect(win, (255, 0, 0), pygame.Rect((self.x+1)*self.tile_size[0]+10, (self.y*self.tile_size[1]+15), 1, (24-15)))
                            if self.num_row+1 < len(tilemap):
                                if tilemap[self.num_row+1][self.num_col] == -1:
                                    self.side_rects.append([pygame.Rect((self.x*self.tile_size[0])+7.5, ((self.y+1)*self.tile_size[1])-30, (self.tile_size[0]), 1), 2])
                                    pygame.draw.rect(win, (255, 0, 0), pygame.Rect((self.x*self.tile_size[0])+7.5, ((self.y+1)*self.tile_size[1])-30, (self.tile_size[0]), 1))
                elif tile == 60:
                    if self.coin_appending:
                        self.queue.append(Coin([self.x*self.tile_size[0], self.y*self.tile_size[1]], self.coin_img, [4, 1]))
                        self.added_coins += 1
                    self.coin_count += 1
                    if self.coin_count > self.added_coins:
                        self.queue.append(Coin([self.x*self.tile_size[0], self.y*self.tile_size[1]], self.coin_img, [4, 1]))
                        self.added_coins += 1
                elif tile == 117:
                    if self.coin_appending:
                        self.add_spike_u([self.x*self.tile_size[0], self.y*self.tile_size[1]])
                        self.added_spikes += 1
                    self.spike_count += 1
                    if self.spike_count > self.added_spikes:
                        self.add_spike_u([self.x*self.tile_size[0], self.y*self.tile_size[1]])
                        self.added_spikes += 1
                elif tile == 129:
                    if self.coin_appending:
                        self.add_spike_d([self.x*self.tile_size[0], self.y*self.tile_size[1]])
                        self.added_spikes += 1
                    self.spike_count += 1
                    if self.spike_count > self.added_spikes:
                        self.add_spike_d([self.x*self.tile_size[0], self.y*self.tile_size[1]])
                        self.added_spikes += 1
                elif tile == 138:
                    if self.coin_appending:
                        self.add_spike_r([self.x*self.tile_size[0], self.y*self.tile_size[1]])
                        self.added_spikes += 1
                    self.spike_count += 1
                    if self.spike_count > self.added_spikes:
                        self.add_spike_r([self.x*self.tile_size[0], self.y*self.tile_size[1]])
                        self.added_spikes += 1
                elif tile == 139:
                    if self.coin_appending:
                        self.add_spike_l([self.x*self.tile_size[0], self.y*self.tile_size[1]])
                        self.added_spikes += 1
                    self.spike_count += 1
                    if self.spike_count > self.added_spikes:
                        self.add_spike_l([self.x*self.tile_size[0], self.y*self.tile_size[1]])
                        self.added_spikes += 1
                elif tile == 118:
                    if self.coin_appending:
                        self.queue.append(HiddenSpike(self.spike_image, [4, 1], [self.x*self.tile_size[0], self.y*self.tile_size[1]]))
                        self.added_spikes_h += 1
                    self.spike_h_count += 1
                    if self.spike_h_count > self.added_spikes_h:
                        self.queue.append(HiddenSpike(self.spike_image, [4, 1], [self.x*self.tile_size[0], self.y*self.tile_size[1]]))
                        self.added_spikes_h += 1
                elif tile == 135:
                    if self.coin_appending:
                        self.queue.append(HiddenSpike(self.spike_image, [4, 1], [self.x*self.tile_size[0], self.y*self.tile_size[1]], True))
                        self.added_spikes_h += 1
                    self.spike_h_count += 1
                    if self.spike_h_count > self.added_spikes_h:
                        self.queue.append(HiddenSpike(self.spike_image, [4, 1], [self.x*self.tile_size[0], self.y*self.tile_size[1]], True))
                        self.added_spikes_h += 1
                elif tile == 136:
                    if self.coin_appending:
                        self.queue.append(HiddenSpike(self.spike_image, [4, 1], [self.x*self.tile_size[0], self.y*self.tile_size[1]], False, 90))
                        self.added_spikes_h += 1
                    self.spike_h_count += 1
                    if self.spike_h_count > self.added_spikes_h:
                        self.queue.append(HiddenSpike(self.spike_image, [4, 1], [self.x*self.tile_size[0], self.y*self.tile_size[1]], False, 90))
                        self.added_spikes_h += 1
                elif tile == 137:
                    if self.coin_appending:
                        self.queue.append(HiddenSpike(self.spike_image, [4, 1], [self.x*self.tile_size[0], self.y*self.tile_size[1]], False, -90))
                        self.added_spikes_h += 1
                    self.spike_h_count += 1
                    if self.spike_h_count > self.added_spikes_h:
                        self.queue.append(HiddenSpike(self.spike_image, [4, 1], [self.x*self.tile_size[0], self.y*self.tile_size[1]], False, -90))
                        self.added_spikes_h += 1
                elif tile == 119:
                    if self.coin_appending:
                        self.queue.append(Crusher([self.x*self.tile_size[0], self.y*self.tile_size[1]]))
                elif tile == 120:
                    if self.coin_appending:
                        self.queue.append(SpikeBall([self.x*self.tile_size[0], self.y*self.tile_size[1]]))
                elif tile == 121:
                    if self.coin_appending:
                        self.queue.append(SwingingAxe([self.x*self.tile_size[0], self.y*self.tile_size[1]]))
                elif tile == 122:
                    if self.coin_appending:
                        self.queue.append(MovingPlatform(5, [self.x*self.tile_size[0], self.y*self.tile_size[1]], 3, 200))
                elif tile == 116:
                    if self.coin_appending:
                        self.queue.append(FireBox([self.x*self.tile_size[0], self.y*self.tile_size[1]]))
                elif tile == 140:
                    if self.coin_appending:
                        self.enemies.append(len(self.queue))
                        self.queue.append(EnemySwordsman([self.x*self.tile_size[0], self.y*self.tile_size[1]], self))
        self.first_cycle = False
        self.coin_appending = False
    def update(self):
        self.clock.tick(self.def_frame)
        if self.clock.get_fps() != 0:
            self.dt = 60/self.clock.get_fps()
        self.render()
        self.enemies = []
        if self.queue != []:
            for obj in self.queue:
                if obj.__class__.__name__ in self.ground:
                    obj.update(self)
                if obj.__class__.__name__ == "EnemySwordsman":
                    if obj.is_alive:
                        self.enemies.append(self.queue.index(obj))
            for obj in self.queue:
                if obj != None:
                    if not (obj.__class__.__name__ in self.ground):
                        obj.update(self)
                
            self.spike_update()
        self.bullet_manager.update_physics(self)
        self.bullet_manager.update_graphics(self)
        
        #if not web:
            #print(self.clock.get_fps())

        
