from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from FuncrionLibrary import GetImageAt
from FuncrionLibrary import AmountImage



class AlbumHUD(Screen):
    def __init__(self, **kwargs):
        super(AlbumHUD, self).__init__(**kwargs)

        self.name = 'AlbumHUD'
        layout = FloatLayout()
        self.DisplayImage = Image(source=GetImageAt(0), allow_stretch=True, keep_ratio=True)
        layout.add_widget(self.DisplayImage)
        self.add_widget(layout)
        self.bLeftSwipe = False
        self.bRightSwipe = False
        self.IndexImage = 0

    def on_touch_move(self, touch):
        if (touch.x - touch.ox) > 50:
            self.bRightSwipe = True
        elif (touch.x - touch.ox) < 50:
            self.bLeftSwipe = True

    def on_touch_up(self, touch):
        if self.bRightSwipe:
            self.IndexImage -= 1
            print(self.IndexImage)
            self.bRightSwipe = False
            if self.IndexImage < 0:
                self.manager.transition.direction = 'right'
                self.manager.current = 'CameraHUD'
                self.IndexImage = 0
            else:
                self.DisplayImage.source = GetImageAt(self.IndexImage)
        elif self.bLeftSwipe:
            self.IndexImage += 1
            print(self.IndexImage)
            self.bLeftSwipe = False
            if self.IndexImage >= AmountImage():
                self.manager.transition.direction = 'left'
                self.manager.current = 'CameraHUD'
                self.IndexImage = 0
            else:
                self.DisplayImage.source = GetImageAt(self.IndexImage)
