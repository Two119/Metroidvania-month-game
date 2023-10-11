from assets.scripts.core_funcs import *
class EnemyWizard:
    def __init__(self, position, renderer):
        self.pos = position
        self.staff_pos = [position[0], position[1]]
        self.frame = [0, 0]
        init_color = [92, 105, 159]
        final_colors = [[255, 0, 0], [255, 255, 0], [0, 255, 0], [255, 140, 0]]
        self.type = randint(0, len(final_colors)-1)
        self.final_color = final_colors[self.type]
        self.tile = 115
        self.is_alive = True
        self.levels_unlocked = [0]
        self.shoot_delay = 0
        self.vel = [0, 0]
        self.gravity = 0.48
        self.just_spawned = True
        self.delay = 0
        self.deaths = 0
        self.standing = False
        self.speed = 4
        self.cycles = 0
        self.just_col = []
        self.collided = False
        self.cur_row = [3, 2]
        self.shapeshifting = False
        self.jumping = False
        self.coins = 0
        self.moving = True
        self.shoot_delay = time.time()
        self.chasing = False
        self.sounds = []
        self.sounds_dict = {"land":0, "jump":1}
        self.just_jumped = False
        self.fell = False
        self.harmful = ["Crusher"]
        self.spinning = False
        self.dir = 0
        self.shots = []
        self.particle_surf = None
        staffs = SpriteSheet(scale_image(pygame.image.load("assets/Spritesheets/staffs.png").convert()), [5, 1], [255, 255, 255]).sheet[0]
        #self.walk_particles = Particles(win, )
        if not web:
            sheets = [pygame.image.load("assets\Spritesheets\\right_sheet.png").convert(), pygame.image.load("assets\Spritesheets\\left_sheet.png").convert()]
            [s.set_colorkey([255, 255, 255]) for s in sheets]
            [swap_color(s, [53, 53, 64], [1, 1, 1])  for s in sheets]
            [swap_color(s, init_color, self.final_color)  for s in sheets]
            sheets = [scale_image(s) for s in sheets]
            pygame.mixer.music.load("assets\Audio\land.ogg")
            self.sounds.append(pygame.mixer.Sound("assets\Audio\land.ogg"))
            pygame.mixer.music.load("assets\Audio\jump.ogg")
            self.sounds.append(pygame.mixer.Sound("assets\Audio\jump.ogg"))
            self.spritesheet = SpriteSheet(sheets[0], [4, 11])
            spritesheet_ = SpriteSheet(sheets[1], [4, 11])
            for sheet in spritesheet_.sheet:
                self.spritesheet.sheet.append(sheet)
            self.staff = staffs[randint(0, len(staffs)-1)].copy()
        else:
            sheets = [pygame.image.load("assets/Spritesheets/right_sheet.png").convert(), pygame.image.load("assets/Spritesheets/left_sheet.png").convert()]
            [s.set_colorkey([255, 255, 255]) for s in sheets]
            [swap_color(s, [53, 53, 64], [1, 1, 1])  for s in sheets]
            [swap_color(s, init_color, self.final_color)  for s in sheets]
            sheets = [scale_image(s) for s in sheets]
            pygame.mixer.music.load("assets/Audio/land.ogg")
            self.sounds.append(pygame.mixer.Sound("assets/Audio/land.ogg"))
            pygame.mixer.music.load("assets/Audio/jump.ogg")
            self.sounds.append(pygame.mixer.Sound("assets/Audio/jump.ogg"))
            self.spritesheet = SpriteSheet(sheets[0], [4, 11])
            spritesheet_ = SpriteSheet(sheets[1], [4, 11])
            for sheet in spritesheet_.sheet:
                self.spritesheet.sheet.append(sheet)
            self.staff = staffs[randint(0, len(staffs)-1)].copy()
        self.staff.set_colorkey([255, 255, 255])
        self.orig_staff = self.staff.copy()
        self.just_shot = False
        self.time = time.time()
        self.renderer = renderer
        self.mask = pygame.mask.from_surface(self.spritesheet.get(self.frame))
    def update_animation(self, row, delay_wait, dt):

        self.frame[1] = row
        if self.just_spawned:
            self.frame[1] == 0
            self.delay += (1)
            if time.time() - self.time >= (0.0166667*delay_wait):
                self.frame[0] += 1
                self.time = time.time()
            if self.frame[0] > 3:
                self.frame[1] = 0
                self.frame[0] = 0
                self.just_spawned = False
                if not self.renderer.coin_channel.get_busy():
                    self.renderer.coin_channel.play(self.sounds[self.sounds_dict["land"]])
        else:
            self.delay += (1)
            if time.time() - self.time >= (0.0166667*delay_wait):
                self.frame[0] += 1
                self.time = time.time()
            if self.frame[0] > 3:
                self.frame[0] = 0
    def update_physics(self, renderer, dt):

        if self.pos[1] > (renderer.player_death_limit[renderer.level]+renderer.camera.cam_change[1]):
            self.is_alive = False
            self.t = True
            #reset(self, renderer)
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
                        if not self.renderer.coin_channel.get_busy():
                            self.renderer.coin_channel.play(self.sounds[self.sounds_dict["land"]])
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

        if self.standing:
            #self.chasing = False
            if self.rect.colliderect(renderer.camera.rect):
                if sqrt((self.pos[0]-renderer.queue[0].pos[0])**2) > self.rect.w * 3:
                    if self.pos[0] < renderer.queue[0].pos[0]:
                        self.vel[0] = (self.speed*dt)
                        self.dir = 1
                        self.update_animation(1, 17.7/2, dt)
                    if self.pos[0] > renderer.queue[0].pos[0]:
                        self.vel[0] = 0-(self.speed*dt)
                        self.dir = 0
                        self.update_animation(12, 17.7/2, dt)
                    self.chasing = True
                else:
                    self.vel[0] = 0
                    #self.chasing = False
            self.vel[1] = 0
        else:
            self.vel[1] += (self.gravity*(dt))    
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        for double_list in renderer.standing_masks:
                if (self.mask.overlap(double_list[0], (double_list[1][0]-self.pos[0], double_list[1][1]-self.pos[1])) == None):
                    pass
                else:
                    if self.standing == False:
                        if not self.renderer.coin_channel.get_busy():
                            self.renderer.coin_channel.play(self.sounds[self.sounds_dict["land"]])
                    self.standing = True
                    
                    if not double_list[2] in renderer.queue:
                        self.pos[1] = double_list[1][1]-self.spritesheet.get(self.frame).get_height()+24
                    self.jumping = False
        self.staff_pos = [self.pos[0]+(self.spritesheet.get(self.frame).get_width()/1.2), self.pos[1]+(self.spritesheet.get(self.frame).get_height()/1.9)]
        ang = 290-angle_between([self.staff_pos, renderer.queue[0].staff_pos])
        self.staff = pygame.transform.rotate(self.orig_staff, ang)
        if self.vel[0] == 0 and self.rect.colliderect(renderer.camera.rect) and not self.just_shot and self.standing:
            self.shots.append(len(renderer.bullet_manager.bullets))
            renderer.bullet_manager.add_bullet(self.staff_pos, 270-ang)
            self.just_shot = True
            self.shoot_delay = time.time()
        if time.time()-self.shoot_delay >= 1:
            self.just_shot = False
            self.shoot_delay = time.time()
        self.staff_pos = [self.staff_pos[0]-(self.staff.get_width()/2), self.staff_pos[1]-(self.staff.get_height()/2)]
        if not self.is_alive:
            if renderer.queue.index(self) in renderer.enemies:
                renderer.enemies.remove(renderer.queue.index(self))
            renderer.queue.remove(self)
            particle_sheet = SpriteSheet(self.spritesheet.get(self.frame), [self.spritesheet.get(self.frame).get_width()//4, self.spritesheet.get(self.frame).get_height()//4], [0, 0, 0])
            for j, sheet in enumerate(particle_sheet.sheet):
                for i, surf in enumerate(sheet):
                    if not isequal(surf.get_at([0, 0]), [0, 0, 0]):
                        renderer.queue.append(DeathParticle(surf, [self.pos[0]+(i*4), self.pos[1]+(j*4)], renderer, [0, 0, 0]))
            del self
    def update(self, renderer):
        if renderer.clock.get_fps() != 0:
            if self.just_spawned:
                    self.update_animation(7, 15/2, renderer.dt)
            
            self.standing = False
            #if renderer.clock.get_fps() != 0:
            self.update_physics(renderer, renderer.dt)
            if self.standing and not self.chasing:
                if self.dir == 1:
                    self.update_animation(0, 15/2, renderer.dt)
                else:
                    self.update_animation(11, 15/2, renderer.dt)
            if self.frame[1] == 1:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, 1)
            else:
                self.rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, 1)
            if self.chasing:
                    renderer.queue[0].combat = True
            #pygame.draw.rect(win, [255, 0, 0], self.rect)
            win.blit(self.spritesheet.get(self.frame), self.pos)
            win.blit(self.staff, self.staff_pos)
