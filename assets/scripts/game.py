from assets.scripts.level_renderer import *
from assets.scripts.player import *
from assets.scripts.camera import *
from assets.scripts.objectives import *
from assets.scripts.button import *
from assets.scripts.slider import *
from assets.scripts.checkbox import *
from assets.scripts.save_system import *
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
def back(args):
    args.screen = 0
def game_menu(args):
    pygame.image.save(win, "win.png")
    args.spare_surf = pygame.image.load("win.png").convert()
    args.playing = False
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
        self.save_system.load(self.renderer)
        self.renderer.super = self
        self.auto_save = True
        self.start_text = scale_image(self.ui_font.render("Start", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.restart_text = scale_image(self.ui_font.render("Restart", False, (255, 255, 255), (0, 0, 0)), 1.1)
        self.vol_text = scale_image(self.ui_font.render("Volume", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.fps_text = scale_image(self.ui_font.render("Framerate", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.back_text = scale_image(self.ui_font.render("Back", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.menu_text = scale_image(self.ui_font.render("Menu", False, (255, 255, 255), (0, 0, 0)), 1.5)
        self.set_text = scale_image(self.ui_font.render("Options", False, (255, 255, 255), (0, 0, 0)), 1.2)
        self.start_text.set_colorkey((0, 0, 0))
        self.restart_text.set_colorkey((0, 0, 0))
        self.set_text.set_colorkey((0, 0, 0))
        self.spawn_positions = [[64, 5*64], [64, 1.5*64]]
        self.vol_text.set_colorkey((0, 0, 0))
        self.menu_text.set_colorkey((0, 0, 0))
        self.back_text.set_colorkey((0, 0, 0))
        self.fps_text.set_colorkey((0, 0, 0))
        self.cycles = 0
        self.playing = True
        self.renderer.camera = self.camera
        self.death_surf = self.d_font.render("You died!", False, (255, 255, 255), (0, 0, 0))
        self.death_surf.set_colorkey((0, 0, 0))
        self.buttons = [Button(center_pos(self.button_sprites.get([0, 0])), self.button_sprites.sheet[0], [start, self], win), Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(1*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [settings, self], win)]
        #self.buttons = [Button(center_pos(self.button_sprites.get([0, 0])), self.button_sprites.sheet[0], [start, self], win), Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(1*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [settings, self], win)]
        self.settings = [Slider([[center_pos(self.button_sprites.get([0, 0]))[0]+(self.vol_text.get_width()/2)+20, center_pos(self.button_sprites.get([0, 0]))[1]+(-2*self.button_sprites.get([0, 0]).get_height())], self.ui_font, True, self]), Slider([[center_pos(self.button_sprites.get([0, 0]))[0]+(self.vol_text.get_width()/2)+20, center_pos(self.button_sprites.get([0, 0]))[1]+(-1*self.button_sprites.get([0, 0]).get_height())], self.ui_font, False, self]), Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(3*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back, self], win)]
        self.small_menu_button = Button([win_size[0]-66, 10], self.small_button_sprites.sheet[0], [game_menu, self], win)
        self.back_button = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(3*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back_to_menu, self], win)
        self.back_button_2 = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(-1*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back_to_game, self], win)
        self.back = Button([center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]-(self.button_sprites.get([0, 0]).get_height())+(3*self.button_sprites.get([0, 0]).get_height())], self.button_sprites.sheet[0], [back, self], win)
        self.renderer.button = self.small_menu_button
    def update(self):
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
                                if double_list[2] != 122:
                                    if pygame.mouse.get_pressed()[2]:
                                            self.renderer.levels[self.renderer.level][int((double_list[1][1])/self.renderer.tile_size[1])+(0-int(self.renderer.init_render_pos[self.renderer.level][1]))][int((double_list[1][0]-self.camera.cam_change[0])/self.renderer.tile_size[0])] = self.renderer.queue[0].tile
                                    pygame.draw.rect(self.rect_surf, (255, 0, 0), pygame.Rect(0, 0, 64, 64))
                                    win.blit(self.rect_surf, [double_list[1][0]+4, double_list[1][1]+4])
                    for obj in self.renderer.queue:
                        if not obj.__class__.__name__ in ["Player", "SpikeManager"] and hasattr(obj, "mask"):
                            if (self.cursor_mask.overlap(obj.mask, (obj.pos[0]-cursor_pos[0], obj.pos[1]-cursor_pos[1])) == None):
                                obj.is_hovered = False
                            else:
                                obj.is_hovered = True
                self.small_menu_button.update()
            if not self.playing:
                if self.spare_surf == None:
                    pygame.image.save(win, "win.png")
                    self.spare_surf = pygame.image.load("win.png").convert()
                win.blit(self.spare_surf, (0, 0))
                win.blit(self.renderer.surf, (0, 0))
                for button in self.buttons:
                    button.update()
                self.back.update()
                self.back_button_2.update()
                win.blit(self.restart_text, [self.buttons[0].pos[0]+10, self.buttons[0].pos[1]+15+(3*self.buttons[0].current)])
                win.blit(self.set_text, [self.buttons[1].pos[0]+5, self.buttons[1].pos[1]+15+(3*self.buttons[1].current)])
                win.blit(self.menu_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+10+(2*self.button_sprites.get([0, 0]).get_height())+(3*self.back.current)])
                win.blit(self.back_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+(-0.8*self.button_sprites.get([0, 0]).get_height())+(3*self.back_button_2.current)])
            if not self.renderer.queue[0].is_alive:
                if self.spare_surf == None:
                    pygame.image.save(win, "win.png")
                    self.spare_surf = pygame.image.load("win.png").convert()
                win.blit(self.spare_surf, (0, 0))
                win.blit(self.renderer.surf, (0, 0))
                for button in self.buttons:
                    button.update()
                self.back.update()
                if pygame.key.get_pressed()[pygame.K_r]:
                    self.buttons[0].onlick(self.buttons[0].args)
                #self.back_button_2.update()
                win.blit(self.restart_text, [self.buttons[0].pos[0]+10, self.buttons[0].pos[1]+15+(3*self.buttons[0].current)])
                win.blit(self.set_text, [self.buttons[1].pos[0]+5, self.buttons[1].pos[1]+15+(3*self.buttons[1].current)])
                win.blit(self.menu_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+10+(2*self.button_sprites.get([0, 0]).get_height())+(3*self.back.current)])
                win.blit(self.death_surf, [center_pos(self.death_surf)[0], center_pos(self.death_surf)[1]-50])

        elif self.screen == 0:
            win.blit(self.renderer.background, (0, 0))
            for button in self.buttons:
                button.update()
            win.blit(self.start_text, [self.buttons[0].pos[0]+10, self.buttons[0].pos[1]+10+(3*self.buttons[0].current)])
            win.blit(self.set_text, [self.buttons[1].pos[0]+5, self.buttons[1].pos[1]+15+(3*self.buttons[1].current)])
        elif self.screen == 2:
            #self.settings[len(self.settings)-1].pos = [center_pos(self.button_sprites.get([0, 0]))[0], center_pos(self.button_sprites.get([0, 0]))[1]+(3*self.button_sprites.get([0, 0]).get_height())]
            win.blit(self.renderer.background, (0, 0))
            self.settings[0].update()
            #self.settings[1].update()
            if self.playing:
                self.settings[2].update()
            else:
                self.back_button.update()
            win.blit(self.vol_text, [center_pos(self.button_sprites.get([0, 0]))[0]-(self.vol_text.get_width()/2), center_pos(self.button_sprites.get([0, 0]))[1]+(-2*self.button_sprites.get([0, 0]).get_height())])
            #win.blit(self.fps_text, [center_pos(self.button_sprites.get([0, 0]))[0]-(self.fps_text.get_width()/1.5), center_pos(self.button_sprites.get([0, 0]))[1]+(-1*self.button_sprites.get([0, 0]).get_height())])
            if self.playing:
                win.blit(self.back_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+(3.2*self.button_sprites.get([0, 0]).get_height())+(3*self.settings[2].current)])
            else:
                win.blit(self.back_text, [center_pos(self.button_sprites.get([0, 0]))[0]+15, center_pos(self.button_sprites.get([0, 0]))[1]+(3.2*self.button_sprites.get([0, 0]).get_height())+(3*self.back_button.current)])
            self.renderer.coin_channel.set_volume(self.settings[0].value/10)
            self.renderer.queue[0].channel.set_volume(self.settings[0].value/10)
        win.blit(self.cursor_img_, cursor_pos)
        if self.auto_save and ((self.cycles%20)==0):
            self.save_system.update(self.renderer)