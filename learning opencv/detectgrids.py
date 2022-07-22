import cv2,matplotlib.pyplot as plt

img=cv2.imread("./data/OIP.jfif")

found,corners=cv2.findChessboardCorners(img,(6,9))
assert found==True,'not found'

dbg_img=img.copy()
cv2.drawChessboardCorners(dbg_img,(6,9),corners,found)
plt.figure(figsize=(8,8))
plt.subplot(221)
plt.imshow(img)
plt.show()
