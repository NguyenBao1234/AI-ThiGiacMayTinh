from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class AlbumHUD(Screen):
    def __init__(self, **kwargs):
        super(AlbumHUD, self).__init__(**kwargs)

        self.name = 'AlbumHUD'
        self.DictHUD = BoxLayout(orientation='vertical')
        self.DictHUD.add_widget(Button(size=(50,50)))
        self.add_widget(self.DictHUD)
