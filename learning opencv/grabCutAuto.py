import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('./data/cask3.jfif')
mask = np.zeros(img.shape[:2],np.uint8)
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)
rect = (50,50,450,290)
cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
contour,_=cv.findContours(mask2,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

for cnt in contour:
    area=cv.contourArea(cnt)
    if area>1000:
        box=cv.boundingRect(cnt)
        cv.rectangle(img,(box[0],box[1]),(box[0]+box[2],box[1]+box[3]),(0,255,0),2)

plt.imshow(img),plt.colorbar(),plt.show()