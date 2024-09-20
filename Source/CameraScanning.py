import cv2
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture


class ScanningApp(App):
    def build(self):
        self.title = 'Camera Scanning'

        self.image = Image()
        self.camera = cv2.VideoCapture(0)

        self.classNames = []
        self.classFile = '../Object_Detection_Files/coco.names'
        with open(self.classFile, 'rt') as f:
            self.classNames = f.read().rstrip('\n').split('\n')

        self.configPath = '../Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.weightsPath = '../Object_Detection_Files/frozen_inference_graph.pb'

        self.net = cv2.dnn.DetectionModel(self.weightsPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return self.image

    def update(self, dt):
        ret, frame = self.camera.read()

        if ret:
            classIds, confs, bbox = self.net.detect(frame, confThreshold=0.5)

            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    cv2.rectangle(frame, box, (0, 0, 255), 2)
                    cv2.putText(frame, self.classNames[classId - 1].upper(), (box[0] + 10, box[1] + 20),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=2)
                    cv2.putText(frame, str(round(confidence * 100, 2)) + '%', (box[0] + 10, box[1] + 40),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), thickness=2)
            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.texture = image_texture

    def on_stop(self):
        self.camera.release()

ScanningApp().run()