class Sword:
    def __init__(self, pos, level=4):
        self.pos = pos
        if web:
            self.sprite = scale_image(pygame.image.load("assets/Spritesheets/sword_"+str(level)+".png").convert())
            self.sprite.set_colorkey([255, 255, 255])
            sheet = scale_image(pygame.image.load("assets/Spritesheets/sword_anim_"+str(level)+".png").convert())
            swap_color(sheet, [53, 53, 64], [1, 1, 1])
            self.spritesheet = SpriteSheet(sheet, [7, 2], [255, 255, 255])
        else:
            self.sprite = scale_image(pygame.image.load("assets\Spritesheets\sword_"+str(level)+".png").convert())
            self.sprite.set_colorkey([255, 255, 255])
            sheet = scale_image(pygame.image.load("assets\Spritesheets\sword_anim_"+str(level)+".png").convert())
            swap_color(sheet, [53, 53, 64], [1, 1, 1])
            self.spritesheet = SpriteSheet(sheet, [7, 2], [255, 255, 255])
        swap_color(self.sprite, [53, 53, 64], [1, 1, 1])
        self.attacking = False
        self.attack = None
        self.frame = [0, 0]
        self.dir = 0
        self.level = level
        self.just_hit = False
        self.hit_delay = 1
        self.time = time.time()
    def update(self, renderer):
        
        if not self.attacking:
            win.blit(pygame.transform.flip(self.spritesheet.get([0, 1]), self.dir, False), self.pos)
            self.rect = pygame.transform.flip(self.spritesheet.get([0, 1]), self.dir, False).get_rect(topleft=self.pos)
        else:
  
            if time.time() - self.time >= (0.0166667*10):
                    self.frame[0] += 1
                    self.time = time.time()
            if self.frame[0] > 6:
                self.frame[0] = 0
                self.just_hit = False
            self.mask = pygame.mask.from_surface(pygame.transform.flip(self.spritesheet.get(self.frame), self.dir, False))
            if self.rect.colliderect(renderer.camera.window_rect):
                if self.frame[0]==0:
                        renderer.swoosh_channel.play(renderer.swoosh_sfx)
            self.rect = pygame.transform.flip(self.spritesheet.get([0, 1]), self.dir, False).get_rect(topleft=self.pos)
            if self.mask.overlap(renderer.queue[0].shield.mask, [renderer.queue[0].shield.pos[0]-self.pos[0], renderer.queue[0].shield.pos[1]-self.pos[1]]) == None:
                if self.mask.overlap(renderer.queue[0].mask, [renderer.queue[0].pos[0]-self.pos[0], renderer.queue[0].pos[1]-self.pos[1]])!=None:
                    renderer.queue[0].is_alive = False
                    renderer.queue[0].deaths += 1
                    
            else:
                if renderer.queue[0].using_shield:
                    if renderer.queue[0].shield.health >= 0:
                        if not self.just_hit:
                            renderer.queue[0].shield.health -= self.level
                            renderer.queue[0].shield.health_bar_rect.w -= renderer.queue[0].shield.unit_bar_length*self.level
                            if renderer.queue[0].shield.health > 0:
                                if self.rect.colliderect(renderer.camera.window_rect):
                                    renderer.thwack_channel.play(renderer.hit_sfx)
                            self.just_hit = True
                    else:
                        if self.mask.overlap(renderer.queue[0].mask, [renderer.queue[0].pos[0]-self.pos[0], renderer.queue[0].pos[1]-self.pos[1]])!=None:
                            renderer.queue[0].is_alive = False
                            renderer.queue[0].deaths += 1
                            
                else:
                    if self.mask.overlap(renderer.queue[0].mask, [renderer.queue[0].pos[0]-self.pos[0], renderer.queue[0].pos[1]-self.pos[1]])!=None:
                            renderer.queue[0].is_alive = False
                            renderer.queue[0].deaths += 1
                            
            win.blit(pygame.transform.flip(self.spritesheet.get(self.frame), self.dir, False), self.pos)
       
            
