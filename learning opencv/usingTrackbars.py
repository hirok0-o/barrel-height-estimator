import cv2, numpy as np

cv2.namedWindow("win")

fill_val=np.array((255,255,255),np.uint8)

def trackBarFunc(idx,val):
    fill_val[idx]=val

cv2.createTrackbar("red","win",255,255,lambda val: trackBarFunc(2,val))
cv2.createTrackbar("green","win",255,255,lambda val: trackBarFunc(1,val))
cv2.createTrackbar("blue","win",255,255,lambda val: trackBarFunc(0,val))

while True:
    img=np.full((500,500,3),fill_val)
    cv2.imshow("win",img)
    key=cv2.waitKey(3)
    if key==27:
        break
cv2.destroyAllWindows()