import cv2
import os
print(cv2.__version__)
print("press Q to quit the program")

"""Test Image"""
QuaBom = cv2.imread('../Asset/QuaBom.png')
'''if QuaBom is None:
    print("Error: Image not found or cannot be loaded.")
    exit()'''

cv2.imshow('AI Thi Giac May Tinh', QuaBom)

(w,h,d)=QuaBom.shape
print("CR= {}, CD= {}, ChieuSau= {}".format(h,w,d))

"""TestVideo"""
videoCat= cv2.VideoCapture('../Asset/HuhCat.mp4')
while True:
    ret, frame = videoCat.read()
    if not ret:
        break
    cv2.imshow('VideoCat', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Press any key to confirm...");break

cv2.waitKey(0)