class EnemySwordsman:
    def __init__(self, position, renderer):
        self.pos = position
        self.staff_pos = [position[0], position[1]]
        self.frame = [0, 0]
        self.tex = "enemy_2.png"
        self.tile = 115
        self.is_alive = True
        self.levels_unlocked = [0]
        self.vel = [0, 0]
        self.gravity = 0.48
        self.just_spawned = True
        self.delay = 0
        self.deaths = 0
        self.standing = False
        self.speed = 4
        self.cycles = 0
        self.just_col = []
        self.collided = False
        self.cur_row = [3, 2]
        self.shapeshifting = False
        self.jumping = False
        self.coins = 0
        self.moving = True
        self.chasing = False
        self.sounds = []
        self.sounds_dict = {"land":0, "jump":1}
        self.just_jumped = False
        self.fell = False
        self.harmful = ["Crusher"]
        self.spinning = False
        self.dir = 0
        self.particle_surf = None
        red_color = [202, 89, 84]
        blue_color = [92, 105, 159]
        green_color = [85, 125, 85]
        colors = [red_color, blue_color, green_color]
        #self.walk_particles = Particles(win, )
        if not web:
            sheets = [pygame.image.load("assets\Spritesheets\\"+self.tex).convert()]
            [s.set_colorkey([255, 255, 255]) for s in sheets]
            [swap_color(s, [53, 53, 64], [1, 1, 1])  for s in sheets]
            [swap_color(s, red_color, colors[randint(0, len(colors)-1)])  for s in sheets]
            sheets = [scale_image(s) for s in sheets]
            pygame.mixer.music.load("assets\Audio\land.ogg")
            self.sounds.append(pygame.mixer.Sound("assets\Audio\land.ogg"))
            pygame.mixer.music.load("assets\Audio\jump.ogg")
            self.sounds.append(pygame.mixer.Sound("assets\Audio\jump.ogg"))
            pygame.mixer.music.load("assets\Audio\crusher_death.ogg")
            self.sounds.append(pygame.mixer.Sound("assets\Audio\crusher_death.ogg"))
            self.spritesheet = SpriteSheet(sheets[0], [4, 22])
        else:
            sheets = [pygame.image.load("assets/Spritesheets/"+self.tex).convert()]
            [s.set_colorkey([255, 255, 255]) for s in sheets]
            [swap_color(s, [53, 53, 64], [1, 1, 1])  for s in sheets]
            [swap_color(s, red_color, colors[randint(0, len(colors)-1)])  for s in sheets]
            sheets = [scale_image(s) for s in sheets]
            pygame.mixer.music.load("assets/Audio/land.ogg")
            self.sounds.append(pygame.mixer.Sound("assets/Audio/land.ogg"))
            pygame.mixer.music.load("assets/Audio/jump.ogg")
            self.sounds.append(pygame.mixer.Sound("assets/Audio/jump.ogg"))
            pygame.mixer.music.load("assets/Audio/crusher_death.ogg")
            self.sounds.append(pygame.mixer.Sound("assets/Audio/crusher_death.ogg"))
            self.spritesheet = SpriteSheet(sheets[0], [4, 22])
        self.renderer = renderer
        self.mask = pygame.mask.from_surface(self.spritesheet.get(self.frame))
        if renderer.level == 0:
            self.weapon = Sword(self.pos, 1)
        if renderer.level == 1:
            p = [1, 1, 1]
            self.weapon = Sword(self.pos, p[randint(0, len(p)-1)])
        if renderer.level == 2:
            p = [1, 2, 2]
            self.weapon = Sword(self.pos, p[randint(0, len(p)-1)])
        if renderer.level == 3:
            p = [4, 3, 3]
            self.weapon = Sword(self.pos, p[randint(0, len(p)-1)])
        if renderer.level == 4:
            p = [3, 4, 4]
            self.weapon = Sword(self.pos, p[randint(0, len(p)-1)])
        self.time = time.time()
    def update_animation(self, row, delay_wait, dt):
        self.frame[1] = row
        if self.just_spawned:
            self.frame[1] == 0
            self.delay += (1)
            if time.time() - self.time >= (0.0166667*delay_wait):
                self.frame[0] += 1
                self.time = time.time()
            if self.frame[0] > 3:
                self.frame[1] = 0
                self.frame[0] = 0
                self.just_spawned = False
                if not self.renderer.coin_channel.get_busy():
                    self.renderer.coin_channel.play(self.sounds[self.sounds_dict["land"]])
        else:
            self.delay += (1)
            if time.time() - self.time >= (0.0166667*delay_wait):
                self.frame[0] += 1
                self.time = time.time()
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
            
                            
        if self.pos[1] > (renderer.player_death_limit[renderer.level]+renderer.camera.cam_change[1]):
            self.is_alive = False
            #reset(self, renderer)
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
                        if not self.renderer.coin_channel.get_busy():
                            self.renderer.coin_channel.play(self.sounds[self.sounds_dict["land"]])
                    if not double_list[2] in renderer.queue:
                        self.pos[1] = double_list[1][1]-self.spritesheet.get(self.frame).get_height()+8
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
        if self.standing:
            #self.chasing = False
            if self.rect.colliderect(renderer.camera.rect):
                if sqrt((self.pos[0]-renderer.queue[0].pos[0])**2) > self.rect.w * 1.5:
                    if self.pos[0] < renderer.queue[0].pos[0]:
                        self.vel[0] = (self.speed*dt)
                        self.dir = 1
                        self.update_animation(1, 17.7/2, dt)
                    if self.pos[0] > renderer.queue[0].pos[0]:
                        self.vel[0] = 0-(self.speed*dt)
                        self.dir = 0
                        self.update_animation(12, 17.7/2, dt)
                    self.chasing = True
                    self.weapon.attacking = False
                    #self.weapon.frame = [0, 0]
                else:
                    self.vel[0] = 0
                    self.weapon.attacking = True
                    #self.chasing = False
            self.vel[1] = 0
            if self.pos[0] < renderer.queue[0].pos[0]:
                self.dir = 1       
            if self.pos[0] > renderer.queue[0].pos[0]:
                self.dir = 0
        else:
            self.vel[1] += (self.gravity*(dt))    
        self.pos[0]+=self.vel[0]
        self.pos[1]+=self.vel[1]
        for double_list in renderer.standing_masks:
                if (self.mask.overlap(double_list[0], (double_list[1][0]-self.pos[0], double_list[1][1]-self.pos[1])) == None):
                    pass
                else:

                    self.standing = True
                    
                    if not double_list[2] in renderer.queue:
                        self.pos[1] = double_list[1][1]-self.spritesheet.get(self.frame).get_height()+8
                    self.jumping = False

        if not self.is_alive:
            if renderer.queue.index(self) in renderer.enemies:
                renderer.enemies.remove(renderer.queue.index(self))
            renderer.queue.remove(self)
            particle_sheet = SpriteSheet(self.spritesheet.get(self.frame), [self.spritesheet.get(self.frame).get_width()//4, self.spritesheet.get(self.frame).get_height()//4], [0, 0, 0])
            for j, sheet in enumerate(particle_sheet.sheet):
                for i, surf in enumerate(sheet):
                    if not isequal(surf.get_at([0, 0]), [0, 0, 0]):
                        renderer.queue.append(DeathParticle(surf, [self.pos[0]+(i*4), self.pos[1]+(j*4)], renderer, [0, 0, 0]))
            del self
    def update(self, renderer):
        if renderer.clock.get_fps() != 0:
            
                if self.just_spawned:
                        self.update_animation(7, 15/2, renderer.dt)
                
                self.standing = False
                #if renderer.clock.get_fps() != 0:
                self.update_physics(renderer, renderer.dt)
                if self.standing and not self.chasing:
                    if self.dir == 1:
                        self.update_animation(0, 15/2, renderer.dt)
                    else:
                        self.update_animation(11, 15/2, renderer.dt)
                if self.frame[1] == 1:
                    self.rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                    self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-3, self.pos[1]-20+(17*3), (12*4)+15, 1)
                else:
                    self.rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, (16*4)+17)
                    self.top_rect = pygame.Rect(self.pos[0]+(22*2)-8-5, self.pos[1]-20+(17*3), (12*4)+15, 1)
                #pygame.draw.rect(win, [255, 0, 0], self.rect)
                win.blit(self.spritesheet.get(self.frame), self.pos)
                if self.dir == 0:
                    self.weapon.pos = [self.pos[0]-40, self.pos[1]+32]
                else:
                    self.weapon.pos = [self.pos[0]+40, self.pos[1]+32]
                if self.chasing:
                    renderer.queue[0].combat = True
                self.weapon.dir = 1-self.dir
                self.weapon.attacking = self.chasing
                if self.rect.colliderect(renderer.queue[0].rect):
                    self.weapon.attacking = True
                self.weapon.update(renderer)
            #win.blit(self.staff, self.staff_pos)
        