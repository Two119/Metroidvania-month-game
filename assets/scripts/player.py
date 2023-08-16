from assets.scripts.core_funcs import *
class Player:
    def __init__(self, position, spritesheet, sheet_size):
        self.pos = position
        self.frame = [0, 0]
        self.tile = 115
        self.is_alive = True
        self.levels_unlocked = [0]
        self.vel = [0, 0]
        self.gravity = 0.24
        self.just_spawned = True
        self.delay = 0
        self.deaths = 0
        self.standing = False
        self.speed = 3
        self.cycles = 0
        self.just_col = []
        self.collided = False
        self.cur_row = [3, 2]
        self.shapeshifting = False
        self.jumping = False
        self.coins = 0
        self.moving = True
        self.channel = pygame.mixer.Channel(1)
        self.channel.set_volume(0.5)
        self.sounds = []
        self.sounds_dict = {"land":0, "jump":1}
        self.just_jumped = False
        self.fell = False
        self.harmful = ["Crusher"]
        self.spinning = False
        self.dir = 0
        if not web:
            sheets = [pygame.image.load("assets\Spritesheets\\right_sheet.png").convert(), pygame.image.load("assets\Spritesheets\\left_sheet.png").convert()]
            [s.set_colorkey([255, 255, 255]) for s in sheets]
            sheets = [scale_image(s) for s in sheets]
            pygame.mixer.music.load("assets\Audio\land.ogg")
            self.sounds.append(pygame.mixer.Sound("assets\Audio\land.ogg"))
            pygame.mixer.music.load("assets\Audio\jump.ogg")
            self.sounds.append(pygame.mixer.Sound("assets\Audio\jump.ogg"))
            pygame.mixer.music.load("assets\Audio\crusher_death.ogg")
            self.sounds.append(pygame.mixer.Sound("assets\Audio\crusher_death.ogg"))
            self.spritesheet = SpriteSheet(sheets[0], [4, 11])
            spritesheet_ = SpriteSheet(sheets[1], [4, 11])
            for sheet in spritesheet_.sheet:
                self.spritesheet.sheet.append(sheet)
        else:
            sheets = [pygame.image.load("assets/Spritesheets/right_sheet.png").convert(), pygame.image.load("assets/Spritesheets/left_sheet.png").convert()]
            [s.set_colorkey([255, 255, 255]) for s in sheets]
            sheets = [scale_image(s) for s in sheets]
            pygame.mixer.music.load("assets/Audio/land.ogg")
            self.sounds.append(pygame.mixer.Sound("assets/Audio/land.ogg"))
            pygame.mixer.music.load("assets/Audio/jump.ogg")
            self.sounds.append(pygame.mixer.Sound("assets/Audio/jump.ogg"))
            pygame.mixer.music.load("assets/Audio/crusher_death.ogg")
            self.sounds.append(pygame.mixer.Sound("assets/Audio/crusher_death.ogg"))
            self.spritesheet = SpriteSheet(sheets[0], [4, 11])
            spritesheet_ = SpriteSheet(sheets[1], [4, 11])
            for sheet in spritesheet_.sheet:
                self.spritesheet.sheet.append(sheet)
    def update_animation(self, row, delay_wait, dt):
        if dt != 0:
            if round(delay_wait/(dt)) != 0:
                self.frame[1] = row
                if self.just_spawned:
                    self.frame[1] == 0
                    self.delay += 1
                    if self.delay % round(delay_wait/(dt)) == 0:
                        self.frame[0] += 1
                    
                    if self.frame[0] > 3:
                        self.frame[1] = 0
                        self.frame[0] = 0
                        self.just_spawned = False
                        if not self.channel.get_busy():
                            self.channel.play(self.sounds[self.sounds_dict["land"]])
                else:
                    self.delay += 1
                    if self.delay % round(delay_wait/(dt)) == 0:
                        self.frame[0] += 1
                    if self.frame[0] > 3:
                        self.frame[0] = 0
    def update_physics(self, renderer, dt):
        for obj in renderer.queue:
            if obj.__class__.__name__ in self.harmful:
                if hasattr(obj, "mask"):
                        if (self.mask.overlap(obj.mask, (obj.pos[0]-self.pos[0], obj.pos[1]-self.pos[1])) == None):
                            pass
                        else:
                            if obj.__class__.__name__ == "Crusher":
                                renderer.coin_channel.play(self.sounds[2])
                            self.is_alive = False
                            #reset(self, renderer)
                            self.deaths += 1
                            return
        if self.pos[1] > (renderer.player_death_limit[renderer.level]+renderer.camera.cam_change[1]):
            self.is_alive = False
            #reset(self, renderer)
            self.deaths += 1
            self.fell = True
            return
        if not self.shapeshifting and self.is_alive:
            if (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]) and not(pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]):
                    self.shapeshifting = True
                    renderer.queue_updating = False
                    return
            global def_frame
            self.collided = False
            if not self.standing:
                self.cycles += 1
            self.mask = pygame.mask.from_surface(self.spritesheet.get(self.frame))
            if self.frame[1] == 1:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, 1)
            else:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, 1)
            for double_list in renderer.standing_masks:
                    if (self.mask.overlap(double_list[0], (double_list[1][0]-self.pos[0], double_list[1][1]-self.pos[1])) == None):
                        pass
                    else:
                        self.standing = True
                        if self.jumping:
                            if not self.channel.get_busy():
                                self.channel.play(self.sounds[self.sounds_dict["land"]])
                        if not double_list[2] in renderer.queue:
                            self.pos[1] = double_list[1][1]-100
                        self.jumping = False
                        
            for rect in renderer.side_rects:
                if self.rect.colliderect(rect[0]):
                    if not [rect[0].x, rect[0].y] in self.just_col:
                        self.jumping = False
                        self.just_col.append([rect[0].x, rect[0].y])
                        if rect[1] != 2:
                            self.vel[0] = (0-(self.vel[0]*(dt)))/2
                        else:
                            self.vel[1] = (0-(((self.vel[1])*dt)))/2
                    self.standing = False
                    self.collided = True
                    break
            
            if not self.collided:
                self.just_col = []
            if self.just_jumped:
                if not (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_UP]):
                    self.just_jumped = False
            if self.standing:
                if self.moving:
                    if not self.just_jumped:
                        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_UP]:
                            self.vel[1] = 0-(find_u(128, self.gravity*(dt)))
                            self.update_animation(1, 17.7/2, dt)
                            self.jumping = True
                            self.standing = False
                            renderer.coin_channel.play(self.sounds[self.sounds_dict["jump"]])
                            self.just_jumped = True
                    if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
                        if not self.jumping:
                            self.vel[0] = (0-(self.speed*(dt)))
                        else:
                            self.vel[0] = 0.85*(0-(find_u(25, self.gravity*(dt))))
                        self.update_animation(12, 17.7/2, dt)
                        self.dir = 0
                    elif pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                        if not self.jumping:
                            self.vel[0] = (self.speed*(dt))
                        else:
                            self.vel[0] = 0.85*((find_u(25, self.gravity*(dt))))
                        self.update_animation(1, 17.7/2, dt)
                        self.dir = 1
                    else:
                        self.vel[0] = 0
                else:
                    self.vel = [0, 0]
                if not self.jumping:
                    self.vel[1] = 0     
                
            else:
                self.vel[1] += (self.gravity*(dt))    
            self.pos[0]+=self.vel[0]
            self.pos[1]+=self.vel[1]
        else:
            if pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL] and not(pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
                    self.shapeshifting = False
                    renderer.queue_updating = True
                    return
            global def_frame
            self.collided = False
            if not self.standing:
                self.cycles += 1
            self.mask = pygame.mask.from_surface(self.spritesheet.get(self.frame))
            if self.frame[1] == 1:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, 1)
            else:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, 1)
            for double_list in renderer.standing_masks:
                    if (self.mask.overlap(double_list[0], (double_list[1][0]-self.pos[0], double_list[1][1]-self.pos[1])) == None):
                        pass
                    else:
                        self.standing = True
                        if self.jumping:
                            if not self.channel.get_busy():
                                self.channel.play(self.sounds[self.sounds_dict["land"]])
                        if not double_list[2] in renderer.queue:
                            self.pos[1] = double_list[1][1]-100
                        self.jumping = False
      
            for rect in renderer.side_rects:
                if self.rect.colliderect(rect[0]):
                    if not [rect[0].x, rect[0].y] in self.just_col:
                        self.jumping = False
                        self.just_col.append([rect[0].x, rect[0].y])
                        if rect[1] != 2:
                            self.vel[0] = (0-(self.vel[0]*(dt)))/2
                        else:
                            self.vel[1] = (0-(((self.vel[1])*dt)))/2
                    self.standing = False
                    self.collided = True
                    break
            
            if not self.collided:
                self.just_col = []
            if self.just_jumped:
                if not (pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_UP]):
                    self.just_jumped = False
            if self.standing:
                if self.moving:
                    if not self.just_jumped:
                        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_UP]:
                            self.vel[1] = 0-(find_u(128, self.gravity*(dt)))
                            self.update_animation(1, 17.7/2, dt)
                            self.jumping = True
                            self.standing = False
                            renderer.coin_channel.play(self.sounds[self.sounds_dict["jump"]])
                            self.just_jumped = True
                    if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
                        if not self.jumping:
                            self.vel[0] = (0-(self.speed*(dt)))
                        else:
                            self.vel[0] = 0.85*(0-(find_u(25, self.gravity*(dt))))
                        self.update_animation(12, 17.7/2, dt)
                        self.dir = 0
                    elif pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                        if not self.jumping:
                            self.vel[0] = (self.speed*(dt))
                        else:
                            self.vel[0] = 0.85*((find_u(25, self.gravity*(dt))))
                        self.update_animation(1, 17.7/2, dt)
                        self.dir = 1
                    else:
                        self.vel[0] = 0
                else:
                    self.vel = [0, 0]
                if not self.jumping:
                    self.vel[1] = 0     
                
            else:
                self.vel[1] += (self.gravity*(dt))    
            self.pos[0]+=self.vel[0]
            self.pos[1]+=self.vel[1]
            if self.frame[1] == 1:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, 1)
            else:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, 1)
        if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.dir = 1
        elif pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
            self.dir = 0
        """
        pygame.draw.rect(win, (255, 0, 0), self.rect)
        if self.frame[1] == 1:
                pygame.draw.rect(win, (0, 0, 255), pygame.Rect(self.pos[0]+(22*2)-8, self.pos[1]-20, (12*4)+15, (16*4)+17))
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8, self.pos[1]-20+(17*3), (12*4)+15, 1)
        else:
            pygame.draw.rect(win, (0, 0, 255), pygame.Rect(self.pos[0]+(22*2)-8-8,  self.pos[1]-20, (12*4)+15, (16*4)+17))
            self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-8, self.pos[1]-20+(17*3), (12*4)+15, 1)
        """
    def update(self, renderer):
        if renderer.clock.get_fps() != 0:
            if self.just_spawned:
                    self.update_animation(7, 15/2, renderer.dt)
            
            self.standing = False
            #if renderer.clock.get_fps() != 0:
            self.update_physics(renderer, renderer.dt)
            if self.standing and not (pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]) and not (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]):
                if self.dir == 1:
                    self.update_animation(0, 15/2, renderer.dt)
                else:
                    self.update_animation(11, 15/2, renderer.dt)
            if self.jumping:
                if self.dir == 1:
                    self.update_animation(3, 60/2, renderer.dt)
                else:
                    self.update_animation(14, 60/2, renderer.dt)
            if self.frame[1] == 1:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, 1)
            else:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, 1)
            #pygame.draw.rect(win, [255, 0, 0], self.rect)
            win.blit(self.spritesheet.get(self.frame), self.pos)