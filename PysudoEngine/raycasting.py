import pygame as pg
import numpy as np
from numba import njit
from compressing import *
import sys
read_zip = False

class Scene:
    def __init__(self, sky_path, floor_path, wall_path, size=5, map_path=None, test_exitx=None, test_exity=None, playerx=None, playery=None, enemies=True):
        global read_zip
        self.next = False
        if not read_zip:
            read_zipfile()
            read_zip = True
        pg.init()
        screen = pg.display.set_mode((800,600))
        running = True
        clock = pg.time.Clock()
        pg.mouse.set_visible(False)
        mv = False
        pg.event.set_grab(not mv)

        hres = 250 #horizontal resolution
        halfvres = int(hres*0.375) #vertical resolution/2
        mod = hres/60 #scaling factor (60° fov)

        self.size = size
        if enemies: nenemies = int(size*2) #number of enemies
        else: nenemies = 0
        if map_path != None:
            posx, posy, rot, maph, mapc, exitx, exity = self.grab_map(map_path, size)
        else:
            posx, posy, rot, maph, mapc, exitx, exity = self.gen_map(size)
        if test_exitx != None: exitx = test_exitx
        if test_exity != None: exity = test_exity
        if playerx != None: posx = playerx
        if playery != None: posy = playery
        frame = np.random.uniform(0,1, (hres, halfvres*2, 3))
        #sky = pg.image.load('ceil_4.png')
        sky = pg.image.load(sky_path)
        sky = pg.surfarray.array3d(pg.transform.smoothscale(sky, (720, halfvres*2)))/255
        #floor = pg.surfarray.array3d(pg.image.load('floor_1.png'))/255
        #wall = pg.surfarray.array3d(pg.image.load('floor_0.png'))/255
        floor = pg.surfarray.array3d(pg.image.load(floor_path))/255
        wall = pg.surfarray.array3d(pg.image.load(wall_path))/255
        sprites, spsize, sword, swordsp = get_sprites(hres)
        
        enemies = spawn_enemies(nenemies, maph, size)
        #grab_map("level0.map")
        while running:
            pg.mouse.set_visible(mv)
            ticks = pg.time.get_ticks()/200
            er = min(clock.tick()/500, 0.3)
            if int(posx) == exitx and int(posy) == exity:
                if nenemies < size:
                    print("You got out of the room!")
                    pg.time.wait(1000)
                    running = False
                elif int(ticks%10+0.9) == 0:
                    print("There is still work to do...")
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    mv = not mv
                    pg.event.set_grab(not mv)
                if swordsp != 1 and event.type == pg.MOUSEBUTTONDOWN:
                    swordsp = 1
                    
            frame = new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod, maph, size,
                            wall, mapc, exitx, exity)
            surf = pg.surfarray.make_surface(frame*255)
            
            if len(enemies) != 0:
                enemies = sort_sprites(posx, posy, rot, enemies, maph, size, er/5)
            surf, en = draw_sprites(surf, sprites, enemies, spsize, hres, halfvres, ticks, sword, swordsp)
            surf = pg.transform.scale(surf, (800, 600))
            
            if int(swordsp) > 0:
                if swordsp == 1 and enemies[en][3] > 1 and enemies[en][3] < 10:
                    enemies[en][0] = 0
                    nenemies = nenemies - 1
                swordsp = (swordsp + er*5)%4

            screen.blit(surf, (0,0))
            pg.display.update()
            fps = int(clock.get_fps())
            pg.display.set_caption("Enemies remaining: " + str(nenemies) + " - FPS: " + str(fps))
            posx, posy, rot = self.movement(pg.key.get_pressed(), posx, posy, rot, maph, er)
        else:
            print("Exited Sucessfully")
    
    def get_next(self): return self.next
    
    def movement(self, pressed_keys, posx, posy, rot, maph, et):
        x, y, rot0, diag = posx, posy, rot, 0
        if pg.mouse.get_focused():
            p_mouse = pg.mouse.get_rel()
            rot = rot + np.clip((p_mouse[0])/200, -0.2, .2)

        if pressed_keys[pg.K_UP] or pressed_keys[ord('w')]:
            x, y, diag = x + et*np.cos(rot), y + et*np.sin(rot), 1

        elif pressed_keys[pg.K_DOWN] or pressed_keys[ord('s')]:
            x, y, diag = x - et*np.cos(rot), y - et*np.sin(rot), 1
            
        if pressed_keys[pg.K_LEFT] or pressed_keys[ord('a')]:
            et = et/(diag+1)
            x, y = x + et*np.sin(rot), y - et*np.cos(rot)
            
        elif pressed_keys[pg.K_RIGHT] or pressed_keys[ord('d')]:
            et = et/(diag+1)
            x, y = x - et*np.sin(rot), y + et*np.cos(rot)


        if not(maph[int(x-0.2)][int(y)] or maph[int(x+0.2)][int(y)] or
            maph[int(x)][int(y-0.2)] or maph[int(x)][int(y+0.2)]):
            posx, posy = x, y
            
        elif not(maph[int(posx-0.2)][int(y)] or maph[int(posx+0.2)][int(y)] or
                maph[int(posx)][int(y-0.2)] or maph[int(posx)][int(y+0.2)]):
            posy = y
            
        elif not(maph[int(x-0.2)][int(posy)] or maph[int(x+0.2)][int(posy)] or
                maph[int(x)][int(posy-0.2)] or maph[int(x)][int(posy+0.2)]):
            posx = x
            
        return posx, posy, rot

    def grab_map(self, filepath, size=25):
        maph = []
        mapc = np.random.uniform(0,1, (size,size,3))
        posx, posy, rot = 1.5, np.random.randint(1, size -1)+.5, np.pi/4
        with open(filepath, "r+") as f:
            raw_map = f.readlines()
            for i in raw_map:
                mapx = []
                mapy = []
                mapx = i.split(" ")
                for l in mapx:
                    l = l.removesuffix("\n")
                    l = int(l)
                    mapy.append(l)
                maph.append(mapy)
        while True:
            x = np.random.randint(0, size)
            y = np.random.randint(0, size)
            if maph[y][x] != 1:
                exitx, exity = x, y
                break
        #print(posx, posy, rot, exitx, exity)
        return posx, posy, rot, np.array(maph), mapc, exitx, exity

    def gen_map(self, size):
        mapc = np.random.uniform(0,1, (size,size,3)) 
        maph = np.random.choice([0, 0, 0, 0, 1, 1], (size,size))
        maph[0,:], maph[size-1,:], maph[:,0], maph[:,size-1] = (1,1,1,1)

        posx, posy, rot = 1.5, np.random.randint(1, size -1)+.5, np.pi/4
        x, y = int(posx), int(posy)
        maph[x][y] = 0
        count = 0
        while True:
            testx, testy = (x, y)
            if np.random.uniform() > 0.5:
                testx = testx + np.random.choice([-1, 1])
            else:
                testy = testy + np.random.choice([-1, 1])
            if testx > 0 and testx < size -1 and testy > 0 and testy < size -1:
                if maph[testx][testy] == 0 or count > 5:
                    count = 0
                    x, y = (testx, testy)
                    maph[x][y] = 0
                    if x == size-2:
                        exitx, exity = (x, y)
                        break
                else:
                    count = count+1
        print(mapc)
        print(len(maph[0]))
        return posx, posy, rot, maph, mapc, exitx, exity

