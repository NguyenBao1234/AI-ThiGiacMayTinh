import cv2
import numpy as np

print(cv2.__version__)


"""Test Image"""
QuaBom = cv2.imread('QuaBom.png')
cv2.imshow('AI Thi Giac May Tinh', QuaBom)

(w,h,d)=QuaBom.shape
print("CR= {}, CD= {}, ChieuSau= {}".format(h,w,d))

"""TestVideo"""
videoCat= cv2.VideoCapture('HuhCat.mp4')
while True:
    ret, frame = videoCat.read()
    if not ret:
        break
    cv2.imshow('VideoCat', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)