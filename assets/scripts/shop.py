from assets.scripts.core_funcs import *
from assets.scripts.button import *
def buy_shapeshift(args):
    if args[1].coins >= 1:
        args[1].coins -= 1
        args[1].shapeshifts += 3
        args[0].notifications.append(Notification(args[0].purchase_text, 1))
    else:
        args[0].notifications.append(Notification(args[0].poor_text, 2))
def buy(args):
    renderer = args[0]
    price = args[1]
    if args[2] == 0:
        if renderer.queue[0].coins >= price:
            renderer.queue[0].tiles_unlocked.append(117) 
            renderer.queue[0].coins -= price
            args[3].notifications.append(Notification(args[3].purchase_text, 1))
        else:
            args[3].notifications.append(Notification(args[3].poor_text, 2))
    elif args[2] == 1:
        if renderer.queue[0].coins >= price:
            renderer.queue[0].tiles_unlocked.append(118) 
            renderer.queue[0].coins -= price
            args[3].notifications.append(Notification(args[3].purchase_text, 1))
        else:
            args[3].notifications.append(Notification(args[3].poor_text, 2))
    elif args[2] == 2:
        if renderer.queue[0].coins >= price:
            renderer.queue[0].tiles_unlocked.append(121) 
            renderer.queue[0].coins -= price
            args[3].notifications.append(Notification(args[3].purchase_text, 1))
        else:
            args[3].notifications.append(Notification(args[3].poor_text, 2))
    elif args[2] == 3:
        if renderer.queue[0].coins >= price:
            renderer.queue[0].tiles_unlocked.append(6) 
            renderer.queue[0].coins -= price
            args[3].notifications.append(Notification(args[3].purchase_text, 1))
        else:
            args[3].notifications.append(Notification(args[3].poor_text, 2))
    elif args[2] in [4, 5, 6, 7]:
        if renderer.queue[0].coins >= price:
            d = {4:200, 5:201, 6:202, 7:203}
            renderer.queue[0].tiles_unlocked.append(d[args[2]]) 
            renderer.queue[0].using_shield = True
            renderer.queue[0].shield = Shield(renderer.queue[0].pos, args[4])
            renderer.queue[0].coins -= price
            args[3].notifications.append(Notification(args[3].purchase_text, 1))
            renderer.shop.shield_level = args[2]
        else:
            args[3].notifications.append(Notification(args[3].poor_text, 2))
    elif args[2] == 8:
        if renderer.queue[0].coins >= price:
            renderer.queue[0].tiles_unlocked.append(116) 
            renderer.queue[0].coins -= price
            args[3].notifications.append(Notification(args[3].purchase_text, 1))
        else:
            args[3].notifications.append(Notification(args[3].poor_text, 2))
def equip(args):
    renderer = args[0]
    if args[1] == 0:
        renderer.queue[0].tile = 117
        renderer.queue[0].inventory.items = renderer.queue[0].tiles_unlocked
        renderer.queue[0].inventory.current = renderer.queue[0].inventory.items.index(117)
    elif args[1] == 1:
        renderer.queue[0].tile = 118
        renderer.queue[0].inventory.items = renderer.queue[0].tiles_unlocked
        renderer.queue[0].inventory.current = renderer.queue[0].inventory.items.index(118)
    elif args[1] == 2:
        renderer.queue[0].tile = 121
        renderer.queue[0].inventory.items = renderer.queue[0].tiles_unlocked
        renderer.queue[0].inventory.current = renderer.queue[0].inventory.items.index(121)
    elif args[1] == 3:
        renderer.queue[0].tile = 6
        renderer.queue[0].inventory.items = renderer.queue[0].tiles_unlocked
        renderer.queue[0].inventory.current = renderer.queue[0].inventory.items.index(6)
    elif args[1] in [4, 5, 6, 7]:
        d = {4:1, 5:2, 6:3, 7:4}
        renderer.queue[0].using_shield = True
        if not renderer.queue[0].shield.level == d[args[1]]:
            renderer.queue[0].shield = Shield(renderer.queue[0].pos, d[args[1]])
        renderer.shop.shield_level = d[args[1]]
    elif args[1] == 8:
        renderer.queue[0].tile = 116
        renderer.queue[0].inventory.items = renderer.queue[0].tiles_unlocked
        renderer.queue[0].inventory.current = renderer.queue[0].inventory.items.index(116)
    notify = True
    for n in renderer.shop.notifications:
        if n.type == 1 and n.alpha > 192:
            notify = False
    if notify:
        renderer.shop.font.set_bold(True)
        notification_text = renderer.shop.font.render("Equipped "+str(renderer.shop.tile_names_dict[renderer.shop.tiles[args[1]]]), False, [0, 0, 255], [0, 0, 0])
        #notification_text = renderer.shop.font.render("Equipped "+str(renderer.shop.tile_names_dict[renderer.shop.tiles[args[1]]]), False, [0, 0, 255], [0, 0, 0])
        renderer.shop.font.set_bold(False)
        notification_text.set_colorkey([0, 0, 0])
        renderer.shop.notifications.append(Notification(notification_text, 3))