def spawn_enemies(number, maph, msize):
    enemies = []
    for i in range(number):
        x, y = np.random.uniform(1, msize-2), np.random.uniform(1, msize-2)
        while (maph[int(x-0.1)%(msize-1)][int(y-0.1)%(msize-1)] or
               maph[int(x-0.1)%(msize-1)][int(y+0.1)%(msize-1)] or
               maph[int(x+0.1)%(msize-1)][int(y-0.1)%(msize-1)] or
               maph[int(x+0.1)%(msize-1)][int(y+0.1)%(msize-1)]):
            x, y = np.random.uniform(1, msize-1), np.random.uniform(1, msize-1)
        angle2p, invdist2p, dir2p = 0, 0, 0 # angle, inv dist, dir2p relative to player
        entype = np.random.choice([0,1]) # 0 zombie, 1 skeleton
        direction = np.random.uniform(0, 2*np.pi) # facing direction
        size = np.random.uniform(7, 10)
        enemies.append([x, y, angle2p, invdist2p, entype, size, direction, dir2p])

    print(len(enemies))
    return np.asarray(enemies)

def get_sprites(hres):
    sheet = pg.image.load('zombie_n_skeleton4.png').convert_alpha()
    sprites = [[], []]
    swordsheet = pg.image.load('sword1.png').convert_alpha() 
    sword = []
    for i in range(3):
        subsword = pg.Surface.subsurface(swordsheet,(i*800,0,800,600))
        sword.append(pg.transform.smoothscale(subsword, (hres, int(hres*0.75))))
        xx = i*32
        sprites[0].append([])
        sprites[1].append([])
        for j in range(4):
            yy = j*100
            sprites[0][i].append(pg.Surface.subsurface(sheet,(xx,yy,32,100)))
            sprites[1][i].append(pg.Surface.subsurface(sheet,(xx+96,yy,32,100)))

    spsize = np.asarray(sprites[0][1][0].get_size())*hres/800

    sword.append(sword[1]) # extra middle frame
    swordsp = 0 #current sprite for the sword
    
    return sprites, spsize, sword, swordsp

