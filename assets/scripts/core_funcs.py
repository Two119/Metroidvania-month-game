import pygame, json, asyncio, os, base64
from random import randint
import math
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
spawn_positions = [[64, 5*64], [64, 4.5*64]]

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
def angle_to(points):
    return math.atan2(points[1][1] - points[0][1], points[1][0] - points[0][0])
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
def reset(player, renderer, fell=False):
        
        renderer.levels = [json.load(open("levels.json", "r"))["level_1"], json.load(open("levels.json", "r"))["level_2"]]
        #renderer.level = 0
        renderer.side_rects = []
        renderer.init_render_pos = [[-1, -9.2], [-1, -12.2]]
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
                player.pos = [64, 5*64]
            case 1:
                player.pos = [64, 4.5*64]
        #player.spritesheet = SpriteSheet(spritesheet, sheet_size)
        player.frame = [0, 0]
        player.fell = False
        player.is_alive = True
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