import pygame as pg
import numpy as np
from numba import njit, prange
import sys
WIN_RES = WIDTH, HEIGHT = 1920, 1080
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
FOCAL_LEN = 250
SCALE = 100
SPEED = 0.1

class Mode7:
    def __init__(self, app, f_tex):
        self.app = app
        self.floor_tex = pg.image.load(f_tex).convert()
        self.tex_size = self.floor_tex.get_size()
        self.floor_array = pg.surfarray.array3d(self.floor_tex)


        self.screen_array = pg.surfarray.array3d(pg.Surface(WIN_RES))

        self.alt = 1.0
        self.angle = 0.0
        self.pos = np.array([0.0, 0.0])

    def update(self):
        self.movement()
        self.screen_array = self.render_frame(self.floor_array, self.screen_array,
                                              self.tex_size, self.angle, self.pos, self.alt)

    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)
        imp = pg.image.load("textures/Sprite.png").convert()
        sx = 32*self.pos[0]*2
        sy = 32*self.pos[0]*2
        if sx <= 0: sx = 32*0.1
        if sy <= 0: sy = 32*0.1
        print(self.pos[0])
        if sx <= 350: self.app.screen.blit(pg.transform.scale(imp, (sx, sy)), (HALF_WIDTH-(self.pos[1]*200)-(self.angle*1000), HALF_HEIGHT))

    @staticmethod
    @njit(fastmath=True, parallel=True)
    def render_frame(floor_array, screen_array, tex_size, angle, player_pos, alt):
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
                #ceil_x = alt * px / z - player_pos[1] * 0.3
                #ceil_y = alt * py / z + player_pos[0] * 0.3
                #ceil_pos = int(ceil_x * SCALE % tex_size[0]), int(ceil_y * SCALE % tex_size[1])
                #depth = 4 * abs(z) / HALF_HEIGHT
                depth = min(max(2.5 * (abs(z) / HALF_HEIGHT), 0), 1)
                fog = (1 - depth) * 230
                floor_col = (floor_col[0] * depth + fog,
                             floor_col[1] * depth + fog,
                             floor_col[2] * depth + fog)
                screen_array[i, j] = floor_col
                new_alt += alt
        return screen_array

    def movement(self):
        keys = pg.key.get_pressed()
        sin_a = np.sin(self.angle)
        cos_a = np.cos(self.angle)
        dx, dy = 0, 0
        speed_sin = SPEED * sin_a
        speed_cos = SPEED * cos_a

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
        self.pos[0] += dx
        self.pos[1] += dy

        if keys[pg.K_LEFT]:
            self.angle -= SPEED/2
        if keys[pg.K_RIGHT]:
            self.angle += SPEED/2

        if keys[pg.K_q]:
            self.alt += SPEED
        if keys[pg.K_e]:
            self.alt -= SPEED
        self.alt = min(max(self.alt, 0.3), 4.0)

class PersudoWindow:
    def __init__(self, floor_tex):
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.mode7 = Mode7(self, floor_tex)

    def update(self):
        self.mode7.update()
        self.clock.tick()
        pg.display.set_caption(f'{self.clock.get_fps() : .1f}')

    def draw(self):
        self.mode7.draw()
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


if __name__ == '__main__':
    app = PersudoWindow('textures/floor_1.png')
    while True: app.run()