def draw_sprites(surf, sprites, enemies, spsize, hres, halfvres, ticks, sword, swordsp):
    #enemies : x, y, angle2p, dist2p, type, size, direction, dir2p
    cycle = int(ticks)%3 # animation cycle for monsters
    if len(enemies) == 0: en0 = 0
    for en in range(len(enemies)):
        if len(enemies) == 0: 
            en0 = en
            return surf, en0-1
        if enemies[en][3] > 10:
            break
        types, dir2p = int(enemies[en][4]), int(enemies[en][7])
        cos2 = np.cos(enemies[en][2])
        scale = min(enemies[en][3], 2)*spsize*enemies[en][5]/cos2
        vert = halfvres + halfvres*min(enemies[en][3], 2)/cos2
        hor = hres/2 - hres*np.sin(enemies[en][2])
        spsurf = pg.transform.scale(sprites[types][cycle][dir2p], scale)
        surf.blit(spsurf, (hor,vert)-scale/2)

    swordpos = (np.sin(ticks)*10*hres/800,(np.cos(ticks)*10+15)*hres/800) # sword shake
    surf.blit(sword[int(swordsp)], swordpos)
    if len(enemies) == 0: 
        en0 = 0
        en = en0
    return surf, en-1

@njit()
def new_frame(posx, posy, rot, frame, sky, floor, hres, halfvres, mod, maph, size, wall, mapc, exitx, exity):
    for i in range(hres):
        rot_i = rot + np.deg2rad(i/mod - 30)
        sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i/mod - 30))
        frame[i][:] = sky[int(np.rad2deg(rot_i)*2%718)][:]

        x, y = posx, posy
        while maph[int(x)%(size-1)][int(y)%(size-1)] == 0:
            x, y = x +0.01*cos, y +0.01*sin

        n = np.sqrt((x-posx)**2+(y-posy)**2)#abs((x - posx)/cos)    
        h = int(halfvres/(n*cos2 + 0.001))

        xx = int(x*3%1*99)        
        if x%1 < 0.02 or x%1 > 0.98:
            xx = int(y*3%1*99)
        yy = np.linspace(0, 3, h*2)*99%99

        shade = 0.3 + 0.7*(h/halfvres)
        if shade > 1:
            shade = 1
            
        ash = 0 
        if maph[int(x-0.33)%(size-1)][int(y-0.33)%(size-1)]:
            ash = 1
            
        if maph[int(x-0.01)%(size-1)][int(y-0.01)%(size-1)]:
            shade, ash = shade*0.5, 0
            
        c = shade*mapc[int(x)%(size-1)][int(y)%(size-1)]
        for k in range(h*2):
            if halfvres - h +k >= 0 and halfvres - h +k < 2*halfvres:
                if ash and 1-k/(2*h) < 1-xx/99:
                    c, ash = 0.5*c, 0
                frame[i][halfvres - h +k] = c*wall[xx][int(yy[k])]
                if halfvres+3*h-k < halfvres*2:
                    frame[i][halfvres+3*h-k] = c*wall[xx][int(yy[k])]
                
        for j in range(halfvres -h): #floor
            n = (halfvres/(halfvres-j))/cos2
            x, y = posx + cos*n, posy + sin*n
            xx, yy = int(x*3%1*99), int(y*3%1*99)

            shade = 0.2 + 0.8*(1-j/halfvres)
            if maph[int(x-0.33)%(size-1)][int(y-0.33)%(size-1)]:
                shade = shade*0.5
            elif ((maph[int(x-0.33)%(size-1)][int(y)%(size-1)] and y%1>x%1)  or
                  (maph[int(x)%(size-1)][int(y-0.33)%(size-1)] and x%1>y%1)):
                shade = shade*0.5

            frame[i][halfvres*2-j-1] = shade*(floor[xx][yy]*2+frame[i][halfvres*2-j-1])/3
            
            if int(x) == exitx and int(y) == exity and (x%1-0.5)**2 + (y%1-0.5)**2 < 0.2:
                ee = j/(10*halfvres)
                frame[i][j:2*halfvres-j] = (ee*np.ones(3)+frame[i][j:2*halfvres-j])/(1+ee)

    return frame