class InfoBar:
    def __init__(self, font:pygame.font.Font):
        self.font = font
        self.tiles = [117, 118, 121, 6, 200, 201, 202, 203, 116]
        self.tile_names_dict = {117: "Spike", 118: "Hidden Spike", 121: "Swinging Axe", 116: "Fire platform", 6: "Standard tile", 200:"Wooden Shield", 201:"Iron Shield", 202:"Golden Shield", 203:"Diamond Shield"}
        self.info_dict = {117: "Ordinary spike, kills enemies and player on contact. Destroyed after killing one enemy.", 118: "Hidden Spike, erupts from ground and kills enemies and player on contact. Destroyed after killing two enemies.", 121: "Swinging axe, kills enemies and player on contact. Permanent but periodically swings high enough to let player or enemies pass.", 116: "Fire Platform, periodically emits blasts of flames which kill player and enemies on contact. Safe to walk accross while not burning.", 6: "Standard ground tile.", 200: "Wooden shield, blocks enemy attacks from killing player. Only blocks attacks if they touch the shield. Has 8 health. Breaks upon reaching 0 health but respawns when player dies and respawns.", 201: "Iron shield, blocks enemy attacks from killing player. Only blocks attacks if they touch the shield. Has 16 health. Breaks upon reaching 0 health but respawns when player dies and respawns.", 202: "Golden shield, blocks enemy attacks from killing player. Only blocks attacks if they touch the shield. Has 24 health. Breaks upon reaching 0 health but respawns when player dies and respawns.", 203: "Diamond shield, blocks enemy attacks from killing player. Only blocks attacks if they touch the shield. Has 32 health. Breaks upon reaching 0 health but respawns when player dies and respawns."}
        self.bg_tex = scale_image(pygame.image.load("assets/Spritesheets/shop_info_bg.png").convert())
        self.bg_tex.set_colorkey([255, 255, 255])
        self.item_names = [self.font.render(self.tile_names_dict[self.tiles[i]], False, [255, 255, 255], [0, 0, 0]) for i in range(len(self.tiles))]
        [item.set_colorkey([0, 0, 0]) for item in self.item_names]
        self.item_descriptions = [self.font.render(self.info_dict[self.tiles[i]], False, [255, 255, 255], [0, 0, 0], 332) for i in range(len(self.tiles))]
        [item.set_colorkey([0, 0, 0]) for item in self.item_descriptions]
        self.current = -1
        self.pos = [860, (720-self.bg_tex.get_height())/2]
    def update(self, renderer):
        win.blit(self.bg_tex, self.pos)
        if self.current != -1:
            win.blit(self.item_names[self.current], [self.pos[0]+16, self.pos[1]+16])
            win.blit(self.item_descriptions[self.current], [self.pos[0]+16, self.pos[1]+48])
