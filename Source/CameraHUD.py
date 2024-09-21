import time
from functools import partial

import cv2
import os
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen


class CameraHUD(Screen):
    def __init__(self, **kwargs):
        super(CameraHUD, self).__init__(**kwargs)
        self.name = 'CameraHUD'

        # Tạo layout cho HUD
        self.HUDLayout = FloatLayout()

        # Tạo widget Image để hiện thị hình ảnh
        self.image = Image(allow_stretch=True, keep_ratio=True)

        self.camera = cv2.VideoCapture(0)

        # Tạo widget Button
        CaptureButton = Button(size_hint=(0.1, 0.1),
                               on_press=self.OnPressCaptureButton,
                               background_normal='../Asset/CaptureNormalButton.png',
                               background_down='../Asset/CapturePressButton.png',
                               border=(3, 3, 3, 3),
                               pos_hint={'center_x': 0.5, 'center_y': 0.1})

        # Tạo Button chuyển đổi giữa camera và thư viện
        latestImgPath = self.LatestImagePath()
        AblumButton = Button(size_hint=(0.1, 0.1),
                             on_press=self.OpenAlbum,
                             background_normal=latestImgPath,
                             border=(3, 3, 3, 3),
                             pos_hint={'center_x': 0.1, 'center_y': 0.1})

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

        self.object_buttons = {}

        # Cập nhật mỗi 1/30 giây
        Clock.schedule_interval(self.update, 1 / 30)

        # Thêm các widget vào layout và HUD
        self.HUDLayout.add_widget(self.image)
        self.HUDLayout.add_widget(CaptureButton)
        self.HUDLayout.add_widget(AblumButton)
        self.add_widget(self.HUDLayout)

    def update(self, dt):
        ret, frame = self.camera.read()
        if ret:
            current_objects = []

            # self.Detect(frame)
            classIds, confs, bbox = self.net.detect(frame, confThreshold=0.5)

            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    current_objects.append(tuple(box))
                    self.DrawBoundingBoxes(frame, classId, confidence, box)
                    """check to Add button into TMap"""
                    if tuple(box) not in self.object_buttons:
                        InforBtn = Button(text=self.classNames[classId - 1].upper(), size_hint=(None, None),
                                          size=(100, 50), pos=(int(box[0]), int(frame.shape[0] - box[1] - 50)))
                        InforBtn.bind(on_press=partial(self.OnPressInforBtn, ObjectName=self.classNames[classId - 1]))
                        self.object_buttons[tuple(box)] = InforBtn
                        self.HUDLayout.add_widget(InforBtn)
                    else:
                        self.object_buttons[tuple(box)].pos = (int(box[0]), int(frame.shape[0] - box[1] - 50))

            """remove the undetected object's info button"""
            for old_box in list(self.object_buttons.keys()):
                if old_box not in current_objects:
                    self.HUDLayout.remove_widget(self.object_buttons[old_box])
                    del self.object_buttons[old_box]

            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = image_texture

    def OnPressCaptureButton(self, instance):

        print("CapturePressButton")
        ret, frame = self.camera.read()

        if ret:
            timestr = time.strftime("%Y%m%d-%H%M%S")

            for classID, confidence, box in zip(*self.Detect(frame)):
                self.DrawBoundingBoxes(frame, classID, confidence, box)
            cv2.imwrite('../ImageCaptured/IMG-{}.jpg'.format(timestr), frame)

    def OpenAlbum(self, instance):
        self.manager.current = 'AlbumHUD'

    def OnPressInforBtn(self, instance, ObjectName):
        print("infor", {ObjectName})

    def DrawBoundingBoxes(self, frame, classId, confidence, box):
        cv2.rectangle(frame, box, (0, 155, 255), 2)
        cv2.putText(frame, self.classNames[classId - 1].upper(), (box[0] + 10, box[1] + 20),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=2)
        cv2.putText(frame, str(round(confidence * 100, 2)) + '%', (box[0] + 10, box[1] + 40),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=2)

    def Detect(self, frame):
        classIds, confs, bbox = self.net.detect(frame, confThreshold=0.5)
        return classIds, confs, bbox

    def LatestImagePath(self):
        imgPathArr = []

        imgFile = '../ImageCaptured'
        for filename in os.listdir(imgFile):
            if filename.endswith('.jpg'):
                imgPath = os.path.join(imgFile, filename)
                imgPathArr.append(imgPath)
        if len(imgPathArr) != 0:
            return imgPathArr[-1]
        else:
            return '../ImageCaptured/whitePic.png'


    def on_stop(self):
        self.camera.release()
