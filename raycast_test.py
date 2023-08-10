from PysudoEngine import *
from random import randint
runner = False

def main():
    global runner
    while room <= 100:
        scn0 = Scene('ceil_4.png', 'floor_1.png', 'floor_0.png', 6, "level0.map", 4, 3, 2, 3.5, False, f'Room: {room}')
        runner = bool(randint(0, 1))
        if runner:
            scn0.spawn_enemy(3, 4, 20)
            scn0.add_effect((0,0,0,128))
        while scn0.running:
            scn0.update_frame()
        else:
            room += 1

if __name__ == '__main__':
    main()