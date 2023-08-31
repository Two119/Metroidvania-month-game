from assets.scripts.core_funcs import *
class BulletManager:
    def __init__(self, renderer):
        self.bullets = []
        self.bullet_vel = 8
        if not web:
            self.bullet_sound = pygame.mixer.Sound("assets\Audio\\fireball.ogg")
            self.bullet_spritesheet = SpriteSheet(scale_image(pygame.image.load("assets\Spritesheets\\fireball.png").convert(), 4/3), [4, 1], [255, 255, 255])
        else:
            self.bullet_sound = pygame.mixer.Sound("assets/Audio/fireball.ogg")
            self.bullet_spritesheet = SpriteSheet(scale_image(pygame.image.load("assets/Spritesheets/fireball.png").convert(), 4/3), [4, 1], [255, 255, 255])
        self.delay = 0
        self.frame = 0
        self.renderer = renderer
        self.remove = False
        self.channel = pygame.mixer.Channel(3)
    def add_bullet(self, pos, angle):
        self.bullets.append([pos, angle, None])
        self.channel.set_volume(self.renderer.coin_channel.get_volume())
        if not self.remove:
            self.channel.play(self.bullet_sound)
    def remove_bullet(self, index):
        self.bullets.pop(index)
    def update_physics(self, renderer):
        if hasattr(renderer, "dt"):
            if renderer.dt != 0:
                self.delay += (1*renderer.dt)
                if round(8/(renderer.dt)) != 0:
                    if int(self.delay) % round(8/(renderer.dt)) == 0:
                        self.frame += 1
                        if self.frame > 3:
                            self.frame = 0
                if self.remove:
                    if len(self.bullets) > 0:
                        self.bullets.pop(len(self.bullets)-1)
                    self.remove = False
                for bullet in self.bullets:
                    bullet[0][0] += self.bullet_vel*math.cos(radians(bullet[1]))*renderer.dt
                    bullet[0][1] += self.bullet_vel*math.sin(radians(bullet[1]))*renderer.dt
    def update_graphics(self, renderer):
        if hasattr(renderer, "dt"):
            if renderer.dt != 0:
                for bullet in self.bullets:
                    bullet_sprite = pygame.transform.rotate(self.bullet_spritesheet.get([self.frame, 0]), 360-bullet[1])
                    bullet[2] = bullet_sprite.get_rect(topleft=[bullet[0][0]-(bullet_sprite.get_width()/2), bullet[0][1]-(bullet_sprite.get_height()/2)])
                    bullet_pos = [bullet[0][0]-(bullet_sprite.get_width()/2), bullet[0][1]-(bullet_sprite.get_height()/2)]
                    win.blit(bullet_sprite, bullet_pos)
                    if not self.bullets.index(bullet) in renderer.queue[0].shots:
                        bullet_mask = pygame.mask.from_surface(bullet_sprite)
                        if bullet_mask.overlap(renderer.queue[0].mask, (renderer.queue[0].pos[0]-bullet_pos[0], renderer.queue[0].pos[1]-bullet_pos[1])) != None:
                            renderer.queue[0].is_alive = False
                            renderer.queue[0].deaths += 1
                    if bullet[2] != None:
                        if not renderer.camera.rect.colliderect(bullet[2]):
                            self.bullets.remove(bullet)
