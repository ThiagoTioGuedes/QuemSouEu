import os
from kivy.core.audio import SoundLoader

class SoundManager:
    def __init__(self):
        self.sound = carregar_som('sound.wav')
        
    def toca_som(self):
        if self.sound:
            self.sound.play()


def carregar_som(nome_som):
    return SoundLoader.load('Assets'+os.sep+nome_som)
    



    