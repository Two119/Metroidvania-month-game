from assets.scripts.level_renderer import *
from assets.scripts.player import *
from assets.scripts.camera import *
from assets.scripts.objectives import *
from assets.scripts.button import *
from assets.scripts.slider import *
from assets.scripts.checkbox import *
from assets.scripts.save_system import *
def ismovingfirebox(box):
    if isinstance(box, FireBox):
        if box.on_platform:
            return True
    return False
def start(args):
    if hasattr(args.renderer, "camera"):
        reset(args.renderer.queue[0], args.renderer)
        args.spare_surf = None
    args.screen = 1
    args.playing  = True
def back_to_game(args):
    args.screen = 1
    args.playing = True
    args.renderer.bullet_manager.remove = True
def back_to_menu(args):
    args.screen = 1
def settings(args):
    args.screen = 2
def settings_2(args):
    args.screen = 5
def back(args):
    if hasattr(args.renderer, "camera"):
        reset(args.renderer.queue[0], args.renderer)
        args.spare_surf = None
    args.screen = 0
    args.playing  = False
    m_pos = pygame.mouse.get_pos()
    pygame.mouse.set_pos([m_pos[0]-120, m_pos[1]])
def game_menu(args):
    pygame.image.save(win, "win.png")
    args.spare_surf = pygame.image.load("win.png").convert()
    args.playing = False
def open_shop(args):
    args.screen = 3
def open_shop_2(args):
    args.screen = 4
    m_pos = pygame.mouse.get_pos()
    pygame.mouse.set_pos([m_pos[0], m_pos[1]-90])
