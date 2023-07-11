import pygame as pg
import pygame_gui as pgui
import numpy as np
from tempfile import gettempdir
from platform import system
import shutil
from zipfile import ZipFile
from numba import njit, prange
import sys, os
pg.font.init()
objects = []
pos = [0, 0]
angle = 0
WIN_RES = WIDTH, HEIGHT = 1920, 1080
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
FOCAL_LEN = 250
SCALE = 100
SPEED = 0.1
pg.mixer.init(channels=2)
if system() == 'Windows': tmpdir = gettempdir() + '\\.getemp'
elif system() == 'Linux': tmpdir = gettempdir() + '/.getemp'
else: tmpdir = gettempdir() + '/.getemp'
camera_modes = {"static":0, "FPS":1, "Rotation-only":2}

def read_zipfile():
    if not os.path.exists(tmpdir): os.mkdir(tmpdir)
    if os.path.exists(tmpdir):
      shutil.rmtree(tmpdir)
      os.mkdir(tmpdir)
    with ZipFile('pack.enres', 'r') as pack:
        pack.extractall(path=tmpdir)
    os.chdir(tmpdir+'/assets')

class Mode7:
    def __init__(self, app, f_tex, c_tex, cmode=1, weapon_col="rect.png", borders=None):
        self.app, self.cmode, self.borders, \
            self.shooting, self.ammo, self.health \
            = app, cmode, borders, False, 150, 100
        self.floor_tex = pg.image.load(f_tex).convert()
        self.tex_size = self.floor_tex.get_size()
        self.floor_array = pg.surfarray.array3d(self.floor_tex)
        self.ceil_tex = pg.image.load(c_tex).convert()
        self.ceil_tex = pg.transform.scale(self.ceil_tex, self.tex_size)
        self.ceil_array = pg.surfarray.array3d(self.ceil_tex)
        self.screen_array = pg.surfarray.array3d(pg.Surface(WIN_RES))
        self.bar = PersudoRect2D(0, 830, 1920, 150)
        if (self.cmode == 1) or (self.cmode == 2):
            self.w1 = pg.image.load("weapon-1.png").convert_alpha()
            self.w2 = pg.image.load("weapon-2.png").convert_alpha()
            self.imp = pg.image.load(weapon_col).convert_alpha()
            self.rect = self.imp.get_rect(topleft = (HALF_WIDTH, HALF_HEIGHT))
        #os.chdir("..")
        self.alt = 10000.0
        self.angle = 0.0
        self.pos = np.array([0.0, 0.0, 1.0])

    def update(self):
        global pos, angle
        self.movement()
        self.screen_array = self.render_frame(self.floor_array, self.ceil_array, self.screen_array,
                                              self.tex_size, self.angle, self.pos, self.alt)
        pos, angle = self.pos, self.angle

    def draw(self, screen, scr_array, extra_text=""):
        pg.surfarray.blit_array(screen, scr_array)
        for i in objects: i.draw(screen, self.pos, self.angle)
        if (self.cmode == 1) or (self.cmode == 2):
            posx = HALF_WIDTH
            posy = HALF_HEIGHT
            WHITE = (255, 255, 255)
            RED = (255, 0, 0)
            self.app.screen.blit(pg.transform.scale(self.imp, (16, 16)), (posx, posy))
            if self.shooting: self.app.screen.blit(self.w2, (HALF_WIDTH, HEIGHT-320))
            else: self.app.screen.blit(self.w1, (HALF_WIDTH, HEIGHT-320))
            #if self.ammo > 0:
            font = pg.font.SysFont('serif', 45)
            text = font.render(f'Ammo: {self.ammo}      Health: {self.health}       {extra_text}', True, WHITE)
            self.app.screen.blit(text, (100, 850))
            #else:
            #    font = pg.font.SysFont('serif', 45)
            #    text = font.render(f'Ammo: {self.ammo}', True, RED)
            #    self.app.screen.blit(text, (100, 850))
                

    @staticmethod
    @njit(fastmath=True, parallel=True)
    def render_frame(floor_array, ceil_array, screen_array, tex_size, angle, player_pos, alt):
        sin, cos = np.sin(angle), np.cos(angle)
        for i in prange(WIDTH):
            new_alt = alt
            for j in range(HALF_HEIGHT, HEIGHT):
                x = HALF_WIDTH - i
                y = j + FOCAL_LEN
                z = j - HALF_HEIGHT + new_alt
                px = (x * cos - y * sin)
                py = (x * sin + y * cos)
                floor_x = px / z - player_pos[1]
                floor_y = py / z + player_pos[0]
                floor_pos = int(floor_x * SCALE % tex_size[0]), int(floor_y * SCALE % tex_size[1])
                floor_col = floor_array[floor_pos]
                ceil_x = alt * px / z - player_pos[1] * 0.3
                ceil_y = alt * py / z + player_pos[0] * 0.3
                ceil_pos = int(ceil_x * SCALE % tex_size[0]), int(ceil_y * SCALE % tex_size[1])
                ceil_col = ceil_array[ceil_pos]
                #depth = 4 * abs(z) / HALF_HEIGHT
                depth = min(max(2.5 * (abs(z) / HALF_HEIGHT), 0), 1)
                fog = (1 - depth) * 230
                #fog = 350
                floor_col = (floor_col[0] * depth + fog,
                             floor_col[1] * depth + fog,
                             floor_col[2] * depth + fog)
                ceil_col = (ceil_col[0] * depth + fog,
                            ceil_col[1] * depth + fog,
                            ceil_col[2] * depth + fog)
                screen_array[i, j] = floor_col
                screen_array[i, -j] = ceil_col
                new_alt += alt/player_pos[2]
        return screen_array

    def movement(self):
        keys = pg.key.get_pressed()
        sin_a = np.sin(self.angle)
        cos_a = np.cos(self.angle)
        dx, dy = 0, 0
        speed_sin = SPEED * sin_a
        speed_cos = SPEED * cos_a
        if self.cmode == 1:
            if keys[pg.K_w]:
                dx += speed_cos
                dy += speed_sin
            if keys[pg.K_s]:
                dx += -speed_cos
                dy += -speed_sin
            if keys[pg.K_a]:
                dx += speed_sin
                dy += -speed_cos
            if keys[pg.K_d]:
                dx += -speed_sin
                dy += speed_cos
            if self.borders != None:
                self.pos[0] = max(self.pos[0]+dx, self.borders[0])
                self.pos[1] = max(self.pos[1]+dy, self.borders[2])
            else:
                self.pos[0] += dx
                self.pos[1] += dy

        if (self.cmode == 1) or (self.cmode == 2):
            if keys[pg.K_x] and not self.shooting and self.ammo > 0:
                self.shooting = True
                for i in objects: 
                    if i != Sound3D and self.rect.colliderect(i.rect):
                        objects.remove(i)
                self.ammo -= 1
                print(self.ammo)
            else:
                self.shooting = False
            if keys[pg.K_LEFT]:
                self.angle -= SPEED/2
            if keys[pg.K_RIGHT]:
                self.angle += SPEED/2

            if keys[pg.K_q]:
                self.pos[2] += SPEED
            if keys[pg.K_e]:
                self.pos[2] -= SPEED
        self.alt = min(max(self.alt, 0.3), 4.0)

