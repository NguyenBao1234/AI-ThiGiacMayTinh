from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import Screen


class AlbumHUD(Screen):
    def __init__(self, **kwargs):
        super(AlbumHUD, self).__init__(**kwargs)

        self.name = 'AlbumHUD'
        self.DictHUD = BoxLayout(orientation='vertical')
        self.DictHUD.add_widget(Camera(play=True))
        self.add_widget(self.DictHUD)