@njit()
def sort_sprites(posx, posy, rot, enemies, maph, size, er):
    if len(enemies) != 0:
        for en in range(len(enemies)):
            cos, sin = er*np.cos(enemies[en][6]), er*np.sin(enemies[en][6])
            enx, eny = enemies[en][0]+cos, enemies[en][1]+sin
            if (maph[int(enx-0.1)%(size-1)][int(eny-0.1)%(size-1)] or
                maph[int(enx-0.1)%(size-1)][int(eny+0.1)%(size-1)] or
                maph[int(enx+0.1)%(size-1)][int(eny-0.1)%(size-1)] or
                maph[int(enx+0.1)%(size-1)][int(eny+0.1)%(size-1)]):
                enx, eny = enemies[en][0], enemies[en][1]
                enemies[en][6] = enemies[en][6] + np.random.uniform(-0.5, 0.5)
            else:
                enemies[en][0], enemies[en][1] = enx, eny
            angle = np.arctan((eny-posy)/(enx-posx))
            if abs(posx+np.cos(angle)-enx) > abs(posx-enx):
                angle = (angle - np.pi)%(2*np.pi)
            angle2= (rot-angle)%(2*np.pi)
            if angle2 > 10.5*np.pi/6 or angle2 < 1.5*np.pi/6:
                dir2p = ((enemies[en][6] - angle -3*np.pi/4)%(2*np.pi))/(np.pi/2)
                enemies[en][2] = angle2
                enemies[en][7] = dir2p
                enemies[en][3] = 1/np.sqrt((enx-posx)**2+(eny-posy)**2+1e-16)
                cos, sin = (posx-enx)*enemies[en][3], (posy-eny)*enemies[en][3]
                x, y = enx, eny
                for i in range(int((1/enemies[en][3])/0.05)):
                    x, y = x +0.05*cos, y +0.05*sin
                    if (maph[int(x-0.02*cos)%(size-1)][int(y)%(size-1)] or
                        maph[int(x)%(size-1)][int(y-0.02*sin)%(size-1)]):
                        enemies[en][3] = 9999
                        break
            else:
                enemies[en][3] = 9999

    enemies = enemies[enemies[:, 3].argsort()]
    return enemies

if __name__ == '__main__':
    write_zipfile()
    scn0 = Scene('ceil_4.png', 'floor_1.png', 'floor_0.png', 6, "level0.map", 4, 3, 2, 3.5, True)
    scn1 = Scene('ceil_4.png', 'floor_1.png', 'floor_0.png', 6, "level0.map", 4, 3, 2, 3.5, False)