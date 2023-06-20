from GraphicsEngine import *

app = PersudoWindow('textures/floor_1.png', 'textures/ceil_2.png')
s = Sprite('textures/Sprite.png', 0, 0, 10)
sound = Sound3D("sound.wav")
sound.play()
while True: app.run()
