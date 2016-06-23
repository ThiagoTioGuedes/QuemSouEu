import LibraryHelper
import NetHelper
from random import randint
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty

# biblioteca que foi selecionada pelo usuario, necessario para a sua edicao
biblioteca_selecionada = ''

class ListaBibliotecaParaBaixar(Screen):
    lista_bibliotecas = []
    lista_view = ObjectProperty(None)

    def on_enter(self, *args):
        NetHelper.baixar_banco_bibliotecas()
        self.lista_bibliotecas = LibraryHelper.abrir_arquivo_banco_bibliotecas()

    def baixar_biblioteca(self):
        NetHelper.baixar_biblioteca(self.lista_view.adapter.selection[0].text)

class Jogo(Screen):
    contagem = ObjectProperty(None)
    item = ObjectProperty(None)
    lista_itens = []
    i = 0
    entrou = False

    def seleciona_item(self):
        self.item.text = self.lista_itens[randint(0, len(self.lista_itens))-1]

    def on_touch_up(self, touch):
        self.seleciona_item()

    def on_enter(self, *args):
        self.i = 0
        self.lista_itens = LibraryHelper.abrir_arquivo_biblioteca(biblioteca_selecionada)
        self.seleciona_item()
        self.entrou = True

    def on_leave(self, *args):
        self.entrou = False;

    def update(self, dt):
        if self.i < 60:
            # as paginas sao criadas no inicio, essa checagem impede que a contagem se inicie antes de entrar nesta pagina
            if self.entrou:
                self.i += dt

            self.contagem.text = "{:3.2f}".format(self.i)
        else:
            self.i = 0
            self.parent.current = 'menu'


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
        self.lista_itens.append(self.nome_item.text)
        self.nome_item.text = ''
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

    def editar_biblioteca(self):
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
        sm.add_widget(game)

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return sm


if __name__ == '__main__':
    QuemSouEuApp().run()
