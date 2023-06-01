import pygame

pygame.mixer.init()

class Sound:
    def __init__(self, filename):
        self.filename = filename
        pygame.mixer.music.load(self.filename)
    
    def play(self):
        pygame.mixer.music.play()
        