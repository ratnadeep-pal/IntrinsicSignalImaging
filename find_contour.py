from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
row=520
column=696
with open('20221219_145219/Camera #1/ManualRecording/20221219_145223178_3477465_3415000.raw','rb') as f:
    image = np.fromfile(f, dtype = np.uint16, count = row*column)
image = (image//256).astype(np.uint8)
#image = 255-image
image = image.reshape(row,column)
#image = cv.GaussianBlur(image,(1,1),0)
#image = cv.Canny(image,30,31)
#ret, thresh = cv.threshold(image, 127, 255, 0)
contours, hierarchy = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
mask = np.zeros_like(image,np.uint8)
for c in contours:
    if cv.contourArea(c) <5:
        cv.drawContours(mask, [c], -1, (255,0,0), 1)
#cv.drawContours(mask, contours, -1, (255,0,0), 1)
cv.imshow('image',image)
cv.waitKey(0)

