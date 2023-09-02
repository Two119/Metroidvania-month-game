from assets.scripts.core_funcs import *
class Inventory:
    def __init__(self, size):
        self.size = size
        self.tile_size = 80
        self.surf = pygame.Surface([size*self.tile_size, self.tile_size])
        self.surf.fill([0, 0, 0])
        self.bg_surf = self.surf.copy()
        self.bg_surf.set_alpha(150)
        self.surf.set_colorkey([0, 0, 0])
        [pygame.draw.rect(self.surf, [108, 108, 108], pygame.Rect(i*self.tile_size, 0, self.tile_size, self.tile_size), 4) for i in range(size)]
        self.rects = [pygame.Rect(((1280-self.bg_surf.get_width())/2)+(i*self.tile_size), 720-self.tile_size, self.tile_size, self.tile_size) for i in range(size)]
        self.items = [6]
        self.spike_dir_list = [117, 129, 138, 139]
        self.hiddenspike_dir_list = [118, 135, 136, 137]
        self.spike_ang_list = [0, 180, 90, -90]
        self.cur_tile = 0
        self.current = 0
    def update(self, renderer):
        win.blit(self.bg_surf, [(1280-self.bg_surf.get_width())/2, 720-self.tile_size])
        win.blit(self.surf, [(1280-self.surf.get_width())/2, 720-self.tile_size])
        index = 0
        for item in self.items:
            if item != 118:
                if self.current < len(self.items):
                    if self.items[self.current] != 117:
                        win.blit(renderer.shop.tile_images[renderer.shop.tiles.index(item)], [((1280-self.surf.get_width())/2)+(self.tile_size*index)+((self.tile_size-64)/2)-4, 720-self.tile_size+((self.tile_size-64)/2)-4])
                    else:
                        if item == 117:
                            s = pygame.transform.rotate(renderer.shop.tile_images[renderer.shop.tiles.index(item)], self.spike_ang_list[self.cur_tile])
                            win.blit(s, [((1280-self.surf.get_width())/2)+(self.tile_size*index)+((self.tile_size-64)/2)-4, 720-self.tile_size+((self.tile_size-64)/2)-4])
                        else:
                            win.blit(renderer.shop.tile_images[renderer.shop.tiles.index(item)], [((1280-self.surf.get_width())/2)+(self.tile_size*index)+((self.tile_size-64)/2)-4, 720-self.tile_size+((self.tile_size-64)/2)-4])
                else:
                    win.blit(renderer.shop.tile_images[renderer.shop.tiles.index(item)], [((1280-self.surf.get_width())/2)+(self.tile_size*index)+((self.tile_size-64)/2)-4, 720-self.tile_size+((self.tile_size-64)/2)-4])
            
            else:
                renderer.shop.tile_images[renderer.shop.tiles.index(item)].set_alpha(96)
                if self.current < len(self.items):
                    if self.items[self.current] == 118:
                        s = pygame.transform.rotate(renderer.shop.tile_images[renderer.shop.tiles.index(item)], self.spike_ang_list[self.cur_tile])
                    else:
                        s = renderer.shop.tile_images[renderer.shop.tiles.index(item)]
                else:
                    s = renderer.shop.tile_images[renderer.shop.tiles.index(item)]
                win.blit(s, [((1280-self.surf.get_width())/2)+(self.tile_size*index)+((self.tile_size-64)/2)-4, 720-self.tile_size+((self.tile_size-64)/2)-4])
                renderer.shop.tile_images[renderer.shop.tiles.index(item)].set_alpha(255)
            index+=1
        index = 0
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and self.current != index:
                self.current = index
                if self.current < len(self.items):
                    self.cur_tile = 0
                    renderer.queue[0].tile = self.items[self.current]
                break
            index += 1
        if self.current < len(self.items):
            if self.items[self.current] == 117:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    self.cur_tile = 2
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self.cur_tile = 3
                if pygame.key.get_pressed()[pygame.K_UP]:
                    self.cur_tile = 0
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.cur_tile = 1
                renderer.queue[0].tile = self.spike_dir_list[self.cur_tile]
            if self.items[self.current] == 118:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    self.cur_tile = 2
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self.cur_tile = 3
                if pygame.key.get_pressed()[pygame.K_UP]:
                    self.cur_tile = 0
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.cur_tile = 1
                renderer.queue[0].tile = self.hiddenspike_dir_list[self.cur_tile]
        pygame.draw.rect(win, [85, 85, 85], pygame.Rect(((1280-self.surf.get_width())/2)+(self.current*self.tile_size), (720-self.tile_size), self.tile_size, self.tile_size), 8)
