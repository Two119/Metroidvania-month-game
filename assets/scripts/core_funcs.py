import numpy
import pygame, json, asyncio, os, base64, time
from random import randint
import math
from assets.scripts.particles import Particles
from math import sqrt, degrees, radians
if __import__("sys").platform == "emscripten":
    import platform
pygame.init()
global web
web =  False
global cursor_mask
global cursor_img
global button_sound
if not web:
    cursor_img = pygame.image.load("assets\Spritesheets\\cursor.png")
    button_sound = pygame.mixer.Sound("assets\\Audio\\click.ogg")
else:
    cursor_img = pygame.image.load("assets/Spritesheets//cursor.png")
    button_sound = pygame.mixer.Sound("assets/Audio/click.ogg")
cursor_mask = pygame.mask.from_surface(cursor_img)
win = pygame.display.set_mode((1280, 720))
global win_size
win_size = [win.get_width(), win.get_height()]
pygame.display.set_caption("Shiftania")
global spawn_positions
spawn_positions = [[64, -3*64], [64, 4.5*64]]

def max_height_vertical(u, g):
    return (u*u)/(2*g)
def find_u(height, g):
    return sqrt(height*2*g)
def blit_center(img):
    win.blit(img, [win_size[0]-(img.get_width()/2), win_size[1]-(img.get_height()/2)])
def center_pos(img):
    return [win_size[0]/2-(img.get_width()/2), win_size[1]/2-(img.get_height()/2)]
def swap_color(img, col1, col2):
    pygame.transform.threshold(img ,img ,col1, (10, 10, 10), col2, 1, None, True)
def scale_image(img, factor=4.0):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size).convert()
def angle_between(points):
    return math.atan2(points[1][1] - points[0][1], points[1][0] - points[0][0])*180/math.pi
#clip function from daflufflyportato
def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()
class SpriteSheet:
    def __init__(self, sheet, size, colorkey = [0, 0, 0]):
        self.spritesheet = sheet
        self.colorkey = colorkey
        self.size = [self.spritesheet.get_width()/size[0], self.spritesheet.get_height()/size[1]]
        self.sheet = []
        for i in range(size[1]):
            self.sheet.append([])
            for j in range(size[0]):
                image = pygame.Surface((self.size))
                image.set_colorkey(self.colorkey)
                image.blit(self.spritesheet, (0, 0), [j*self.size[0], i*self.size[1], self.size[0], self.size[1]])
                self.sheet[i].append(image)
    def get(self, loc):
        return self.sheet[loc[1]][loc[0]]
class DeathParticle:
    def __init__(self, tex, pos, colkey = [0, 0, 0]):
        self.tex = tex
        self.pos = pos
        self.orig_x = pos[0]*1
        self.colkey = colkey
        self.alpha = 255
        self.colkey = colkey
    def update(self, renderer):
        if self.alpha > 0:
            self.alpha -= (2*renderer.dt)
        self.pos[1] -= (1.5*renderer.dt)
        self.pos[0] = self.orig_x+randint(-5, 5)
        self.tex.set_alpha(self.alpha)
        win.blit(self.tex, [self.pos[0]+renderer.camera.cam_change[0], self.pos[1]])
class Shield:
    def __init__(self, pos, level) -> None:
        self.pos = [pos[0]*1, pos[1]*1]
        self.level = level
        wood_color = [115, 91, 66]
        iron_color = [161, 154, 150]
        gold_color = [238, 181, 81]
        diamond_color = [139, 176, 173]
        level_colors = [wood_color, iron_color, gold_color, diamond_color]
        if web:
            sprite = scale_image(pygame.image.load("assets/Spritesheets/shield_anim.png").convert())
        else:
            sprite = scale_image(pygame.image.load("assets\Spritesheets\shield_anim.png").convert())
        swap_color(sprite, wood_color, level_colors[level-1])
        self.sheet = SpriteSheet(sprite, [4, 3], [255, 255, 255])
        self.frame = [0, 0]
        self.mask = pygame.mask.from_surface(self.sheet.get(self.frame))
        self.health = self.level*8
        self.health_bar_length = 96*self.level
        self.unit_bar_length = self.health_bar_length/self.health
        self.health_bar_rect = pygame.Rect(32, 32, self.health_bar_length, 16)
        self.health_bar_rect_2 = pygame.Rect(32, 32, self.health_bar_length+4, 16)
        self.dead = False
    def update(self, renderer):
        if not self.dead:
            if self.health > 0:
                self.mask = pygame.mask.from_surface(self.sheet.get(self.frame))
                win.blit(self.sheet.get(self.frame), self.pos)
                pygame.draw.rect(win, [255, 0, 0], self.health_bar_rect)
                pygame.draw.rect(win, [255, 255, 255], self.health_bar_rect_2, 4)
                for i in range(self.level*8):
                    pygame.draw.rect(win, [255, 255, 255], pygame.Rect(32+(i*self.unit_bar_length), 32, 4, 16), 4)
            else:
                particle_sheet = SpriteSheet(self.sheet.get(self.frame), [self.sheet.get(self.frame).get_width()//4, self.sheet.get(self.frame).get_height()//4], [0, 0, 0])
                for j, sheet in enumerate(particle_sheet.sheet):
                    for i, surf in enumerate(sheet):
                        renderer.queue.append(DeathParticle(surf, [self.pos[0]+(i*4), self.pos[1]+(j*4)], [0, 0, 0]))
                self.dead = True
def reset(player, renderer, fell=False):
        
        renderer.levels = [json.load(open("levels.json", "r"))["level_1"], json.load(open("levels.json", "r"))["level_2"]]
        #renderer.level = 0
        renderer.side_rects = []
        renderer.init_render_pos = [[-1, -13.2], [-5, 0]]
        #renderer.coin_channel = pygame.mixer.Channel(2)
        renderer.queue = [player]
        renderer.first_cycle = True
        renderer.clock = pygame.time.Clock()
        renderer.coin_appending = True
        renderer.added_coins = 0
        renderer.spikes = []
        renderer.played = False
        renderer.added_spikes = 0
        renderer.added_spikes_h = 0
        renderer.camera.cam_change = [0, 0]
        match renderer.level:
            case 0:
                player.pos = [64, -3*64]
            case 1:
                player.pos = [2816, 5952]
        #player.spritesheet = SpriteSheet(spritesheet, sheet_size)
        player.frame = [0, 0]
        player.fell = False
        player.vel = [0, 0]
        player.gravity = 0.2
        player.just_spawned = True
        player.delay = 0
        player.standing = False
        player.speed = 3
        player.cycles = 0
        player.just_col = []
        player.collided = False
        player.cur_row = [5, 4]
        player.jumping = False
        player.moving = True
        player.just_jumped = False
        renderer.cur_cycle += 1
        renderer.bullet_manager.bullets = []
        renderer.cycles = 0
        player.is_alive = True
        player.shield = Shield(player.pos, renderer.shop.shield_level)
        