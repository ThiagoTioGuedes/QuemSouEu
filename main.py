import LibraryHelper
import NetHelper
from AssetsHelper import SoundManager
from random import randint
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# biblioteca que foi selecionada pelo usuario, necessario para a sua edicao
biblioteca_selecionada = ''

class ListaBibliotecaParaBaixar(Screen):
    lista_view = ObjectProperty(None)
    lista_bibliotecas = ListProperty([])


    
    def on_enter(self, *args):
        NetHelper.baixar_banco_bibliotecas()
        self.lista_bibliotecas = LibraryHelper.abrir_arquivo_banco_bibliotecas()

    def baixar_biblioteca(self):
        def dismiss(instance):
            self.parent.current = 'editaBiblioteca'

        biblioteca_selecionada = self.lista_view.adapter.selection[0].text
        NetHelper.baixar_biblioteca(self.lista_view.adapter.selection[0].text)
        popup = Popup(title='Sucesso', content=Label(text='Biblioteca '+biblioteca_selecionada+' foi baixada com sucesso'),
                      size_hint=(.65, .65))
        popup.bind(on_dismiss=dismiss)
        popup.open()
        

class Jogo(Screen):
    player = SoundManager()
    contagem = ObjectProperty(None)
    item = ObjectProperty(None)
    lista_itens = []
    tempo_passado = 0
    acertos = 0
    erros = 0
    # variaveis que servirao para contar o tempo entre o comeco e o fim
    inicio_toque = 0
    fim_toque = 0
    
    entrou = False

    def seleciona_item(self):
        self.item.text = self.lista_itens[randint(0, len(self.lista_itens))-1]
    
    def on_touch_down(self, touch):
        self.inicio_toque = self.tempo_passado
    
    def on_touch_up(self, touch):
        self.fim_toque = self.tempo_passado
        # Se foi segurado por 1 segundo ou mais, passa com erro
        if (self.fim_toque - self.inicio_toque) > .5:
            self.player.toca_erro()
        else:
            self.player.toca_acerto()
            self.acertos += 1
        
        self.seleciona_item()

    def on_enter(self, *args):
        self.i = 0
        self.lista_itens = LibraryHelper.abrir_arquivo_biblioteca(biblioteca_selecionada)
        self.seleciona_item()
        self.entrou = True

    def on_leave(self, *args):
        self.entrou = False

    def update(self, dt):
        if self.tempo_passado < 60:
            # as paginas sao criadas no inicio, essa checagem impede que a contagem se inicie antes de entrar nesta pagina
            if self.entrou:
                self.tempo_passado += dt

            self.contagem.text = "{:3.2f}".format(self.tempo_passado)
        else:
            def dismiss(instance):
                self.acertos = 0
                self.erros = 0
                self.parent.current = 'menu'

            self.tempo_passado = 0
            self.entrou = False
            popup = Popup(title='Fim de jogo', content=Label(text='Na categoria '+biblioteca_selecionada+' voce acertou '+str(self.acertos)),
                          size_hint=(.65, .65))
            popup.bind(on_dismiss=dismiss)
            popup.open()




class ListaBibliotecaParaJogar(Screen):
    lista_bibliotecas = ListProperty([])
    lista_view = ObjectProperty(None)

    def on_enter(self, *args):
        self.lista_bibliotecas = LibraryHelper.lista_bibliotecas()

    def jogar(self):
        global biblioteca_selecionada
        biblioteca_selecionada = self.lista_view.adapter.selection[0].text
        self.parent.current = 'jogar'


class EditaBiblioteca(Screen):
    nome_item = ObjectProperty(None)
    lista_itens = ListProperty([])
    lista_view = ObjectProperty(None)
    biblioteca_label = ObjectProperty(None)

    def salvar_biblioteca(self):
        LibraryHelper.criar_arquivo(biblioteca_selecionada, self.lista_itens)

    def on_enter(self, *args):
        self.lista_itens = LibraryHelper.abrir_arquivo_biblioteca(biblioteca_selecionada)
        self.biblioteca_label.text = biblioteca_selecionada

    def criar_item(self):
        if self.nome_item.text != '' and self.nome_item.text not in self.lista_itens:
            self.lista_itens.append(self.nome_item.text)
            self.nome_item.text = ''

    def on_leave(self, *args):
        self.salvar_biblioteca()


    def remover_item(self):
        for item in self.lista_view.adapter.selection:
            self.lista_itens.remove(item.text)
        self.salvar_biblioteca()


class ListaBiblioteca(Screen):
    nome_biblioteca = ObjectProperty(None)
    lista_bibliotecas = ListProperty([])
    lista_view = ObjectProperty(None)

    def on_enter(self, *args):
        self.lista_bibliotecas = LibraryHelper.lista_bibliotecas()

    def criar_biblioteca(self):
        self.lista_bibliotecas.append(LibraryHelper.tratar_nome_biblioteca(self.nome_biblioteca.text))
        LibraryHelper.criar_arquivo(LibraryHelper.tratar_nome_biblioteca(self.nome_biblioteca.text), [])
        self.nome_biblioteca.text = ''

    def editar_biblioteca(self):
        if len(self.lista_view.adapter.selection)>0:
            global biblioteca_selecionada
            biblioteca_selecionada = self.lista_view.adapter.selection[0].text
            # o pai eh sm, o screenManager
            self.parent.current = 'editaBiblioteca'


class MenuPrincipal(Screen):
    pass


class QuemSouEuApp(App):
    def build(self):
        LibraryHelper.criar_pasta_bibliotecas()
        # Create the screen manager
        sm = ScreenManager()
        game = Jogo(name='jogar')

        sm.add_widget(MenuPrincipal(name='menu'))
        sm.add_widget(ListaBiblioteca(name='listaBiblioteca'))
        sm.add_widget(EditaBiblioteca(name='editaBiblioteca'))
        sm.add_widget(ListaBibliotecaParaJogar(name='listaBibliotecaJogar'))
        sm.add_widget(ListaBibliotecaParaBaixar(name='listaBibliotecaBaixar'))
        sm.add_widget(game)

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return sm


if __name__ == '__main__':
    QuemSouEuApp().run()
