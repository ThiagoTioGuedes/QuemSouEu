import os
from kivy.core.audio import SoundLoader

class SoundManager:
    def __init__(self):
        self.acerto = carregar_som('acerto.wav')
        self.erro = carregar_som('erro.wav')
        
    def toca_acerto(self):
        if self.acerto:
            self.acerto.play()
    
    def toca_erro(self):
        if self.erro:
            self.erro.play()

def carregar_som(nome_som):
    return SoundLoader.load('Assets'+os.sep+nome_som)
    



    