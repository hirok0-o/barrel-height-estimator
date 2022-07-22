import cv2, matplotlib.pyplot as plt

img=cv2.imread("./data/car.jfif")

edges=cv2.Canny(img,200,100)

plt.figure(figsize=(8,5))
plt.subplot(121)
plt.axis("off")
plt.title("original")
plt.imshow(img[:,:,[2,1,0]])
plt.subplot(122)
plt.axis("off")
plt.title("edges")
plt.imshow(edges,cmap="gray")
plt.tight_layout()

plt.show()