class Sprite3D:
    def __init__(self, sprite, x=0, y=0, angle=0) -> None:
        global objects
        self.x, self.y, self.angle = x, y, angle
        self.imp = pg.image.load(sprite).convert_alpha()
        self.rect = self.imp.get_rect(topleft = (x, y))
        self.type = Sprite3D
        objects.append(self)
    
    def draw(self, window, pos, angle):
        sx = 32*pos[0]*2
        sy = 32*pos[0]*2
        if sx <= 0: sx = 32*0.1
        if sy <= 0: sy = 32*0.1
        hx = sx/2
        hy = sy/2
        (-self.angle)
        posx = HALF_WIDTH+self.x-hx-(pos[1]*300)-(angle*1000)
        posy = HALF_HEIGHT+self.y-pos[2]
        imp = pg.transform.scale(self.imp, (sx, sy))
        self.rect = imp.get_rect(topleft = (posx, posy))
        if sx >= 20 and sx <= 500: window.blit(pg.transform.scale(self.imp, (sx, sy)), (posx, posy))

class Rect3D:
    def __init__(self, x=0, y=0, w=10, h=10, angle=0) -> None:
        global objects
        self.x, self.y, self.w, self.h, self.angle = x, y, w, h, angle
        self.RED = (255, 0, 0)
        self.imp = pg.image.load("rect.png").convert()
        self.rect = self.imp.get_rect(topleft = (x, y))
        self.type = Rect3D
        objects.append(self)
    
    def draw(self, window, pos, angle):
        sx = 32*pos[0]+self.w*2
        sy = 32*pos[0]+self.h*2
        if sx <= 0: sx = 32*0.1
        if sy <= 0: sy = 32*0.1
        hx = sx/2
        hy = sy/2
        (-self.angle)
        posx = HALF_WIDTH+self.x-hx-(pos[1]*300)-(angle*1000)
        posy = HALF_HEIGHT+self.y-(pos[2]*20)
        imp = pg.transform.scale(self.imp, (sx, sy))
        self.rect = imp.get_rect(topleft = (posx, posy))
        if sx >= 20 and sx <= 500: window.blit(pg.transform.scale(self.imp, (sx, sy)), (posx, posy))
        if pos[1] == posx: print("colliding")

