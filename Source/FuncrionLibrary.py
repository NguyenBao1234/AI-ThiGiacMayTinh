import os
from kivy.core.audio import SoundLoader
from Audio import *


def GetImageArr():
    imgPathArr = []
    imgFile = '../ImageCaptured'
    for filename in os.listdir(imgFile):
        if filename.endswith('.jpg'):
            imgPath = os.path.join(imgFile, filename)
            imgPathArr.append(imgPath)
    return imgPathArr

def AmountImage():
    imgFile = '../ImageCaptured'
    i = 0
    for filename in os.listdir(imgFile):
        if filename.endswith('.jpg'):
            i +=1
    return  i

def GetImageAt(index):
    a = AmountImage()
    if a > 0:
        if index < a :
            return GetImageArr()[a-1-index]


def Dectect(self, frame):
    classIds, confs, bbox = self.net.detect(frame, confThreshold=0.5)
    return classIds, confs, bbox

def PlayInforObject(self, ObjectName):
    print("infor", {ObjectName})

def PlayInforObject(self, indexOfObject):
    pathAudio = GetPathAudio(indexOfObject)
    sound = SoundLoader.load(pathAudio)
    if sound != None:
        sound.play()
        sound.stop()