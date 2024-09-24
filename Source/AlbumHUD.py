from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from _functools import partial
from FuncrionLibrary import GetImageAt
from FuncrionLibrary import AmountImage
from FuncrionLibrary import PlayInforObject
from kivy.graphics.texture import Texture
import cv2

class AlbumHUD(Screen):
    def __init__(self, **kwargs):
        super(AlbumHUD, self).__init__(**kwargs)

        self.name = 'AlbumHUD'
        self.AlbumLayout = FloatLayout()
        self.DisplayImage = Image(source=GetImageAt(0), allow_stretch=True, keep_ratio=True)
        self.AlbumLayout.add_widget(self.DisplayImage)
        self.add_widget(self.AlbumLayout)
        self.bLeftSwipe = False
        self.bRightSwipe = False
        self.bDownSwipe = False
        self.IndexImage = 0

        # Cài đạt hệ thống nhận diện
        self.classNames = []
        self.classFile = '../ModelObjectDetection/coco.names'
        with open(self.classFile, 'rt') as f:
            self.classNames = f.read().rstrip('\n').split('\n')
        self.configPath = '../ModelObjectDetection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.weightsPath = '../ModelObjectDetection/frozen_inference_graph.pb'
        self.net = cv2.dnn.DetectionModel(self.weightsPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        # TMap : key = <tuple(box)>; value = <button>
        self.object_buttons = {}

    def on_enter(self, *args):
        image = cv2.imread(self.DisplayImage.source)
        RefreshInforBtn(self, image)

    def on_touch_move(self, touch):
        if (touch.x - touch.ox) > 200:
            self.bRightSwipe = True
        elif (touch.x - touch.ox) < -200:
            self.bLeftSwipe = True
        elif (touch.y - touch.oy) <-200:
            self.bDownSwipe = True

    def on_touch_up(self, touch):
        if self.bDownSwipe:
            self.manager.transition.direction = 'down'
            self.manager.current = 'CameraHUD'
            self.bDownSwipe = False
        else:
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
                    image = cv2.imread(self.DisplayImage.source)
                    RefreshInforBtn(self,image)

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
                    image = cv2.imread(self.DisplayImage.source)
                    RefreshInforBtn(self, image)

def RefreshInforBtn(self,image):
    current_objects = []
    classIds, confs, bbox = self.net.detect(image, confThreshold=0.5)
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(image, box, (0, 155, 255), 2)
            current_objects.append(tuple(box))

            '''check to assign <infor button> to < the detected object>'''
            if tuple(box) not in self.object_buttons:
                InforBtn = Button(text=self.classNames[classId - 1].upper(), size_hint=(None, None),
                                  size=(100, 50), pos=(int(box[0]), int(image.shape[0] - box[1] - 50)))
                InforBtn.bind(on_press=partial(PlayInforObject, ObjectName=self.classNames[classId - 1]))
                self.object_buttons[tuple(box)] = InforBtn
                self.AlbumLayout.add_widget(InforBtn)

    for old_box in list(self.object_buttons.keys()):
        if old_box not in current_objects:
            self.AlbumLayout.remove_widget(self.object_buttons[old_box])
            del self.object_buttons[old_box]

    buf = cv2.flip(image, 0).tostring()
    image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
    image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
    self.DisplayImage.texture = image_texture