class Oval3D:
    def __init__(self, x=0, y=0, w=10, h=10, angle=0) -> None:
        global objects
        self.x, self.y, self.w, self.h, self.angle = x, y, w, h, angle
        self.RED = (255, 0, 0)
        self.type = Oval3D
        self.imp = pg.image.load("circle.png").convert_alpha()
        self.rect = self.imp.get_rect(topleft = (x, y))
        objects.append(self)
    
    def draw(self, window, pos, angle):
        sx = 32*pos[0]+self.w*2
        sy = 32*pos[0]+self.h*2
        if sx <= 0: sx = 32*0.1
        if sy <= 0: sy = 32*0.1
        hx = sx/2
        hy = sy/2
        (-self.angle)
        posx = HALF_WIDTH+self.x-hx-(pos[1]*300)-(angle*1000)
        posy = HALF_HEIGHT+self.y-(pos[2]*20)
        imp = pg.transform.scale(self.imp, (sx, sy))
        self.rect = imp.get_rect(topleft = (posx, posy))
        if sx >= 20 and sx <= 500: window.blit(pg.transform.scale(self.imp, (sx, sy)), (posx, posy))

class Text3D:
    def __init__(self, x=0, y=0, text="", size=1000, t_color=(0, 0, 0), f_color=(256, 256, 256)) -> None:
        global objects
        self.x, self.y, self.text, self.size, self.t_color, self.f_color = x, y, text, size, t_color, f_color
        self.type = Text3D
        self.white=(255, 255, 255)
        objects.append(self)
    
    def draw(self, window, pos, angle):
        s = self.size*pos[0]*2
        if s <= 0: s = self.size*0.1
        (-angle)
        posx = HALF_WIDTH+self.x-(pos[1]*300)-(angle*1000)
        posy = HALF_HEIGHT+self.y
        font = pg.font.SysFont('Sans Serif', s)
        text = font.render(self.text, True, self.white)
        #textRect = text.get_rect()
        if s >= 20 and s <= 500: window.blit(text, (posx, posy))

class Sound3D:
    def __init__(self, file, volume=100, x=0, y=0) -> None:
        global objects
        self.file, self.volume, self.x, self.y = file, volume, x, y
        self.sound = pg.mixer.Sound(self.file)
        self.type = Sound3D
        self.sound.set_volume(volume/100)
        objects.append(self)
        self.music_channel = pg.mixer.Channel(0)
    
    def update_volume(self, left_channel, right_channel):
        self.music_channel.set_volume(left_channel/100, right_channel/100)
    
    def draw(self, _w, pos, angle):
        HALF_WIDTH=1920/2
        posx = HALF_WIDTH-self.x-(pos[1]*300)-(angle*1000)
        self.update_volume(HALF_WIDTH-(posx), HALF_WIDTH+(posx))
    
    def play(self): self.sound.play()

class PersudoText2D:
    def __init__(self, x=0, y=0, color=(256, 256, 256), text="") -> None:
        self.color, self.x, self.y, self.text = color, x, y, text
    
    def draw(self, w, _pos, _angle):
        font = pg.font.SysFont('Sans Serif', 30)
        text = font.render(self.text, True, self.color)
        w.blit(text, (self.x, self.y))

class PersudoRect2D:
    def __init__(self, x=0, y=0, w=10, h=10, angle=0) -> None:
        global objects
        self.x, self.y, self.w, self.h, self.angle = x, y, w, h, angle
        self.RED = (255, 0, 0)
        self.imp = pg.image.load("rect.png").convert()
        self.rect = self.imp.get_rect(topleft = (x, y))
        self.type = Rect3D
        objects.append(self)
    
    def draw(self, window, _pos, _angle):
        window.blit(pg.transform.scale(self.imp, (self.w, self.h)), (self.x, self.y))

class PersudoWindow:
    def __init__(self, floor_tex, c_tex, cmode, extra_text="", borders=None):
        read_zipfile()
        self.extra_text = extra_text
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.mode7 = Mode7(self, floor_tex, c_tex, cmode=cmode, borders=borders)

    def update(self):
        self.mode7.update()
        self.clock.tick()
        pg.display.set_caption(f'{self.clock.get_fps() : .1f}')

    def draw(self):
        self.mode7.draw(self.screen, self.mode7.screen_array, self.extra_text)
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def check_event(self):
        for i in pg.event.get():
            if i.type == pg.QUIT or (i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        self.check_event()
        self.get_time()
        self.update()
        self.draw()
    
    def gameloop(self): 
        while True: self.run()

if __name__ == '__main__':
    room = 1
    app = PersudoWindow('floor_1.png', 'ceil_2.png', camera_modes['FPS'], "Room: 0")
    #s = Sprite('textures/Sprite.png', 0, 0, 10)
    #sound = Sound3D("sound.wav")
    r = Rect3D(10, 10, 25, 35, 25)
    c = Oval3D(150, 15, 25, 45, 60)
    #wsound.play()
    while True:
        app.extra_text = f"Room: {int(room)}"
        room += 0.1
        app.run()