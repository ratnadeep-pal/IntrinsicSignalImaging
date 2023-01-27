from matplotlib import pyplot as plt
import numpy as np
import cv2
row=520
column=696
with open('20221219_145219/Camera #1/ManualRecording/20221219_145223178_3477465_3415000.raw','rb') as f:
    image = np.fromfile(f, dtype = np.uint16, count = row*column)
image = image.reshape(row,column)
image = (image//256).astype(np.uint8)
print(np.max(image))
cv2.imshow('image',image)
cv2.waitKey(0)
#plt.imshow(image,cmap='gray')
#plt.show()