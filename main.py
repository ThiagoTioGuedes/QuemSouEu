import FileHelper
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty

# biblioteca que foi selecionada pelo usuario, necessario para a sua edicao
biblioteca_selecionada = ''

class EditaBiblioteca(Screen):
    nome_item = ObjectProperty(None)
    lista_itens = ListProperty([])
    lista_view = ObjectProperty(None)
    biblioteca_label = ObjectProperty(None)

    def on_enter(self, *args):
        self.nome_item.text = biblioteca_selecionada

    def criar_item(self):
        self.lista_itens.append(self.nome_item.text)

    def remover_item(self):
        self.lista_itens.remove(self.lista_view.adapter.selection[0].text)



class ListaBiblioteca(Screen):
    nome_biblioteca = ObjectProperty(None)
    lista_bibliotecas = ListProperty([])
    lista_view = ObjectProperty(None)

    def on_enter(self, *args):
        self.lista_bibliotecas = FileHelper.lista_bibliotecas();

    def criar_biblioteca(self):
        self.lista_bibliotecas.append(self.nome_biblioteca.text)
        FileHelper.criar_arquivo(self.nome_biblioteca.text, self.lista_bibliotecas)

    def editar_biblioteca(self):
        global biblioteca_selecionada
        biblioteca_selecionada = self.lista_view.adapter.selection[0].text
        # o pai eh sm, o screenManager
        self.parent.current = 'editaBiblioteca'


class MenuPrincipal(Screen):
    pass


class QuemSouEuApp(App):

    def build(self):
        FileHelper.criar_pasta_bibliotecas()
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuPrincipal(name='menu'))
        sm.add_widget(ListaBiblioteca(name='listaBiblioteca'))
        sm.add_widget(EditaBiblioteca(name='editaBiblioteca'))

        return sm


if __name__ == '__main__':
    QuemSouEuApp().run()
