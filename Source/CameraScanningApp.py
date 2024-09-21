from kivy.uix.screenmanager import ScreenManager

from CameraHUD import CameraHUD
from LibraryHUD import LibraryHUD
from kivy.app import App

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CameraHUD())
        sm.add_widget(LibraryHUD())
        return sm

MyApp().run()
