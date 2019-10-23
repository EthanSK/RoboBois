import pygame

class SoundManager:
    def __init__(self, volume):
        self.volume = volume

    def rev_engine(self):
        self.play_sound("sounds/rev.mp3")

    def drive(self):
        self.play_sound("sounds/drive.mp3")


    def play_sound(self, file):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play() 
        while pygame.mixer.music.get_busy() == True:
            continue