class Player:
    def __init__(self, position, spritesheet, sheet_size):
        self.pos = position
        self.staff_pos = [position[0], position[1]]
        self.frame = [0, 0]
        self.tile = 115
        self.tiles_unlocked = []
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
        self.shots = []
        self.particle_surf = None
        self.just_shot = False
        self.staffs = SpriteSheet(scale_image(pygame.image.load("assets/Spritesheets/staffs.png").convert()), [5, 1], [255, 255, 255])
        #self.walk_particles = Particles(win, )
        if not web:
            sheets = [pygame.image.load("assets\Spritesheets\\right_sheet.png").convert(), pygame.image.load("assets\Spritesheets\\left_sheet.png").convert()]
            [s.set_colorkey([255, 255, 255]) for s in sheets]
            [swap_color(s, [53, 53, 64], [1, 1, 1])  for s in sheets]
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
            self.staff = self.staffs.get([0, 0]).copy()
        else:
            sheets = [pygame.image.load("assets/Spritesheets/right_sheet.png").convert(), pygame.image.load("assets/Spritesheets/left_sheet.png").convert()]
            [s.set_colorkey([255, 255, 255]) for s in sheets]
            [swap_color(s, [53, 53, 64], [1, 1, 1])  for s in sheets]
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
            self.staff = self.staffs.get([0, 0]).copy()
        self.staff.set_colorkey([255, 255, 255])
        self.orig_staff = self.staff.copy()
        self.just_shot = False
        self.inventory = Inventory(8)
    def update_animation(self, row, delay_wait, dt):
        if dt != 0:
            if round(delay_wait/(dt)) != 0:
                self.frame[1] = row
                if self.just_spawned:
                    self.frame[1] == 0
                    self.delay += (1*dt)
                    if int(self.delay) % round(delay_wait/(dt)) == 0:
                        self.frame[0] += 1
                    
                    if self.frame[0] > 3:
                        self.frame[1] = 0
                        self.frame[0] = 0
                        self.just_spawned = False
                        if not self.channel.get_busy():
                            self.channel.play(self.sounds[self.sounds_dict["land"]])
                else:
                    self.delay += (1*dt)
                    if int(self.delay) % round(delay_wait/(dt)) == 0:
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
                            self.pos[1] = double_list[1][1]-self.spritesheet.get(self.frame).get_height()+24
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
                if not (pygame.key.get_pressed()[pygame.K_SPACE] ):
                    self.just_jumped = False
            if self.standing:
                if self.moving:
                    if not self.just_jumped:
                        if pygame.key.get_pressed()[pygame.K_SPACE] :
                            self.vel[1] = 0-(find_u(128, self.gravity*(dt)))
                            self.update_animation(1, 17.7/2, dt)
                            self.jumping = True
                            self.standing = False
                            renderer.coin_channel.play(self.sounds[self.sounds_dict["jump"]])
                            self.just_jumped = True
                    if pygame.key.get_pressed()[pygame.K_a] :
                        if not self.jumping:
                            self.vel[0] = (0-(self.speed*(dt)))
                        else:
                            self.vel[0] = 0.85*(0-(find_u(25, self.gravity*(dt))))
                        self.update_animation(12, 17.7/2, dt)
                        self.dir = 0
                    elif pygame.key.get_pressed()[pygame.K_d] :
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
                            self.pos[1] = double_list[1][1]-self.spritesheet.get(self.frame).get_height()+24
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
                if not (pygame.key.get_pressed()[pygame.K_SPACE] ):
                    self.just_jumped = False
            if self.standing:
                if self.moving:
                    if not self.just_jumped:
                        if pygame.key.get_pressed()[pygame.K_SPACE] :
                            self.vel[1] = 0-(find_u(128, self.gravity*(dt)))
                            self.update_animation(1, 17.7/2, dt)
                            self.jumping = True
                            self.standing = False
                            renderer.coin_channel.play(self.sounds[self.sounds_dict["jump"]])
                            self.just_jumped = True
                    if pygame.key.get_pressed()[pygame.K_a] :
                        if not self.jumping:
                            self.vel[0] = (0-(self.speed*(dt)))
                        else:
                            self.vel[0] = 0.85*(0-(find_u(25, self.gravity*(dt))))
                        self.update_animation(12, 17.7/2, dt)
                        self.dir = 0
                    elif pygame.key.get_pressed()[pygame.K_d] :
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
        if pygame.key.get_pressed()[pygame.K_d] :
            self.dir = 1
        elif pygame.key.get_pressed()[pygame.K_a] :
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
        self.staff_pos = [self.pos[0]+(self.spritesheet.get(self.frame).get_width()/1.2), self.pos[1]+(self.spritesheet.get(self.frame).get_height()/1.9)]
        ang = 270-angle_between([self.staff_pos, pygame.mouse.get_pos()])
        self.staff = pygame.transform.rotate(self.orig_staff, ang)
        if pygame.mouse.get_pressed()[0] and not self.just_shot and not renderer.button.rect.collidepoint(pygame.mouse.get_pos()) and self.shapeshifting:
            self.shots.append(len(renderer.bullet_manager.bullets))
            renderer.bullet_manager.add_bullet(self.staff_pos, 270-ang)
            self.just_shot = True
        if not pygame.mouse.get_pressed()[0]:
            self.just_shot = False
        self.staff_pos = [self.staff_pos[0]-(self.staff.get_width()/2), self.staff_pos[1]-(self.staff.get_height()/2)]
        
    def update(self, renderer):
        if renderer.clock.get_fps() != 0:
            if self.just_spawned:
                    self.update_animation(7, 15/2, renderer.dt)
            
            self.standing = False
            #if renderer.clock.get_fps() != 0:
            self.update_physics(renderer, renderer.dt)
            if self.standing and not (pygame.key.get_pressed()[pygame.K_a] ) and not (pygame.key.get_pressed()[pygame.K_d] ):
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
            win.blit(self.staff, self.staff_pos)
            self.inventory.items = self.tiles_unlocked
            self.inventory.update(renderer)