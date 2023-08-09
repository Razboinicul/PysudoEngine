from PysudoEngine import *
from random import randint

if __name__ == '__main__':
    room = 1
    while True:
        scn0 = Scene('ceil_4.png', 'floor_1.png', 'floor_0.png', 6, "level0.map", 4, 3, 2, 3.5, False, f'Room: {room}')
        if bool(randint(0, 1)):
            scn0.spawn_enemy(3, 4, 20)
        while scn0.running:
            scn0.update_frame()
        else:
            room += 1