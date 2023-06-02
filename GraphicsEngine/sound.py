import pygame

pygame.mixer.init()

class Sound:
    def __init__(self, filename, volume=100):
        self.filename = filename
        self.sound = pygame.mixer.Sound(self.filename)
        try:
            volume /= 100
        except ZeroDivisionError:
            volume = 100/100
        self.sound.set_volume(volume)
    
    def play(self):
        self.sound.play()
        