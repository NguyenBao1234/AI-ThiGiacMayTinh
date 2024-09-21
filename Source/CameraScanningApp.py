from kivy.uix.screenmanager import ScreenManager

from CameraHUD import CameraHUD
from AlbumHUD import AlbumHUD
from kivy.app import App

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CameraHUD())
        sm.add_widget(AlbumHUD())
        return sm

MyApp().run()
