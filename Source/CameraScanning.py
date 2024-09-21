import time
from functools import partial

import cv2
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout


class ScanningApp(App):
    def build(self):
        self.HUD = FloatLayout()
        self.title = 'Camera Scanning'
        self.image = Image(allow_stretch=True, keep_ratio=False)
        self.camera = cv2.VideoCapture(0)

        CaptureButton = Button(size_hint=(0.1, 0.1),
                               on_press=self.OnPressCaptureButton,
                               background_normal='../Asset/CaptureNormalButton.png',
                               background_down='../Asset/CapturePressButton.png',
                               border=(3, 3, 3, 3),
                               pos_hint={'center_x': 0.5, 'y': 0})

        ''' button data for each detected object '''
        self.object_buttons = {}

        """SetUpModel"""
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

        Clock.schedule_interval(self.update, 1.0 / 30.0)

        self.HUD.add_widget(self.image)
        self.HUD.add_widget(CaptureButton)
        return self.HUD

    # event chup anh
    def OnPressCaptureButton(self, instance):
        print("CapturePressButton")
        ret, frame = self.camera.read()

        if ret:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            for classID, confidence, box in zip(*self.Dectec(frame)):
                self.DrawBoundingBoxes(frame, classID, confidence, box)
            cv2.imwrite('../ImageCaptured/{}.jpg'.format(timestr), frame)

    def OnPressInforBtn(self, instance, ObjectName):
        print("infor", {ObjectName})

    """update realtime"""

    def update(self, dt):
        ret, frame = self.camera.read()

        if ret:
            current_objects = []
            #self.Dectec(frame)
            classIds, confs, bbox = self.net.detect(frame,confThreshold=0.5)

            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    current_objects.append(tuple(box))
                    self.DrawBoundingBoxes(frame, classId, confidence, box)
                    '''cv2.rectangle(frame, box, (0, 155, 255), 2)
                    cv2.putText(frame, self.classNames[classId - 1].upper(), (box[0] + 10, box[1] + 20),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=2)
                    cv2.putText(frame, str(round(confidence * 100, 2)) + '%', (box[0] + 10, box[1] + 40),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=2)'''
                    """Assign all infor buttons to the dectected object """
                    if tuple(box) not in self.object_buttons:
                        InforBtn = Button(text=self.classNames[classId - 1].upper(), size_hint=(None, None),
                                          size=(100, 50), pos=(int(box[0]), int(frame.shape[0] - box[1] - 50)))
                        InforBtn.bind(on_press=partial(self.OnPressInforBtn, ObjectName=self.classNames[classId - 1]))
                        self.object_buttons[tuple(box)] = InforBtn
                        self.HUD.add_widget(InforBtn)
                    else:
                        self.object_buttons[tuple(box)].pos = (int(box[0]), int(frame.shape[0] - box[1] - 50))
            """remove the undetected object's info button"""
            for old_box in list(self.object_buttons.keys()):
                if old_box not in current_objects:
                    self.HUD.remove_widget(self.object_buttons[old_box])
                    del self.object_buttons[old_box]
            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = image_texture

    def on_stop(self):
        self.camera.release()

    def DrawBoundingBoxes(self, image, classId, confidence, box):
        cv2.rectangle(image, box, (0, 155, 255), 2)
        cv2.putText(image, self.classNames[classId - 1].upper(), (box[0] + 10, box[1] + 20),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=2)
        cv2.putText(image, str(round(confidence * 100, 2)) + '%', (box[0] + 10, box[1] + 40),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=2)

    # Using tuple: MyName: data_detect_tuple
    def Dectec(self, image):
        classIds, confs, bbox = self.net.detect(image, confThreshold=0.5)
        return classIds, confs, bbox


ScanningApp().run()