class Shop:
    def  __init__(self, renderer):
        self.tiles = [117, 118, 121, 6, 200, 201, 202, 203, 116]
        self.tile_names_dict = {117: "Spike", 118: "Hidden Spike", 121: "Swinging Axe", 116: "Fire platform", 6: "Standard tile", 200:"Wooden Shield", 201:"Iron Shield", 202:"Golden Shield", 203:"Diamond Shield"}
        self.tile_images = [renderer.spikesheet.sheet[0][3].copy(), renderer.spikesheet.sheet[0][3].copy()]
        fb = pygame.image.load("assets/Spritesheets/FireBox.png").convert()
        f = pygame.image.load("assets/Spritesheets/fire.png").convert()
        fb = scale_image(fb)
        f = scale_image(f)
        self.spikesheet = renderer.spikesheet
        self.firebox_sheet = SpriteSheet(fb, [13, 1], [255, 255, 255])
        self.fire_sheet = SpriteSheet(f, [13, 1], [255, 255, 255])
        firebox = self.firebox_sheet.get([0, 0])
        swinging_axe = scale_image(pygame.image.load("assets/Spritesheets/swingin_axe_icon.png").convert())
        swinging_axe.set_colorkey([236, 28, 36])
        self.tile_images.append(swinging_axe)
        self.tile_images.append(renderer.images[6])
        self.shields = [Shield([0, 0], 1), Shield([0, 0], 2), Shield([0, 0], 3), Shield([0, 0], 4)]
        self.shield_level = 1
        surf = pygame.Surface([64, 64])
        surf.blit(self.shields[0].sheet.get([0, 0]), [-30, -36])
        surf.set_colorkey([0, 0, 0])
        self.tile_images.append(surf)
        surf = pygame.Surface([64, 64])
        surf.blit(self.shields[1].sheet.get([0, 0]), [-30, -36])
        surf.set_colorkey([0, 0, 0])
        self.tile_images.append(surf)
        surf = pygame.Surface([64, 64])
        surf.blit(self.shields[2].sheet.get([0, 0]), [-30, -36])
        surf.set_colorkey([0, 0, 0])
        self.tile_images.append(surf)
        surf = pygame.Surface([64, 64])
        surf.blit(self.shields[3].sheet.get([0, 0]), [-30, -36])
        surf.set_colorkey([0, 0, 0])
        self.tile_images.append(surf)
        self.tile_images.append(firebox)
        self.pos = [0, 0]
        self.bg_tex = scale_image(pygame.image.load("assets/Spritesheets/shop_bg.png").convert())
        self.bg_tex.set_colorkey([255, 255, 255])
        self.tile_masks = [pygame.mask.from_surface(i) for i in self.tile_images]
        self.tile_positions = []
        self.font : pygame.font.Font = renderer.font
        self.prices = [5, 10, 25, 0, 3, 8, 16, 25, 30]
        self.item_names = [self.font.render(self.tile_names_dict[self.tiles[i]], False, [255, 255, 255], [0, 0, 0]) for i in range(len(self.tiles))]
        self.price_texts = [self.font.render(str(self.prices[i])+" coins", False, [255, 255, 255], [0, 0, 0]) for i in range(len(self.tiles))]
        [item.set_colorkey([0, 0, 0]) for item in self.item_names]
        [item.set_colorkey([0, 0, 0]) for item in self.price_texts]
        self.firebox_frame = 0
        self.spike_frame = 0
        self.delay = 0
        self.buttons = []
        self.add_heights = [96, 96, 88, 88, 88, 88, 88, 88, 152]
        self.button_sprites = SpriteSheet(scale_image(pygame.image.load("assets/Spritesheets/buy_buttons.png").convert()), [2, 1], [255, 255, 255])
        self.subtract_x = [(self.button_sprites.sheet[0][0].get_width()-self.tile_images[i].get_width())/2 for i in range(len(self.tile_images))]
        self.buy_text = self.font.render("Buy", False, [254, 255, 255], [0, 0, 0])
        self.equip_text = self.font.render("Equip", False, [254, 255, 255], [0, 0, 0])
        self.font.set_bold(True)
        self.poor_text = self.font.render("You are poor!", False, [255, 0, 0], [0, 0, 0])
        self.purchase_text = self.font.render("Purchased successfully!", False, [0, 255, 0], [0, 0, 0])
        self.font.set_bold(False)
        self.buy_text.set_colorkey([0, 0, 0])
        self.equip_text.set_colorkey([0, 0, 0])
        self.poor_text.set_colorkey([0, 0, 0])
        self.purchase_text.set_colorkey([0, 0, 0])
        self.notifications = []
        self.infobar = InfoBar(self.font)
        self.current = -1
    def update(self, renderer):
        x = ((1280-self.bg_tex.get_width())/2)+128
        y = -128
        
        win.blit(self.bg_tex, [96, (720-self.bg_tex.get_height())/2])
        coin_text = self.font.render("Coins: "+str(renderer.queue[0].coins), False, (255, 255, 255), (0, 0, 0))
        coin_text.set_colorkey([0, 0, 0])
        shift_text = self.font.render("Shapeshifts: "+str(renderer.queue[0].shapeshifts), False, (255, 255, 255), (0, 0, 0))
        shift_text.set_colorkey([0, 0, 0])
        #shift_text
        #win.blit(coin_text, [(1280-self.bg_tex.get_width())/2, (720-self.bg_tex.get_height())/2])
        for i in range(len(self.tile_images)):
            if i % 3 == 0:
                y += 192
                x = 224
            if i == 0:
                if self.tiles[i] in renderer.queue[0].tiles_unlocked:
                    win.blit(self.tile_images[i], [x-4, y-8])
                else:
                    self.tile_images[i].set_alpha(96)
                    win.blit(self.tile_images[i], [x-4, y-8])
                    self.tile_images[i].set_alpha(255)
                if not ([x-4, y-8] in self.tile_positions):
                    self.tile_positions.append([x-4, y-8])
                win.blit(self.item_names[i], [x-((self.item_names[i].get_width()-self.tile_images[i].get_width())/2), y+72])
                win.blit(self.price_texts[i], [x-((self.price_texts[i].get_width()-self.tile_images[i].get_width())/2), y+140])
            elif i == 1:
                if self.tiles[i] in renderer.queue[0].tiles_unlocked:
                    win.blit(self.tile_images[i], [x-4, y-8])
                else:
                    self.tile_images[i].set_alpha(96)
                    win.blit(self.tile_images[i], [x-4, y-8])
                    self.tile_images[i].set_alpha(255)
                if not ([x-4, y-8] in self.tile_positions):
                    self.tile_positions.append([x-4, y-8])
                win.blit(self.item_names[i], [x-((self.item_names[i].get_width()-self.tile_images[i].get_width())/2), y+72])
                win.blit(self.price_texts[i], [x-((self.price_texts[i].get_width()-self.tile_images[i].get_width())/2), y+140])
            else:
                if self.tiles[i] in renderer.queue[0].tiles_unlocked:
                    if i != len(self.tile_images) - 1:
                        win.blit(self.tile_images[i], [x, y])
                    else:
                        win.blit(self.tile_images[i], [x, y-64])
                else:
                    self.tile_images[i].set_alpha(96)
                    if i != len(self.tile_images) - 1:
                        win.blit(self.tile_images[i], [x, y])
                    else:
                        win.blit(self.tile_images[i], [x, y-64])
                    self.tile_images[i].set_alpha(255)
                if not ([x, y] in self.tile_positions) and i != len(self.tile_images)-1:
                    self.tile_positions.append([x, y])
                if not ([x, y-64] in self.tile_positions) and i == len(self.tile_images)-1:
                    self.tile_positions.append([x, y-64])
                win.blit(self.item_names[i], [x-((self.item_names[i].get_width()-self.tile_images[i].get_width())/2), y+72])
                if i == 6:
                    win.blit(coin_text, [x-((self.item_names[i].get_width()-self.tile_images[i].get_width())/2)+32, ((720-self.bg_tex.get_height())/2)+30])
                    win.blit(shift_text, [x-((self.item_names[i].get_width()-self.tile_images[i].get_width())/2)+288, ((720-self.bg_tex.get_height())/2)+30])
                    if not hasattr(self, "buy_shapeshift_button"):
                        self.buy_shapeshift_button = Button([x-((self.item_names[i].get_width()-self.tile_images[i].get_width())/2)+480, ((720-self.bg_tex.get_height())/2)+10], [self.button_sprites.sheet[0][0].copy(), self.button_sprites.sheet[0][1].copy()], [buy_shapeshift, [self, renderer.queue[0]]], win)
                win.blit(self.price_texts[i], [x-((self.price_texts[i].get_width()-self.tile_images[i].get_width())/2), y+140])
            x += 192
        self.current = -1
        for i in range(len(self.tile_masks)):
            if cursor_mask.overlap(self.tile_masks[i], (self.tile_positions[i][0]-pygame.mouse.get_pos()[0], self.tile_positions[i][1]-pygame.mouse.get_pos()[1])) != None:
                self.current = i
                if i == len(self.tile_images)-1:
                    pygame.draw.rect(win, [234, 212, 170], pygame.Rect(self.tile_positions[i][0], self.tile_positions[i][1]+32, 64, 96))
                    win.blit(self.firebox_sheet.get([self.firebox_frame, 0]), self.tile_positions[i]) 
                    win.blit(self.fire_sheet.get([self.firebox_frame, 0]), self.tile_positions[i]) 
                    if renderer.clock.get_fps() != 0:
                        self.delay += (1*(60/renderer.clock.get_fps()))
                        if int(self.delay)%round(16/(60/renderer.clock.get_fps()))==0:
                            self.firebox_frame += 1
                            if self.firebox_frame > 12:
                                self.firebox_frame = 0
                elif i == 1:
                    pygame.draw.rect(win, [234, 212, 170], pygame.Rect(self.tile_positions[i][0], self.tile_positions[i][1], 64, 72))
                    win.blit(self.spikesheet.get([self.spike_frame, 0]), self.tile_positions[i]) 
                    win.blit(self.spikesheet.get([self.spike_frame, 0]), self.tile_positions[i]) 
                    if renderer.clock.get_fps() != 0:
                        self.delay += (1*(60/renderer.clock.get_fps()))
                        if int(self.delay)%round(10/(60/renderer.clock.get_fps()))==0:
                            self.spike_frame += 1
                            if self.spike_frame > 3:
                                self.spike_frame = 0
                else:
                    win.blit(self.tile_images[i], self.tile_positions[i])
        if self.buttons == []:
            self.buttons = [Button([self.tile_positions[i][0]-self.subtract_x[i], self.tile_positions[i][1]+self.add_heights[i]], [self.button_sprites.sheet[0][0].copy(), self.button_sprites.sheet[0][1].copy()], [buy, [renderer, self.prices[i], i, self]], win) for i in range(len(self.tile_positions))]
            self.buttons[len(self.buttons)-2].args.append(1)
            self.buttons[len(self.buttons)-3].args.append(2)
            self.buttons[len(self.buttons)-4].args.append(3)
            self.buttons[len(self.buttons)-5].args.append(4)
            self.equip_buttons = [Button([self.tile_positions[i][0]-self.subtract_x[i], self.tile_positions[i][1]+self.add_heights[i]], [self.button_sprites.sheet[0][0].copy(), self.button_sprites.sheet[0][1].copy()], [equip, [renderer, i]], win) for i in range(len(self.tile_positions))]
            self.equip_buttons[len(self.equip_buttons)-2].args.append(1)
            self.equip_buttons[len(self.equip_buttons)-3].args.append(2)
            self.equip_buttons[len(self.equip_buttons)-4].args.append(3)
            self.equip_buttons[len(self.equip_buttons)-5].args.append(4)
            [self.buttons[i].textures[0].blit(self.buy_text, [(self.buttons[i].textures[0].get_width()-self.buy_text.get_width())/2, 12]) for i in range(len(self.buttons))]
            [self.buy_shapeshift_button.textures[i].blit(self.buy_text, [(self.buy_shapeshift_button.textures[0].get_width()-self.buy_text.get_width())/2, 12]) for i in range(0, 1)]
            [self.buy_shapeshift_button.textures[i].blit(self.buy_text, [(self.buy_shapeshift_button.textures[1].get_width()-self.buy_text.get_width())/2, 16]) for i in range(1, 2)]
            [self.buttons[i].textures[1].blit(self.buy_text, [(self.buttons[i].textures[1].get_width()-self.buy_text.get_width())/2, 16]) for i in range(len(self.buttons))]
            [self.equip_buttons[i].textures[0].blit(self.equip_text, [(self.equip_buttons[i].textures[0].get_width()-self.equip_text.get_width())/2, 12]) for i in range(len(self.equip_buttons))]
            [self.equip_buttons[i].textures[1].blit(self.equip_text, [(self.equip_buttons[i].textures[1].get_width()-self.equip_text.get_width())/2, 16]) for i in range(len(self.equip_buttons))]
        else:
            for i in range(len(self.buttons)):
                if not ((self.tiles[self.buttons[i].args[2]] in renderer.queue[0].tiles_unlocked) or self.tiles[i]==6):
                    self.buttons[i].update(renderer)
                    if self.buttons[i].current == 1:
                        self.current = i
                else:
                    self.equip_buttons[i].update(renderer)
                    self.equip_buttons[i].update(renderer)
                    if self.equip_buttons[i].current == 1:
                        self.current = i
        self.buy_shapeshift_button.update(renderer)
        for notification in self.notifications:
            if renderer.clock.get_fps() != 0:
                notification.update((60/renderer.clock.get_fps()))
                if notification.alpha < 0:
                    self.notifications.remove(notification)
        self.infobar.current = self.current
        self.infobar.update(renderer)
                
                
        

        