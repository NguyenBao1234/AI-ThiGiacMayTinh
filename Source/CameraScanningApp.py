from kivy.uix.screenmanager import ScreenManager

from CameraHUD import CameraHUD
from AlbumHUD import AlbumHUD
from kivy.app import App


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        self.CameraPage = CameraHUD()
        self.AlbumPage = AlbumHUD()
        sm.add_widget(self.CameraPage)
        sm.add_widget(self.AlbumPage)
        return sm

MyApp().run()
