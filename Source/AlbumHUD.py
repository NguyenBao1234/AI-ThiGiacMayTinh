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
import os
class AlbumHUD(Screen):
    def __init__(self, **kwargs):
        super(AlbumHUD, self).__init__(**kwargs)
        #Giao diện
        self.name = 'AlbumHUD'
        self.AlbumLayout = FloatLayout()
        self.DisplayImage = Image(allow_stretch=True, keep_ratio=True)
        self.DeleteBtn = Button(size_hint=(0.1, 0.13),
                            on_press=self.DeleteImage,
                            background_normal='../Asset/DeleteIcon.png',
                            background_down='../Asset/DeleteIcon_pressed.png',
                            pos_hint={'center_x': 0.9, 'center_y': 0.95})
        self.AlbumLayout.add_widget(self.DisplayImage)
        self.AlbumLayout.add_widget(self.DeleteBtn)
        self.add_widget(self.AlbumLayout)
        #Biến cho điều khiển
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


    #Khi mở giao diện album HUD
    def on_enter(self, *args):
        self.DisplayImage.source = GetImageAt(0)
        image = cv2.imread(self.DisplayImage.source)
        RefreshInforBtn(self, image)
    #xử lý điều khiển bằng chạm vào màn hình
    def on_touch_move(self, touch):
        if (touch.x - touch.ox) > 200:
            self.bRightSwipe = True
        elif (touch.x - touch.ox) < -200:
            self.bLeftSwipe = True
        elif (touch.y - touch.oy) <-200:
            self.bDownSwipe = True
    #Chọn trường hợp tương tác dựa vào thao tác chạm vuôt màn hình
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
    def DeleteImage(self,ImagePath):
        # Kiểm tra xem tệp có tồn tại không
        ImagePath = GetImageAt(self.IndexImage)
        if os.path.exists(ImagePath):
            os.remove(ImagePath)
            self.IndexImage -= 1
            print(f"{ImagePath} đã bị xóa.")
            #Mở ảnh khác của thư viện sau khi xóa, nếu thư viện còn ảnh
            if(self.IndexImage<0):
                if(AmountImage()>0):
                    self.IndexImage = 0
                    Source = GetImageAt(0)
                    self.DisplayImage.source = Source
                    image = cv2.imread(self.DisplayImage.source)
                    RefreshInforBtn(self, image)
                else:
                    self.IndexImage = 0
                    self.manager.transition.direction = 'right'
                    self.manager.current = 'CameraHUD'
            else:
                self.DisplayImage.source = GetImageAt(self.IndexImage)
                image = cv2.imread(self.DisplayImage.source)
                RefreshInforBtn(self, image)



#Hàm cập nhập nút bấm trên màn hình
def RefreshInforBtn(self,image):
    current_objects = []
    classIds, confs, bbox = self.net.detect(image, confThreshold=0.5)
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(image, box, (255, 155,0 ), 2)
            current_objects.append(tuple(box))

            '''check to assign <infor button> to < the detected object>'''
            if tuple(box) not in self.object_buttons:
                InforBtn = Button(text=self.classNames[classId - 1].upper(), size_hint=(None, None),
                                  size=(100, 50), pos=(int(box[0]), int(image.shape[0] - box[1] - 50)))
                InforBtn.bind(on_press=partial(AlbumPlayInforObject, indexClassObject=classId - 1))

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
#Hàm gọi phát âm thanh về vật thể
def AlbumPlayInforObject(self, indexClassObject):
    PlayInforObject(indexClassObject)

