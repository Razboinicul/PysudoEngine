from GraphicsEngine import *

app = PersudoWindow('floor_1.png', 'ceil_2.png', camera_modes['FPS'])
#s = Sprite('textures/Sprite.png', 0, 0, 10)
#sound = Sound3D("sound.wav")
r = Rect3D(10, 10, 15, 15, 25)
c = Oval3D(150, 15, 10, 25, 60)
#wsound.play()
app.gameloop()