class Game:
    def __init__(self):
        self.save_system = SaveSystem()
        if not web:
            self.renderer = LevelRenderer([json.load(open("levels.json", "r"))["level_1"], json.load(open("levels.json", "r"))["level_2"]], pygame.image.load("assets\Spritesheets\desert.png").convert(), [13, 10], [], [[20, 21, 19]],pygame.image.load("assets\Backgrounds\\background.png").convert(), pygame.image.load("assets\Spritesheets\coin.png").convert())
            self.save_system.load(self.renderer)
            self.player = Player(spawn_positions[self.renderer.level], scale_image(pygame.image.load("assets\Spritesheets\player.png").convert()), [4, 22])
            self.ui_font = pygame.font.Font("assets\\Fonts\\yoster.ttf", 20)
            self.d_font = pygame.font.Font("assets\\Fonts\\yoster.ttf", 35)
            self.button_sprites = SpriteSheet(scale_image(pygame.image.load("assets\Spritesheets\\buttons.png")), [2, 1], [255, 255, 255])
            self.small_button_sprites = SpriteSheet(scale_image(pygame.image.load("assets\Spritesheets\\small_buttons.png")), [2, 1], [255, 255, 255])
        else:
            self.renderer = LevelRenderer([json.load(open("levels.json", "r"))["level_1"], json.load(open("levels.json", "r"))["level_2"]], pygame.image.load("assets/Spritesheets/desert.png").convert(), [13, 10], [], [[20, 21, 19]],pygame.image.load("assets/Backgrounds/background.png").convert(), pygame.image.load("assets/Spritesheets/coin.png").convert())
            self.save_system.load(self.renderer)
            self.player = Player(spawn_positions[self.renderer.level], scale_image(pygame.image.load("assets/Spritesheets/player.png").convert()), [4, 22])
            self.ui_font = pygame.font.Font("assets/Fonts/yoster.ttf", 20)
            self.d_font = pygame.font.Font("assets/Fonts/yoster.ttf", 35)
            self.button_sprites = SpriteSheet(scale_image(pygame.image.load("assets/Spritesheets/buttons.png")), [2, 1], [255, 255, 255])
            self.small_button_sprites = SpriteSheet(scale_image(pygame.image.load("assets/Spritesheets/small_buttons.png")), [2, 1], [255, 255, 255])
        self.camera = Camera()
        self.cursor_img_ = scale_image(cursor_img, 2)
        self.objective_manager = ObjectiveManager()
        self.spare_surf = None
        self.run = True
        self.screen = 0
        self.renderer.queue.append(self.player)
        pygame.mouse.set_visible(False)
        self.volume = 0.75
        self.cursor_mask = pygame.mask.from_surface(self.cursor_img_)
        self.rect_surf = pygame.Surface((64, 64))
        self.rect_surf.set_alpha(50)
        self.cursor_img_.set_colorkey([0, 0, 0])
        self.renderer.super = self
        self.auto_save = True
        self.start_text = scale_image(self.ui_font.render("Start", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.restart_text = scale_image(self.ui_font.render("Restart", False, (255, 255, 255), (0, 0, 0)), 1.1)
        self.vol_text = scale_image(self.ui_font.render("Volume", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.fps_text = scale_image(self.ui_font.render("Framerate", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.back_text = scale_image(self.ui_font.render("Back", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.menu_text = scale_image(self.ui_font.render("Home", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.set_text = scale_image(self.ui_font.render("Options", False, (255, 255, 255), (0, 0, 0)), 1.2)
        self.shop_text = scale_image(self.ui_font.render("Shop", False, (255, 255, 255), (0, 0, 0)), 1.3)
        self.renderer.font = self.ui_font
        self.start_text.set_colorkey((0, 0, 0))
        self.restart_text.set_colorkey((0, 0, 0))
        self.set_text.set_colorkey((0, 0, 0))
        self.spawn_positions = [[64, 5*64], [64, 1.5*64]]
        self.vol_text.set_colorkey((0, 0, 0))
        self.menu_text.set_colorkey((0, 0, 0))
        self.back_text.set_colorkey((0, 0, 0))
        self.fps_text.set_colorkey((0, 0, 0))
        self.shop_text.set_colorkey((0, 0, 0))
        self.cycles = 0
        self.playing = True
        self.renderer.camera = self.camera
        self.death_surf = self.d_font.render("You died!", False, (255, 255, 255), (0, 0, 0))
        self.death_surf.set_colorkey((0, 0, 0))
        self.buttons = [Button(center_pos(self.button_sprites.get([0, 0])), self.button_sprites.sheet[0], [start, self], win), Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(1*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [settings, self], win)]
        shop_button = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(2*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [open_shop, self], win)
        self.shop_button_2 = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(3*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [open_shop_2, self], win)
        self.buttons.append(shop_button)
        self.settings_2 = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(1*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [settings_2, self], win)
        #self.buttons = [Button(center_pos(self.button_sprites.get([0, 0])), self.button_sprites.sheet[0], [start, self], win), Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(1*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [settings, self], win)]
        self.settings = [Slider([[center_pos(self.button_sprites.get([0, 0]))[0]+(self.vol_text.get_width()/2)+20, center_pos(self.button_sprites.get([0, 0]))[1]+(-2*self.button_sprites.get([0, 0]).get_height())], self.ui_font, True, self]), Slider([[center_pos(self.button_sprites.get([0, 0]))[0]+(self.vol_text.get_width()/2)+20, center_pos(self.button_sprites.get([0, 0]))[1]+(-1*self.button_sprites.get([0, 0]).get_height())], self.ui_font, False, self]), Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(3*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back, self], win)]
        self.small_menu_button = Button([win_size[0]-66, 10], self.small_button_sprites.sheet[0], [game_menu, self], win)
        self.back_button = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(4*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back_to_menu, self], win)
        self.back_button_ = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(5*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back, self], win)
        self.back_button_3 = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(5*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back_to_menu, self], win)
        self.back_button_2 = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(-1*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back_to_game, self], win)
        self.back = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]-(self.button_sprites.get([0, 0]).get_height())+(3*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back, self], win)
        self.renderer.button = self.small_menu_button
        self.shoppables = []
        self.finished = False
        self.radius = 0
        self.add_rad = 0.12
        self.level_spike_dicts = {0: 780, 1:-64}
        self.x_level_dicts = {0: 0, 1:256}
        self.shop = Shop(self.renderer)
        self.renderer.shop = self.shop
        self.save_system.load(self.renderer)
    def update(self):
        self.renderer.clock.tick(self.renderer.def_frame)
        self.cycles += 1
        cursor_pos = pygame.mouse.get_pos()
        win.fill((0, 0, 0))
        if self.screen == 1:
            if self.playing and self.renderer.queue[0].is_alive:
                self.renderer.update()
                self.camera.update(self.renderer)
                self.renderer.camera = self.camera
                if self.objective_manager.update(self.renderer):
                    self.renderer.queue[0].levels_unlocked.append(self.renderer.level+1)
                    self.renderer.level+=1
                    self.screen = 0
                s_urf = scale_image(self.ui_font.render(str(self.renderer.queue[0].coins), False, (255, 255, 255), (0, 0, 0))) 
                s_urf.set_colorkey((0, 0, 0)) 
                win.blit(s_urf, [100, 100])
                if self.renderer.queue_updating == False:
                    for double_list in self.renderer.standing_masks:
                            if (self.cursor_mask.overlap(double_list[0], (double_list[1][0]-cursor_pos[0], double_list[1][1]-cursor_pos[1])) == None):
                                pass
                            else:
                                if double_list[2] != 122 and not isinstance(double_list[2], SpikeBall) and not ismovingfirebox(double_list[2]):
                                    if not isinstance(double_list[2], FireBox):
                                        if pygame.mouse.get_pressed()[2] and double_list[2] != self.renderer.queue[0].tile:
                                            self.renderer.queue[0].shapeshifts -= 1
                                            self.renderer.levels[self.renderer.level][double_list[3][1]][double_list[3][0]] = self.renderer.queue[0].tile
                                            if self.renderer.level == 0:
                                                if self.renderer.queue[0].tile == 117:
                                                    self.renderer.add_spike_u([double_list[3][0]*64+self.renderer.camera.cam_change[0], double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4], True)
                                                    self.renderer.added_spikes += 1
                                                    self.renderer.spike_count += 1
                                                    if self.renderer.spike_count > self.renderer.added_spikes:
                                                        self.renderer.add_spike_u([double_list[3][0]*64+self.renderer.camera.cam_change[0], double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4], True)
                                                        self.renderer.added_spikes += 1
                                                    self.renderer.queue[0].shapeshifting=False
                                                    self.renderer.queue_updating = True
                                                if self.renderer.queue[0].tile == 129:
                                                    self.renderer.add_spike_d([double_list[3][0]*64+self.renderer.camera.cam_change[0], double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-1], True)
                                                    self.renderer.added_spikes += 1
                                                    self.renderer.spike_count += 1
                                                    if self.renderer.spike_count > self.renderer.added_spikes:
                                                        self.renderer.add_spike_d([double_list[3][0]*64+self.renderer.camera.cam_change[0], double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-1], True)
                                                        self.renderer.added_spikes += 1
                                                    self.renderer.queue[0].shapeshifting=False
                                                    self.renderer.queue_updating = True
                                                if self.renderer.queue[0].tile == 138:
                                                    self.renderer.add_spike_r([double_list[3][0]*64+self.renderer.camera.cam_change[0]+1, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4], True)
                                                    self.renderer.added_spikes += 1
                                                    self.renderer.spike_count += 1
                                                    if self.renderer.spike_count > self.renderer.added_spikes:
                                                        self.renderer.add_spike_r([double_list[3][0]*64+self.renderer.camera.cam_change[0]+1, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4], True)
                                                        self.renderer.added_spikes += 1
                                                    self.renderer.queue[0].shapeshifting=False
                                                    self.renderer.queue_updating = True
                                                if self.renderer.queue[0].tile == 139:
                                                    self.renderer.add_spike_l([double_list[3][0]*64+self.renderer.camera.cam_change[0]-1, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-1], True)
                                                    self.renderer.added_spikes += 1
                                                    self.renderer.spike_count += 1
                                                    if self.renderer.spike_count > self.renderer.added_spikes:
                                                        self.renderer.add_spike_l([double_list[3][0]*64+self.renderer.camera.cam_change[0]-1, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-1], True)
                                                        self.renderer.added_spikes += 1
                                                    self.renderer.queue[0].shapeshifting=False
                                                    self.renderer.queue_updating = True
                                                if self.renderer.queue[0].tile == 118:
                                                    if True:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0], double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4]))
                                                        self.renderer.added_spikes_h += 1
                                                    self.renderer.spike_h_count += 1
                                                    if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0], double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4]))
                                                        self.renderer.added_spikes_h += 1
                                                if self.renderer.queue[0].tile == 135:
                                                    if True:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0], double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]+4], True))
                                                        self.renderer.added_spikes_h += 1
                                                    self.renderer.spike_h_count += 1
                                                    if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0], double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]+4], True))
                                                        self.renderer.added_spikes_h += 1
                                                if self.renderer.queue[0].tile == 136:
                                                    if True:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-12, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-8], False, 90))
                                                        self.renderer.added_spikes_h += 1
                                                    self.renderer.spike_h_count += 1
                                                    if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-12, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-8], False, 90))
                                                        self.renderer.added_spikes_h += 1
                                                if self.renderer.queue[0].tile == 137:
                                                    self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-4, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-8], False, -90))
                                                    self.renderer.added_spikes_h += 1
                                                    self.renderer.spike_h_count += 1
                                                    if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-4, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-8], False, -90))
                                                        self.renderer.added_spikes_h += 1
                                            else:
                                                if self.renderer.queue[0].tile == 117:
                                                    self.renderer.add_spike_u([double_list[3][0]*64+self.renderer.camera.cam_change[0]-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4], True)
                                                    self.renderer.added_spikes += 1
                                                    self.renderer.spike_count += 1
                                                    if self.renderer.spike_count > self.renderer.added_spikes:
                                                        self.renderer.add_spike_u([double_list[3][0]*64+self.renderer.camera.cam_change[0]-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4], True)
                                                        self.renderer.added_spikes += 1
                                                    self.renderer.queue[0].shapeshifting=False
                                                    self.renderer.queue_updating = True
                                                if self.renderer.queue[0].tile == 129:
                                                    self.renderer.add_spike_d([double_list[3][0]*64+self.renderer.camera.cam_change[0]-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-1], True)
                                                    self.renderer.added_spikes += 1
                                                    self.renderer.spike_count += 1
                                                    if self.renderer.spike_count > self.renderer.added_spikes:
                                                        self.renderer.add_spike_d([double_list[3][0]*64+self.renderer.camera.cam_change[0]-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-1], True)
                                                        self.renderer.added_spikes += 1
                                                    self.renderer.queue[0].shapeshifting=False
                                                    self.renderer.queue_updating = True
                                                if self.renderer.queue[0].tile == 138:
                                                    self.renderer.add_spike_r([double_list[3][0]*64+self.renderer.camera.cam_change[0]+1-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4], True)
                                                    self.renderer.added_spikes += 1
                                                    self.renderer.spike_count += 1
                                                    if self.renderer.spike_count > self.renderer.added_spikes:
                                                        self.renderer.add_spike_r([double_list[3][0]*64+self.renderer.camera.cam_change[0]+1-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4], True)
                                                        self.renderer.added_spikes += 1
                                                    self.renderer.queue[0].shapeshifting=False
                                                    self.renderer.queue_updating = True
                                                if self.renderer.queue[0].tile == 139:
                                                    self.renderer.add_spike_l([double_list[3][0]*64+self.renderer.camera.cam_change[0]-1-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-1], True)
                                                    self.renderer.added_spikes += 1
                                                    self.renderer.spike_count += 1
                                                    if self.renderer.spike_count > self.renderer.added_spikes:
                                                        self.renderer.add_spike_l([double_list[3][0]*64+self.renderer.camera.cam_change[0]-1-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-1], True)
                                                        self.renderer.added_spikes += 1
                                                    self.renderer.queue[0].shapeshifting=False
                                                    self.renderer.queue_updating = True
                                                if self.renderer.queue[0].tile == 118:
                                                    if True:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4]))
                                                        self.renderer.added_spikes_h += 1
                                                    self.renderer.spike_h_count += 1
                                                    if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-4]))
                                                        self.renderer.added_spikes_h += 1
                                                if self.renderer.queue[0].tile == 135:
                                                    if True:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]+4], True))
                                                        self.renderer.added_spikes_h += 1
                                                    self.renderer.spike_h_count += 1
                                                    if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]+4], True))
                                                        self.renderer.added_spikes_h += 1
                                                if self.renderer.queue[0].tile == 136:
                                                    if True:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-12-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-8], False, 90))
                                                        self.renderer.added_spikes_h += 1
                                                    self.renderer.spike_h_count += 1
                                                    if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-12-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-8], False, 90))
                                                        self.renderer.added_spikes_h += 1
                                                if self.renderer.queue[0].tile == 137:
                                                    self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-4-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-8], False, -90))
                                                    self.renderer.added_spikes_h += 1
                                                    self.renderer.spike_h_count += 1
                                                    if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                        self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[3][0]*64+self.renderer.camera.cam_change[0]-4-256, double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]-8], False, -90))
                                                        self.renderer.added_spikes_h += 1
                                            if self.renderer.queue[0].tile == 121:
                                                self.renderer.queue.append(SwingingAxe([((int((double_list[1][0]-self.renderer.camera.cam_change[0])/self.renderer.tile_size[0]))*self.renderer.tile_size[0])+self.camera.cam_change[0], (int((double_list[1][1])/self.renderer.tile_size[1])+(0-int(self.renderer.init_render_pos[self.renderer.level][1])))*self.renderer.tile_size[1]-self.level_spike_dicts[self.renderer.level]+self.camera.cam_change[1]]))
                                            if self.renderer.queue[0].tile == 116:
                                                self.renderer.queue.append(FireBox([double_list[3][0]*64+self.renderer.camera.cam_change[0]-self.x_level_dicts[self.renderer.level], double_list[3][1]*64+self.renderer.camera.cam_change[1]-self.level_spike_dicts[self.renderer.level]], True))
                                                self.renderer.queue[0].shapeshifting=False
                                                self.renderer.queue_updating = True
                                            self.renderer.queue[0].shapeshifting=False
                                            self.renderer.queue_updating = True
                                        pygame.draw.rect(self.rect_surf, (255, 0, 0), pygame.Rect(0, 0, 64, 64))
                                        win.blit(self.rect_surf, [double_list[1][0]+4, double_list[1][1]+4])
                                    else:
                                        if pygame.mouse.get_pressed()[2] and not self.renderer.queue[0].tile==116:
                                            self.renderer.queue[0].shapeshifts -= 1
                                            old_value = self.renderer.levels[self.renderer.level][double_list[3][1]][double_list[3][0]]*2
                                            if self.renderer.level == 0:
                                                self.renderer.levels[self.renderer.level][double_list[3][1]+4][double_list[3][0]] = self.renderer.queue[0].tile
                                            else:
                                                self.renderer.levels[self.renderer.level][int((double_list[1][1])/self.renderer.tile_size[1])+(0-int(self.renderer.init_render_pos[self.renderer.level][1]))+1][4+int((double_list[1][0]-self.camera.cam_change[0])/self.renderer.tile_size[0])] = self.renderer.queue[0].tile 
                                            if self.renderer.queue[0].tile == 121:
                                                self.renderer.queue.append(SwingingAxe([(int((double_list[1][0]-self.renderer.camera.cam_change[0])/self.renderer.tile_size[0]))*self.renderer.tile_size[0]+self.camera.cam_change[0], (int((double_list[1][1])/self.renderer.tile_size[1])+(0-int(self.renderer.init_render_pos[self.renderer.level][1])))*self.renderer.tile_size[1]-self.level_spike_dicts[self.renderer.level]+64+self.camera.cam_change[1]]))
                                            if self.renderer.queue[0].tile == 118:
                                                if True:
                                                    self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[2].pos[0]-4, double_list[2].pos[1]+56]))
                                                    self.renderer.added_spikes_h += 1
                                                self.renderer.spike_h_count += 1
                                                if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                    self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[2].pos[0]-4, double_list[2].pos[1]+56]))
                                                    self.renderer.added_spikes_h += 1
                                            if self.renderer.queue[0].tile == 135:
                                                if True:
                                                    self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[2].pos[0]-4, double_list[2].pos[1]+60], True))
                                                    self.renderer.added_spikes_h += 1
                                                self.renderer.spike_h_count += 1
                                                if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                    self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[2].pos[0]-4, double_list[2].pos[1]+60], True))
                                                    self.renderer.added_spikes_h += 1
                                            if self.renderer.queue[0].tile == 136:
                                                if True:
                                                    self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[2].pos[0]-18, double_list[2].pos[1]+56], False, 90))
                                                    self.renderer.added_spikes_h += 1
                                                self.renderer.spike_h_count += 1
                                                if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                    self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[2].pos[0]-18, double_list[2].pos[1]+56], False, 90))
                                                    self.renderer.added_spikes_h += 1
                                            if self.renderer.queue[0].tile == 137:
                                                self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[2].pos[0]-8, double_list[2].pos[1]+56], False, -90))
                                                self.renderer.added_spikes_h += 1
                                                self.renderer.spike_h_count += 1
                                                if self.renderer.spike_h_count > self.renderer.added_spikes_h:
                                                    self.renderer.queue.append(HiddenSpike(self.renderer.spike_image, [4, 1], [double_list[2][0]-8, double_list[2].pos[1]+56], False, -90))
                                                    self.renderer.added_spikes_h += 1
                                        pygame.draw.rect(self.rect_surf, (255, 0, 0), pygame.Rect(0, 0, 64, 64))
                                        win.blit(self.rect_surf, [double_list[1][0], double_list[1][1]+64])
                    for obj in self.renderer.queue:
                        if not obj.__class__.__name__ in ["Player", "SpikeManager", "Shop"] and hasattr(obj, "mask"):
                            if (self.cursor_mask.overlap(obj.mask, (obj.pos[0]-cursor_pos[0], obj.pos[1]-cursor_pos[1])) == None) and not isinstance(obj, SpikeBall):
                                obj.is_hovered = False
                            else:
                                if not hasattr(obj, 'on_platform'):
                                    obj.is_hovered = True
                                else:
                                    if not obj.on_platform:
                                        obj.is_hovered = True
                self.small_menu_button.update(self.renderer)
            if not self.playing:
                if self.spare_surf == None:
                    pygame.image.save(win, "win.png")
                    self.spare_surf = pygame.image.load("win.png").convert()
                win.blit(self.spare_surf, (0, 0))
                win.blit(self.renderer.surf, (0, 0))
                self.buttons[0].update(self.renderer)
                self.settings_2.update(self.renderer)
                self.back.update(self.renderer)
                self.back_button_2.update(self.renderer)
                self.shop_button_2.update(self.renderer)
                win.blit(self.restart_text, [self.buttons[0].pos[0]+10, self.buttons[0].pos[1]+15+(4*self.buttons[0].current)])
                win.blit(self.set_text, [self.buttons[1].pos[0]+5, self.buttons[1].pos[1]+15+(4*self.settings_2.current)])
                win.blit(self.menu_text, [center_pos(self.button_sprites.get([0, 0]))[0]+self.menu_text.get_width()/4, center_pos(self.button_sprites.get([0, 0]))[1]+10+(2*self.button_sprites.get([0, 0]).get_height())+(4*self.back.current)])
                win.blit(self.back_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+(-0.8*self.button_sprites.get([0, 0]).get_height())+(4*self.back_button_2.current)])
                win.blit(self.shop_text, [center_pos(self.button_sprites.get([0, 0]))[0]+self.shop_text.get_width()/3, center_pos(self.button_sprites.get([0, 0]))[1]+(3.25*self.button_sprites.get([0, 0]).get_height())+(4*self.shop_button_2.current)])
            if not self.renderer.queue[0].is_alive:
                if self.radius == 0:
                    pygame.image.save(win, "win.png")
                    self.spare_surf = pygame.image.load("win.png").convert()
                if self.finished:
                    win.blit(self.cursor_img_, cursor_pos)
                    start(self)
                    self.finished = False
                    return
                else:
                    self.radius+=(self.add_rad*(60/self.renderer.clock.get_fps()))
                    self.add_rad+=(0.15)*(60/self.renderer.clock.get_fps())
                    if self.radius >= 700:
                        self.finished = True
                        self.radius = 0 
                        self.add_rad = 0.12
                        return
                
                win.blit(self.spare_surf, (0, 0))
                win.blit(self.renderer.surf, (0, 0))
                if not self.finished:
                    pygame.draw.circle(win, [0, 0, 0], [640, 360], self.radius)
                

        elif self.screen == 0:
            win.blit(self.renderer.background, (0, 0))
            for button in self.buttons:
                button.update(self.renderer)
            win.blit(self.start_text, [self.buttons[0].pos[0]+10, self.buttons[0].pos[1]+10+(4*self.buttons[0].current)])
            win.blit(self.set_text, [self.buttons[1].pos[0]+5, self.buttons[1].pos[1]+15+(4*self.buttons[1].current)])
            win.blit(self.shop_text, [self.buttons[2].pos[0]+(self.buttons[2].textures[0].get_width()-self.shop_text.get_width())/2, self.buttons[2].pos[1]+15+(4*self.buttons[2].current)])
        elif self.screen == 2:
            #self.settings[len(self.settings)-1].pos = [center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(3*self.button_sprites.get([0, 0]).get_height())]
            win.blit(self.renderer.background, (0, 0))
            #self.settings[1].update()
            self.settings[0].update()
            self.settings[2].update(self.renderer)
            win.blit(self.vol_text, [center_pos(self.button_sprites.get([0, 0]))[0]-(self.vol_text.get_width()/2), center_pos(self.button_sprites.get([0, 0]))[1]+(-2*self.button_sprites.get([0, 0]).get_height())])
            #win.blit(self.fps_text, [center_pos(self.button_sprites.get([0, 0]))[0]-(self.fps_text.get_width()/1.5), center_pos(self.button_sprites.get([0, 0]))[1]+(-1*self.button_sprites.get([0, 0]).get_height())])
            win.blit(self.back_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+(3.2*self.button_sprites.get([0, 0]).get_height())+(4*self.settings[2].current)])
            self.renderer.coin_channel.set_volume(self.settings[0].value/10)
            self.renderer.queue[0].channel.set_volume(self.settings[0].value/10)
        elif self.screen == 3:
            win.blit(self.renderer.background, (0, 0))
            #self.settings[1].update()
            
            self.shop.update(self.renderer)
            self.back_button_.update(self.renderer)
            win.blit(self.back_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+(5.2*self.button_sprites.get([0, 0]).get_height())+(4*self.back_button_.current)])
        elif self.screen == 4:
            if self.spare_surf == None:
                pygame.image.save(win, "win.png")
                self.spare_surf = pygame.image.load("win.png").convert()
            win.blit(self.spare_surf, (0, 0))
            win.blit(self.renderer.surf, (0, 0))
            #self.settings[1].update()
            
            self.shop.update(self.renderer)
            self.back_button_3.update(self.renderer)
            win.blit(self.back_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+(5.2*self.button_sprites.get([0, 0]).get_height())+(4*self.back_button_3.current)])
        elif self.screen == 5:
            if self.spare_surf != None:
                win.blit(self.spare_surf, (0, 0))
                win.blit(self.renderer.surf, (0, 0))
            self.settings[0].update()
            self.back_button.update(self.renderer)
            win.blit(self.back_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+(4.2*self.button_sprites.get([0, 0]).get_height())+(4*self.back_button.current)])
            #self.settings[2].update(self.renderer)
            win.blit(self.vol_text, [center_pos(self.button_sprites.get([0, 0]))[0]-(self.vol_text.get_width()/2), center_pos(self.button_sprites.get([0, 0]))[1]+(-2*self.button_sprites.get([0, 0]).get_height())])
            self.renderer.coin_channel.set_volume(self.settings[0].value/10)
            self.renderer.queue[0].channel.set_volume(self.settings[0].value/10)
        win.blit(self.cursor_img_, cursor_pos)
        if ((self.cycles%20)==0):
            self.save_system.update(self.renderer)