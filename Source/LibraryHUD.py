from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import Screen


class LibraryHUD(Screen):
    def __init__(self, **kwargs):
        super(LibraryHUD, self).__init__(**kwargs)

        self.name = 'LibraryHUD'
        self.DictHUD = BoxLayout(orientation='vertical')
        self.DictHUD.add_widget(Camera(play=True))
        self.add_widget(self.DictHUD)
