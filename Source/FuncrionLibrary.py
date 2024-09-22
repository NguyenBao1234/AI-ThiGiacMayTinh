import os

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